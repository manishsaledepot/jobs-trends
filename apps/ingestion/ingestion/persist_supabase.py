"""Persist normalized JSONL into Supabase with auditable source-run lifecycle.
Service-role credentials are backend-only; never expose them to browser code."""
import argparse
import json
import os
from pathlib import Path
from supabase import create_client


def main(path: str) -> None:
    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    source = client.table("data_sources").select("id").eq("key", "manual_csv").single().execute().data
    source_id = source["id"]
    lines = [line for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    items = [json.loads(line) for line in lines]
    run = client.table("source_runs").insert({
        "source_id": source_id, "status": "running", "fetched_count": len(items),
        "metadata": {"adapter": "manual_csv", "input_file": Path(path).name},
    }).execute().data[0]

    accepted = rejected = duplicates = 0
    errors = []
    try:
        for item in items:
            try:
                fingerprint = item["fingerprint"]
                company_name = item["company"].strip()
                normalized = " ".join(company_name.casefold().split())
                company = client.table("companies").upsert(
                    {"canonical_name": company_name, "normalized_name": normalized},
                    on_conflict="normalized_name").execute().data[0]
                job = client.table("jobs").upsert({
                    "canonical_fingerprint": fingerprint, "title": item["title"],
                    "company_id": company["id"], "country_code": item["country_code"],
                    "city": item.get("city"), "remote_type": item.get("remote_type", "unknown"),
                    "employment_type": item.get("employment_type"), "seniority": item.get("seniority"),
                    "posted_at": item.get("posted_at"), "last_seen_at": item.get("imported_at"),
                }, on_conflict="canonical_fingerprint").execute().data[0]
                # Preserve the raw normalized record for audit/reprocessing.
                client.table("raw_job_records").upsert({
                    "source_id": source_id, "source_run_id": run["id"],
                    "provider_job_id": item.get("provider_job_id"),
                    "payload": item, "payload_hash": fingerprint, "parse_status": "accepted",
                }, on_conflict="source_id,payload_hash").execute()
                client.table("job_observations").upsert({
                    "job_id": job["id"], "source_id": source_id,
                    "provider_job_id": item.get("provider_job_id"),
                    "source_posted_at": item.get("posted_at"), "source_url": item["source_url"],
                    "payload_hash": fingerprint,
                }, on_conflict="source_id,payload_hash").execute()
                accepted += 1
            except Exception as exc:  # isolate malformed records; retain run diagnostics
                rejected += 1
                errors.append(str(exc)[:300])
        status = "success" if rejected == 0 else ("partial" if accepted else "failed")
        client.table("source_runs").update({
            "status": status, "finished_at": "now()",
            "accepted_count": accepted, "rejected_count": rejected,
            "duplicate_count": duplicates,
            "error_summary": "; ".join(errors[:5]) or None,
        }).eq("id", run["id"]).execute()
        print(f"run={run['id']} status={status} fetched={len(items)} accepted={accepted} rejected={rejected}")
    except Exception:
        client.table("source_runs").update({
            "status": "failed", "finished_at": "now()", "accepted_count": accepted,
            "rejected_count": rejected, "error_summary": "Unexpected persistence failure",
        }).eq("id", run["id"]).execute()
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl")
    main(parser.parse_args().jsonl)
