import os
import sqlite3

def get_database_path():
    home_dir = os.path.expanduser("~")
    db_dir = os.path.join(home_dir, ".onwut")
    db_path = os.path.join(db_dir, "onwut_data.db")
    return db_path

def fetch_data(search_string=None, start_date=None, end_date=None, source=None, db_path=None):
    if db_path is None:
        db_path = get_database_path()

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"データベースファイルが見つかりません: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT title, date, url, content, source FROM reports WHERE 1=1"
    params = []

    if search_string:
        query += " AND content LIKE ?"
        params.append(f"%{search_string}%")

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    if source:
        query += " AND source = ?"
        params.append(source)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    for row in results:
        title, date, url, content, source = row
        preview_content = content[:30]  # 最初の30文字のみを取得
        print(f"タイトル: {title}\n日付: {date}\nURL: {url}\nソース: {source}\n内容: {preview_content}...\n")

if __name__ == "__main__":
    fetch_data(search_string="産業", start_date="2024-01", end_date="2024-12")
