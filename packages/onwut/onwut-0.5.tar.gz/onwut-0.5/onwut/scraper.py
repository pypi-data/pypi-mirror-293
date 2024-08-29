import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
from io import BytesIO
from datetime import datetime
from .database import save_report

def parse_dates(date_str):
    if re.match(r'^\d{4}-\d{2}$', date_str):
        return datetime.strptime(date_str, '%Y-%m')
    elif re.match(r'^\d{4}$', date_str):
        return datetime.strptime(date_str, '%Y')
    else:
        raise ValueError(f"不正な日付フォーマットです: {date_str}")

def scrape_and_store_reports(conn, start_date=None, end_date=None, search_string=None):
    url = 'https://www.meti.go.jp/statistics/tyo/iip/kako_press.html'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    reference_links = soup.find_all('a', href=lambda href: href and '/reference/' in href)
    base_url = 'https://www.meti.go.jp/statistics/tyo/iip/'

    for link in reference_links:
        pdf_url = base_url + link['href']
        match = re.search(r'b\d{4}_(\d{6})', link['href'])
        if match:
            year_month = match.group(1)
            year = int(year_month[:4])
            month = int(year_month[4:])
            file_date = datetime(year, month, 1).strftime('%Y-%m')

            # 日付範囲でフィルタリング
            if start_date and end_date:
                if not (start_date <= file_date <= end_date):
                    continue
            elif start_date:
                if not (start_date == file_date):
                    continue

            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_response.content))
            pdf_text = ""
            for page in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page].extract_text()

            if search_string and search_string not in pdf_text:
                continue

            preview_text = pdf_text[:30].replace("\n", " ")
            save_report(conn, "鉱工業生産", file_date, pdf_url, preview_text)
            print(f"タイトル: 鉱工業生産\n日付: {file_date}\nURL: {pdf_url}\n内容: {preview_text}...\n")
