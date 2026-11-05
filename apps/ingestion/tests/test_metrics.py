import unittest
from datetime import date
from ingestion.metrics import period_counts, month_over_month, skill_frequency, coverage_summary

class MetricTests(unittest.TestCase):
    def test_period_count_deduplicates(self):
        rows=[{"fingerprint":"a","posted_at":"2026-10-01"},{"fingerprint":"a","posted_at":"2026-10-01"},{"fingerprint":"b","posted_at":"2026-11-01"}]
        self.assertEqual(period_counts(rows,date(2026,10,1),date(2026,10,31)),1)
    def test_mom(self):
        self.assertEqual(month_over_month(120,100),20)
        self.assertIsNone(month_over_month(10,0))
    def test_skill_share_denominator(self):
        result=skill_frequency([("1","python"),("2","python"),("1","sql")],["1","2"])
        self.assertEqual(result[0]["share_pct"],100)
    def test_coverage_disclaimer(self):
        self.assertIn("not a complete census",coverage_summary({},5)["coverage_note"])

if __name__=="__main__": unittest.main()
