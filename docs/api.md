# API Contract v1

Base: /api/v1. JSON, ISO timestamps, cursor pagination; cap page size.

## Market
- GET /market/overview?country=IN&window=12m
- GET /market/trends?metric=new_postings&group_by=role&country=IN&from=&to=
- GET /market/compare?countries=IN,US,GB&role=
- GET /market/regions?country=IN&metric=
- GET /market/technology-radar?country=IN&window=12m
- GET /market/reports?period=monthly

## Jobs / skills / employers
- GET /jobs/search?q=&country=&role=&skill=&seniority=&remote=&posted_after=&cursor=
- GET /jobs/trending?country=IN&window=30d
- GET /jobs/{job_id}; GET /roles/{role_slug}
- GET /skills/trending?country=IN&window=90d; GET /skills/{skill_slug}
- GET /companies/top?country=IN&window=30d; GET /companies/{company_id}
- GET /salaries/overview?country=IN&role=

## Career (authenticated)
- GET/PUT /career/profile; GET/PUT /career/skills
- GET/POST /career/goals; POST /career/gap-analysis
- POST /career/roadmaps; GET /career/roadmaps/{roadmap_id}
- POST /career/progress; GET /career/job-matches; GET/PUT /career/alerts

## Response envelope
```json
{
 "data": [],
 "meta": {
  "metric": "unique_active_postings",
  "definition": "Distinct canonical postings observed active",
  "country": "IN", "period": {"from":"2026-01-01","to":"2026-01-31"},
  "source_coverage": ["provider-a"], "sample_size": 0,
  "freshness_at": "2026-02-01T02:00:00Z", "methodology_version": "v1"
 }
}
```

Public endpoints never expose career data. Career routes verify authenticated ownership. AI responses include evidence IDs and disclaimers. Rate-limit search and AI; cache market aggregates.