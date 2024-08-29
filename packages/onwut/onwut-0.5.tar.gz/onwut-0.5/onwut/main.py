import sys
import re
from datetime import datetime, timedelta
from .database import init_db, get_reports
from .scraper import scrape_and_store_reports, parse_dates

def main(start_date=None, end_date=None, search_string=None, scrape=False):
    conn = init_db()

    if scrape:
        scrape_and_store_reports(conn, start_date, end_date, search_string)
    else:
        reports = get_reports(conn, start_date, end_date, search_string)
        for report in reports:
            title, date, url, content_preview = report
            print(f"タイトル: {title}\n日付: {date}\nURL: {url}\n内容: {content_preview}...\n")

    conn.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    search_string = None
    start_date = None
    end_date = None
    scrape = False

    if len(args) == 0:
        end_date = datetime.now().strftime('%Y-%m')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m')
    elif len(args) == 1:
        if re.match(r'^\d{4}(-\d{2})?$', args[0]):
            start_date = parse_dates(args[0]).strftime('%Y-%m')
            end_date = start_date
        else:
            search_string = args[0]
            end_date = datetime.now().strftime('%Y-%m')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m')
    elif len(args) == 2:
        start_date = parse_dates(args[0]).strftime('%Y-%m')
        end_date = parse_dates(args[1]).strftime('%Y-%m')
    elif len(args) == 3:
        start_date = parse_dates(args[0]).strftime('%Y-%m')
        end_date = parse_dates(args[1]).strftime('%Y-%m')
        search_string = args[2]
    elif len(args) == 4 and args[3] == "scrape":
        start_date = parse_dates(args[0]).strftime('%Y-%m')
        end_date = parse_dates(args[1]).strftime('%Y-%m')
        search_string = args[2]
        scrape = True
    else:
        print("使用方法: python script.py [開始日 [終了日]] [検索文字列] [scrape]")
        sys.exit(1)

    main(start_date, end_date, search_string, scrape)
