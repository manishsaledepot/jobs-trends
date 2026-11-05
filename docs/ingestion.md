# Ingestion and Data Quality

## Adapter contract
Each adapter implements fetch_page(cursor, query, date_window), normalize(raw), source_metadata(), rate_limit_policy() and health_check().

Normalized record: provider_id, title (required), company, ISO country_code, city, posted_at, URL, description, salary_min/max/currency, employment_type, remote_type and source_id.

## Source onboarding
1. Confirm license, retention, attribution and redistribution terms.
2. Document geography, categories, cadence and historical access.
3. Respect pagination, quotas, rate limits and retries.
4. Keep API keys in server secrets; never commit credentials.
5. Add fixtures, schema-drift tests and monitoring.
6. Add source kill switch and coverage/freshness display.

## Quality gates
- Required title/source ID; validate country and date.
- Quarantine malformed salary ranges; missing salary is null, not zero.
- Normalize company/role aliases.
- Deduplicate by provider ID; fallback title/company/location/date fingerprint.
- Detect future dates, duplicate bursts, stale feeds and source volume anomalies.
- Record fetched/accepted/rejected/duplicate counts for every run.

Start with two permitted structured job APIs plus official labor statistics. Employer career-page connectors require permission/terms review. Hiring reports are report-level observations, not job posting counts.