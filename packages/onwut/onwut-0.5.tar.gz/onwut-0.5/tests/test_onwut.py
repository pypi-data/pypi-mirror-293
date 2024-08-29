import unittest
from onwut.database import init_db, get_reports
from onwut.scraper import scrape_and_store_reports

class TestOnwut(unittest.TestCase):

    def test_database_initialization(self):
        conn = init_db()
        self.assertIsNotNone(conn)
        conn.close()

    def test_scraping_and_saving(self):
        conn = init_db()
        scrape_and_store_reports(conn, start_date="2024-01", end_date="2024-12", search_string="産業")
        reports = get_reports(conn, start_date="2024-01", end_date="2024-12", search_string="産業")
        self.assertGreater(len(reports), 0)
        conn.close()

if __name__ == '__main__':
    unittest.main()
