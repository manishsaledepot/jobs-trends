import tempfile
import unittest
from pathlib import Path
from ingestion.csv_import import normalize, run

class CsvImportTests(unittest.TestCase):
    def test_normalize_country_and_fingerprint(self):
        row = {"title":" Backend Engineer ", "company":" ACME ", "country_code":"in",
               "source_url":"https://example.test/job/1"}
        item = normalize(row, "manual_csv")
        self.assertEqual(item["country_code"], "IN")
        self.assertEqual(item["title"], "Backend Engineer")
        self.assertEqual(item["fingerprint"], normalize(row, "manual_csv")["fingerprint"])

    def test_reject_missing_title(self):
        with self.assertRaises(ValueError):
            normalize({"company":"X","country_code":"IN","source_url":"x"}, "manual_csv")

    def test_reject_unknown_country(self):
        with self.assertRaises(ValueError):
            normalize({"title":"T","company":"X","country_code":"ZZ","source_url":"x"}, "manual_csv")

    def test_file_dedup_and_quarantine(self):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d)/"in.csv", Path(d)/"out.jsonl"
            src.write_text("title,company,country_code,source_url\\nT,X,IN,u\\nT,X,IN,u\\n,XX,IN,u\\n")
            accepted, rejected = run(src, out, "manual_csv")
            self.assertEqual((accepted,rejected),(1,1))
            self.assertEqual(len(out.read_text().splitlines()),1)

if __name__ == "__main__":
    unittest.main()
