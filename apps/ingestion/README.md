# Ingestion starter (offline-first)

The first adapter is a user-controlled CSV import. It does not scrape websites or call paid APIs.

## Required columns
`title,company,country_code,source_url`
Optional: `posted_at,city,remote_type,employment_type,seniority,description,provider_job_id`

```bash
python -m ingestion.csv_import path/to/jobs.csv --out data/normalized_jobs.jsonl --source manual_csv
```

Rows with missing title/country or invalid country codes are quarantined in `*.rejected.jsonl`.
The importer fingerprints records deterministically and de-duplicates within the file.
Keep original files in a private location; do not commit personal data or licensed datasets.

## Supabase persistence (optional)

Install ingestion dependencies with `pip install -r requirements.txt`. After applying `supabase/migrations` and the taxonomy seed, set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in a private shell environment (see `.env.example`; never commit actual values). Run `python -m ingestion.persist_supabase data/normalized_jobs.jsonl`. The service-role key is backend-only and must never be used in a browser.

## Metrics module
`ingestion.metrics` provides pure, testable observed-posting counts, MoM change, skill shares, and source-coverage disclaimers. These are sample metrics, not estimates of all vacancies.
