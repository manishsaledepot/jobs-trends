from datetime import datetime, timezone
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="IT Market Intelligence API", version="0.2.0",
              description="Personal market analytics and career planning API.")
app.add_middleware(CORSMiddleware, allow_origins=[], allow_credentials=False,
                   allow_methods=["GET"], allow_headers=["Authorization", "Content-Type"])

class Health(BaseModel):
    status: str
    service: str
    timestamp: datetime

@app.get("/health", response_model=Health, tags=["system"])
def health():
    return Health(status="ok", service="market-intelligence-api",
                 timestamp=datetime.now(timezone.utc))

def _supabase_client():
    """Return a server-only client when configured; never expose service credentials."""
    url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        return None
    from supabase import create_client
    return create_client(url, key)

@app.get("/api/v1/market/overview", tags=["market"])
def market_overview():
    """Return verified stored metrics; no synthetic fallback values."""
    markets = ["IN", "US", "GB", "DE", "CA", "SG"]
    client = _supabase_client()
    if client is None:
        return {"status":"no_data","message":"Supabase is not configured; no verified metrics available.",
                "markets":markets,"metrics":[],"as_of":None,"source_coverage":[]}
    try:
        result = client.table("market_metrics").select(
            "metric_date,metric_key,country_code,region,role_slug,skill_slug,value,unit,sample_size,coverage,methodology_version"
        ).order("metric_date", desc=True).limit(500).execute()
        rows = result.data or []
        if not rows:
            return {"status":"no_data","message":"No verified market metrics have been calculated yet.",
                    "markets":markets,"metrics":[],"as_of":None,"source_coverage":[]}
        latest = max(row["metric_date"] for row in rows)
        return {"status":"ok","message":"Stored metrics; interpret with each metric's coverage and methodology.",
                "markets":markets,"metrics":rows,"as_of":latest,"source_coverage":[]}
    except Exception as exc:
        # Avoid leaking DB URLs, credentials, or provider error details.
        return {"status":"unavailable","message":"Market metrics could not be read from the configured database.",
                "markets":markets,"metrics":[],"as_of":None,"source_coverage":[]}
