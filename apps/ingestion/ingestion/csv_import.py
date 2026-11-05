"""Offline CSV adapter: validates and normalizes user-provided job rows."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone

COUNTRIES = {"IN","US","GB","DE","CA","SG"}
REQUIRED = {"title", "company", "country_code", "source_url"}

def clean(value):
    return re.sub(r"\s+", " ", (value or "").strip())

def normalize(row, source):
    row = {k: clean(v) for k, v in row.items()}
    missing = [k for k in REQUIRED if not row.get(k)]
    if missing:
        raise ValueError("missing required fields: " + ", ".join(sorted(missing)))
    country = row["country_code"].upper()
    if country not in COUNTRIES:
        raise ValueError(f"country_code must be one of {sorted(COUNTRIES)}")
    title = row["title"]
    company = row["company"]
    identity = "|".join((title.casefold(), company.casefold(), country,
                         row.get("city","").casefold(), row.get("source_url","").casefold()))
    fingerprint = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return {
        "fingerprint": fingerprint, "source_key": source,
        "title": title, "company": company, "country_code": country,
        "source_url": row["source_url"], "posted_at": row.get("posted_at") or None,
        "city": row.get("city") or None, "remote_type": row.get("remote_type") or "unknown",
        "employment_type": row.get("employment_type") or None,
        "seniority": row.get("seniority") or None,
        "description": row.get("description") or None,
        "provider_job_id": row.get("provider_job_id") or None,
        "imported_at": datetime.now(timezone.utc).isoformat()
    }

def run(input_path, output_path, source):
    accepted, rejected, seen = 0, 0, set()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    reject_path = output_path.with_suffix(output_path.suffix + ".rejected.jsonl")
    with open(input_path, newline="", encoding="utf-8-sig") as src, \
         open(output_path, "w", encoding="utf-8") as out, \
         open(reject_path, "w", encoding="utf-8") as bad:
        reader = csv.DictReader(src)
        if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV headers must include: {sorted(REQUIRED)}")
        for line, row in enumerate(reader, start=2):
            try:
                item = normalize(row, source)
                if item["fingerprint"] in seen:
                    continue
                seen.add(item["fingerprint"])
                out.write(json.dumps(item, ensure_ascii=False) + "\\n")
                accepted += 1
            except Exception as exc:
                bad.write(json.dumps({"line": line, "error": str(exc), "row": row},
                                   ensure_ascii=False) + "\\n")
                rejected += 1
    return accepted, rejected

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out", default="data/normalized_jobs.jsonl")
    parser.add_argument("--source", default="manual_csv")
    args = parser.parse_args()
    a, r = run(args.input, args.out, args.source)
    print(f"accepted={a} rejected={r} output={args.out}")
