import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
from io import BytesIO
from datetime import datetime
import sqlite3  # SQLiteデータベースを使用

def scrape_all_data():
    url = 'https://www.meti.go.jp/statistics/tyo/iip/kako_press.html'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    reference_links = soup.find_all('a', href=lambda href: href and '/reference/' in href)
    base_url = 'https://www.meti.go.jp/statistics/tyo/iip/'

    # SQLiteデータベースに接続
    conn = sqlite3.connect('onwut_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports
                      (title TEXT, date TEXT, url TEXT, content TEXT)''')

    for link in reference_links:
        pdf_url = base_url + link['href']
        match = re.search(r'b\d{4}_(\d{6})', link['href'])
        if match:
            year_month = match.group(1)
            year = int(year_month[:4])
            month = int(year_month[4:])
            file_date = datetime(year, month, 1)

            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_response.content))
            pdf_text = ""
            for page in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page].extract_text()

            formatted_date = f"{file_date.year}-{file_date.month:02}"

            # データベースに全内容を保存
            cursor.execute('''INSERT INTO reports (title, date, url, content)
                              VALUES (?, ?, ?, ?)''', 
                              ("鉱工業生産", formatted_date, pdf_url, pdf_text))

    conn.commit()
    conn.close()
    print("すべてのデータが取得され、データベースに保存されました。")

if __name__ == "__main__":
    scrape_all_data()
