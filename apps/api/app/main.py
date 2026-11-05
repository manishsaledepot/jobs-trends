from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="IT Market Intelligence API", version="0.1.0",
              description="Personal market analytics and career planning API.")

# Configure explicit origins before deployment; no wildcard credentials.
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

@app.get("/api/v1/market/overview", tags=["market"])
def market_overview():
    """Placeholder until a data source is ingested; never fabricate market counts."""
    return {
        "status": "no_data",
        "message": "No verified job-posting dataset has been ingested yet.",
        "markets": ["IN", "US", "GB", "DE", "CA", "SG"],
        "metrics": [],
        "as_of": None,
        "source_coverage": []
    }
