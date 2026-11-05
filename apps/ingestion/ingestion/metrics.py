"""Deterministic, explainable posting metrics from observed job rows."""
from collections import Counter
from datetime import date, datetime, timedelta

def parse_date(value):
    if not value: return None
    try: return datetime.fromisoformat(value.replace("Z","+00:00")).date()
    except ValueError: return None

def period_counts(rows, start, end, date_field="posted_at"):
    """Count unique fingerprints by first-posted date in inclusive window."""
    seen=set()
    total=0
    for row in rows:
        d=parse_date(row.get(date_field))
        fp=row.get("fingerprint") or row.get("canonical_fingerprint")
        if d and start<=d<=end and fp and fp not in seen:
            seen.add(fp); total+=1
    return total

def month_over_month(current, previous):
    if previous is None or previous == 0: return None
    return round((current/previous-1)*100,2)

def skill_frequency(job_skills, eligible_job_ids):
    eligible=set(eligible_job_ids)
    counts=Counter(skill for job_id,skill in job_skills if job_id in eligible)
    denom=len(eligible)
    return [{"skill":s,"jobs":n,"share_pct":round(n/denom*100,2) if denom else None}
            for s,n in counts.most_common()]

def coverage_summary(source_counts, total_jobs):
    """Source-level counts; never treat a source count as total market coverage."""
    return {"total_observed_jobs":total_jobs,
            "source_counts":dict(source_counts),
            "coverage_note":"Observed sample only; not a complete census of vacancies."}
