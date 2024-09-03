import os
import psycopg2

def get_database_url():
    # ここでHerokuのDATABASE_URLをデフォルトに設定
    default_db_url = "postgres://udqo9u95b9ver2:p818daad9176bfa7f5c5cdd3e15d0993517d981a6cbbfa671f8399ccd3e80a2be@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7qbcmbmrj0c0b"
    return os.getenv("DATABASE_URL", default_db_url)

def fetch_data(search_string=None, start_date=None, end_date=None, source=None, limit=10):
    db_url = get_database_url()

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    query = "SELECT title, date, url, content, source FROM reports WHERE 1=1"
    params = []

    if search_string:
        query += " AND content LIKE %s"
        params.append(f"%{search_string}%")

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"
        params.append(end_date)

    if source:
        query += " AND source = %s"
        params.append(source)

    query += " LIMIT %s"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    for row in results:
        title, date, url, content, source = row
        preview_content = content[:30]  # 最初の30文字のみを取得
        print(f"タイトル: {title}\n日付: {date}\nURL: {url}\nソース: {source}\n内容: {preview_content}...\n")

if __name__ == "__main__":
    fetch_data(search_string="産業", start_date="2024-01", end_date="2024-12", limit=5)
