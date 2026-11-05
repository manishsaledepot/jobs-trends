# Metric Dictionary

## Definitions
- Job advertisement/posting: one listing captured from a provider.
- Unique posting: canonicalized listing after deduplication.
- Active observed posting: listing observed active under a documented source expiry policy.
- Official vacancy/opening: authority-defined statistical concept; never equate to scraped ads.
- Hiring demand index: normalized indicator, not literal vacancies.

## Metrics
- new_postings: unique postings first observed during a period.
- active_postings: distinct postings observed active on snapshot date.
- MoM % = (current period / prior period - 1) * 100.
- YoY % = (current period / same period previous year - 1) * 100.
- skill_share % = postings containing skill / eligible postings with parsed skills * 100.
- salary_median: comparable salary observations normalized for currency/pay period only with documented assumptions.
- employer_adoption: distinct employers posting for role/skill in period.
- trend_score: proprietary 0–100 composite, not official statistic.

## Trend score v1
Demand volume percentile 25%, growth percentile 30%, employer breadth 20%, salary signal 15%, persistence 10%. Normalize within comparable geography/window. Require minimum sample; suppress score when coverage shifts materially.

## Forecasts
Use seasonal-naive and moving-average baselines first; validate out of sample. Show horizon, interval, model version and error. Label predictions separately from observed metrics.

Every chart states geography, time range, definition, source set, freshness, sample and limitations.