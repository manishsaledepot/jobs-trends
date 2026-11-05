"""Persist normalized JSONL into Supabase using server-side credentials.
Never put SUPABASE_SERVICE_ROLE_KEY in a frontend/browser environment."""
import argparse
import json
import os
from pathlib import Path
from supabase import create_client

def main(path):
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    client = create_client(url, key)
    source = client.table("data_sources").select("id").eq("key","manual_csv").single().execute().data
    source_id = source["id"]
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    accepted, duplicates = 0, 0
    for item in rows:
        company_name = item["company"].strip()
        normalized = " ".join(company_name.casefold().split())
        company = client.table("companies").upsert(
            {"canonical_name":company_name,"normalized_name":normalized},
            on_conflict="normalized_name").execute().data[0]
        job = client.table("jobs").upsert({
            "canonical_fingerprint":item["fingerprint"], "title":item["title"],
            "company_id":company["id"], "country_code":item["country_code"],
            "city":item.get("city"), "remote_type":item.get("remote_type","unknown"),
            "employment_type":item.get("employment_type"), "seniority":item.get("seniority"),
            "posted_at":item.get("posted_at"), "last_seen_at":item.get("imported_at")
        },on_conflict="canonical_fingerprint").execute().data[0]
        obs = client.table("job_observations").upsert({
            "job_id":job["id"], "source_id":source_id,
            "provider_job_id":item.get("provider_job_id"),
            "source_posted_at":item.get("posted_at"), "source_url":item["source_url"],
            "payload_hash":item["fingerprint"]
        },on_conflict="source_id,payload_hash").execute()
        accepted += 1
    print(f"processed={accepted} source=manual_csv")
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("jsonl")
    args=parser.parse_args()
    main(args.jsonl)
