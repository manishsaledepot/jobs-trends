# Milestone 3 — Data Foundation Status

## Implemented in repository
- [x] Versioned Supabase migration for source registry, run logs, raw payloads, jobs, observations, skills, snapshots, metrics, salary observations.
- [x] Personal career tables and owner-scoped RLS policies.
- [x] Seed source registry (manual CSV enabled; API source disabled pending terms/access review).
- [x] FastAPI service scaffold with health and truthful no-data market endpoint.
- [x] Offline CSV adapter with normalization, deterministic fingerprints, duplicate suppression, rejected-row quarantine.
- [x] Adapter unit tests authored.

## Not yet verified / pending
- [ ] Run migration against a Supabase project and inspect policies.
- [ ] Execute Python tests in CI/local environment.
- [ ] Connect API to Supabase using server-only credentials.
- [ ] Seed role/skill taxonomy (first 50 roles / 200 skills).
- [ ] Add ingestion-to-database persistence and source run lifecycle.
- [ ] Choose and verify a legally permitted live job-data provider.

## Privacy/cost guardrails
Personal project. No production/public deployment, paid service, paid API, or secret is created by this milestone. Market data remains empty until an actual source is configured; dashboards must not manufacture counts.
