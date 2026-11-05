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
