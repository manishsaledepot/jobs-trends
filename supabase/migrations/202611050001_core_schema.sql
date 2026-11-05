-- IT Market Intelligence Board | personal-use foundation
-- Run with Supabase CLI: supabase db push
create extension if not exists pgcrypto;

create table if not exists public.data_sources (
 id uuid primary key default gen_random_uuid(), key text unique not null, name text not null,
 source_type text not null, terms_url text, coverage jsonb not null default '{}',
 enabled boolean not null default false, created_at timestamptz not null default now()
);
create table if not exists public.source_runs (
 id uuid primary key default gen_random_uuid(), source_id uuid not null references public.data_sources(id),
 started_at timestamptz not null default now(), finished_at timestamptz,
 status text not null check(status in ('queued','running','success','partial','failed')),
 fetched_count int not null default 0, accepted_count int not null default 0,
 rejected_count int not null default 0, duplicate_count int not null default 0,
 error_summary text, metadata jsonb not null default '{}'
);
create table if not exists public.raw_job_records (
 id uuid primary key default gen_random_uuid(), source_id uuid not null references public.data_sources(id),
 source_run_id uuid references public.source_runs(id), provider_job_id text, payload jsonb not null,
 payload_hash text not null, received_at timestamptz not null default now(),
 parse_status text not null default 'pending' check(parse_status in ('pending','accepted','rejected','duplicate')),
 parse_error text, unique(source_id,payload_hash)
);
create table if not exists public.companies (
 id uuid primary key default gen_random_uuid(), canonical_name text not null, normalized_name text unique not null,
 website text, created_at timestamptz not null default now()
);
create table if not exists public.job_roles (
 id uuid primary key default gen_random_uuid(), slug text unique not null, name text not null,
 family text not null, level text, parent_role_id uuid references public.job_roles(id)
);
create table if not exists public.skills (
 id uuid primary key default gen_random_uuid(), slug text unique not null, name text not null,
 category text not null, aliases text[] not null default '{}'
);
create table if not exists public.jobs (
 id uuid primary key default gen_random_uuid(), canonical_fingerprint text unique not null,
 title text not null, company_id uuid references public.companies(id), role_id uuid references public.job_roles(id),
 country_code char(2), city text, remote_type text not null default 'unknown',
 employment_type text, seniority text, posted_at timestamptz, first_seen_at timestamptz not null default now(),
 last_seen_at timestamptz not null default now(), expires_at timestamptz,
 status text not null default 'active' check(status in ('active','expired','closed','unknown'))
);
create index if not exists jobs_role_geo_date on public.jobs(role_id,country_code,posted_at desc);
create index if not exists jobs_country_seen on public.jobs(country_code,first_seen_at desc);
create table if not exists public.job_observations (
 id uuid primary key default gen_random_uuid(), job_id uuid not null references public.jobs(id) on delete cascade,
 source_id uuid not null references public.data_sources(id), provider_job_id text,
 observed_at timestamptz not null default now(), source_posted_at timestamptz, source_url text,
 payload_hash text not null, unique(source_id,payload_hash)
);
create table if not exists public.job_skills (
 job_id uuid references public.jobs(id) on delete cascade, skill_id uuid references public.skills(id) on delete cascade,
 extraction_method text not null, confidence numeric(4,3), primary key(job_id,skill_id)
);
create table if not exists public.job_snapshots (
 snapshot_date date not null, job_id uuid references public.jobs(id) on delete cascade,
 source_id uuid references public.data_sources(id), is_active boolean not null,
 observed boolean not null default true, primary key(snapshot_date,job_id,source_id)
);
create table if not exists public.market_metrics (
 id uuid primary key default gen_random_uuid(), metric_date date not null, metric_key text not null,
 country_code char(2), region text, role_slug text, skill_slug text, company_key text,
 value numeric not null, unit text not null, sample_size integer, coverage jsonb not null default '{}',
 methodology_version text not null default 'v1', calculated_at timestamptz not null default now(),
 dimension_key text generated always as (coalesce(country_code,'*')||'|'||coalesce(region,'*')||'|'||coalesce(role_slug,'*')||'|'||coalesce(skill_slug,'*')||'|'||coalesce(company_key,'*')) stored,
 unique(metric_date,metric_key,dimension_key,methodology_version)
);
create table if not exists public.salary_observations (
 id uuid primary key default gen_random_uuid(), job_id uuid references public.jobs(id) on delete cascade,
 source_id uuid references public.data_sources(id), min_amount numeric, max_amount numeric,
 currency char(3), pay_period text, normalized_annual_min numeric, normalized_annual_max numeric,
 observed_at timestamptz not null default now(), normalization_note text
);
-- Personal workspace: isolated to the authenticated owner.
create table if not exists public.career_profiles (
 user_id uuid primary key references auth.users(id) on delete cascade, display_name text,
 present_role text, experience_years numeric, target_countries text[] not null default array['IN'],
 target_roles text[] not null default '{}', career_goal text, updated_at timestamptz not null default now()
);
create table if not exists public.career_skills (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
 skill_id uuid references public.skills(id), skill_name text not null, proficiency text not null default 'learning',
 years_experience numeric, evidence text, updated_at timestamptz not null default now()
);
create table if not exists public.career_goals (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
 title text not null, target_role text, target_country char(2), target_date date, status text not null default 'active',
 created_at timestamptz not null default now()
);
create table if not exists public.learning_plans (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
 title text not null, target_skill text, plan jsonb not null default '[]', status text not null default 'active',
 created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create table if not exists public.learning_progress (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
 plan_id uuid references public.learning_plans(id) on delete cascade, item text not null,
 completed boolean not null default false, completed_at timestamptz, notes text
);
create table if not exists public.saved_jobs (
 user_id uuid not null references auth.users(id) on delete cascade, job_id uuid not null references public.jobs(id) on delete cascade,
 saved_at timestamptz not null default now(), notes text, primary key(user_id,job_id)
);
create table if not exists public.market_alerts (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
 name text not null, criteria jsonb not null default '{}', enabled boolean not null default true,
 created_at timestamptz not null default now()
);

-- RLS on personal data; market tables can be read by authenticated users only initially.
alter table public.career_profiles enable row level security;
alter table public.career_skills enable row level security;
alter table public.career_goals enable row level security;
alter table public.learning_plans enable row level security;
alter table public.learning_progress enable row level security;
alter table public.saved_jobs enable row level security;
alter table public.market_alerts enable row level security;
do $$
declare t text;
begin
 foreach t in array array['career_profiles','career_skills','career_goals','learning_plans','learning_progress','saved_jobs','market_alerts'] loop
  execute format('drop policy if exists owner_all on public.%I',t);
  execute format('create policy owner_all on public.%I for all using (user_id = auth.uid()) with check (user_id = auth.uid())',t);
 end loop;
end $$;

-- Seed source registry; disabled until terms/access have been checked.
insert into public.data_sources(key,name,source_type,coverage,enabled) values
 ('manual_csv','Manual CSV import','user_upload','{"countries":["IN","US","GB","DE","CA","SG"]}',true),
 ('adzuna','Adzuna API','api','{"countries":["IN","US","GB","DE","CA","SG"]}',false)
on conflict(key) do nothing;
