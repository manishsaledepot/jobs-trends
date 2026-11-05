# Database Blueprint

Use UUID primary keys, UTC timestamps and ISO country codes. Enable RLS on every user-owned table.

## Tables
- data_sources: provider, terms, coverage, enabled state
- source_runs: execution status, timestamps, counts, errors
- raw_job_records: payload, provider ID, hash, parse status
- companies, locations, job_roles, skills: canonical dimensions + aliases
- jobs: canonical posting and normalized attributes
- job_observations: source evidence over time
- job_skills: job-skill links, extraction method and confidence
- job_snapshots: daily active/observed state
- market_metrics: aggregate metric by date and dimensions, methodology version
- salary_observations: range, currency, pay period, source, normalized value
- career_profiles, career_skills, career_goals, learning_plans, learning_progress: private user workspace
- saved_jobs, market_alerts: personal saved records and alert settings

## Starter SQL
```sql
create extension if not exists pgcrypto;
create table data_sources (
 id uuid primary key default gen_random_uuid(), key text unique not null,
 name text not null, source_type text not null,
 terms_url text, coverage jsonb not null default '{}',
 enabled boolean not null default false, created_at timestamptz not null default now()
);
create table source_runs (
 id uuid primary key default gen_random_uuid(), source_id uuid not null references data_sources(id),
 started_at timestamptz not null default now(), finished_at timestamptz,
 status text not null check(status in ('queued','running','success','partial','failed')),
 fetched_count int not null default 0, accepted_count int not null default 0,
 rejected_count int not null default 0, duplicate_count int not null default 0,
 error_summary text, metadata jsonb not null default '{}'
);
create table companies (
 id uuid primary key default gen_random_uuid(), canonical_name text not null,
 normalized_name text unique not null, website text, created_at timestamptz default now()
);
create table job_roles (
 id uuid primary key default gen_random_uuid(), slug text unique not null,
 name text not null, family text not null, level text,
 parent_role_id uuid references job_roles(id)
);
create table skills (
 id uuid primary key default gen_random_uuid(), slug text unique not null,
 name text not null, category text not null, aliases text[] not null default '{}'
);
create table jobs (
 id uuid primary key default gen_random_uuid(), canonical_fingerprint text unique not null,
 title text not null, company_id uuid references companies(id), role_id uuid references job_roles(id),
 country_code char(2), city text, remote_type text default 'unknown', employment_type text,
 seniority text, posted_at timestamptz, first_seen_at timestamptz default now(),
 last_seen_at timestamptz default now(), expires_at timestamptz,
 status text not null default 'active' check(status in ('active','expired','closed','unknown'))
);
create index jobs_role_geo_date on jobs(role_id,country_code,posted_at desc);
create table job_observations (
 id uuid primary key default gen_random_uuid(), job_id uuid not null references jobs(id) on delete cascade,
 source_id uuid not null references data_sources(id), provider_job_id text,
 observed_at timestamptz not null default now(), source_posted_at timestamptz,
 source_url text, payload_hash text not null
);
create table job_skills (
 job_id uuid references jobs(id) on delete cascade, skill_id uuid references skills(id),
 extraction_method text not null, confidence numeric(4,3), primary key(job_id,skill_id)
);
create table job_snapshots (
 snapshot_date date not null, job_id uuid references jobs(id) on delete cascade,
 source_id uuid references data_sources(id), is_active boolean not null,
 observed boolean not null default true, primary key(snapshot_date,job_id,source_id)
);
```

Add raw_job_records, locations, market_metrics, salary and career tables in versioned migrations. For nullable aggregate dimensions use NULLS NOT DISTINCT (Postgres 15+) or a deterministic dimension key to prevent duplicate aggregates. User-owned tables need user_id -> auth.users and owner-only RLS.