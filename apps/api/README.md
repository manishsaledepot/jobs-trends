# API service

Python 3.11+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- Health: `GET /health`
- Market overview: `GET /api/v1/market/overview` (returns explicit no-data state until verified ingestion)
- OpenAPI docs: `/docs`

No secrets are needed for the health endpoint. Supabase integration will be added via environment variables and server-side service role only; never expose service-role keys in the browser.
