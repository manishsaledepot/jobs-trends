# Roadmap and Acceptance Criteria

## Milestone 2 — Architecture baseline
- [x] GitHub repository verified
- [x] Architecture, database, API, ingestion, metrics and roadmap docs
- [ ] Freeze v1 scope and data-source licensing decisions

## Milestone 3 — Data foundation
- [ ] Supabase project + secrets
- [ ] SQL migrations and RLS
- [ ] Seed 50 normalized roles + 200 skills
- [ ] Source registry/admin run view
- [ ] First permitted adapter with fixtures/tests
- [ ] Raw archive + quarantine
- [ ] Idempotency and dedup tests

## Milestone 4 — Market dashboard
- [ ] India overview with source/freshness disclosure
- [ ] Country comparison
- [ ] Monthly trend and role leaderboard
- [ ] Skill trend + technology radar
- [ ] Company and salary intelligence
- [ ] Filters for country, family, seniority, remote and period

## Milestone 5 — Career intelligence
- [ ] Profile, skills, target role/country
- [ ] Evidence-backed skill-gap analysis
- [ ] Transferable-role suggestions
- [ ] Learning roadmap and progress
- [ ] Saved jobs and alerts

## Milestone 6 — AI and reporting
- [ ] Grounded market summaries
- [ ] Monthly report generation
- [ ] Recommendation traceability
- [ ] Forecast baseline and evaluation

## Release gates
- Every metric traces to source + methodology; no fabricated data.
- Migration rollback and API contract tests.
- RLS test proves user A cannot read user B data.
- Adapter tests cover pagination, throttling, malformed rows and retries.
- Empty/low-coverage UI states and freshness labels.
- Secret/dependency scanning and backup restore drill.