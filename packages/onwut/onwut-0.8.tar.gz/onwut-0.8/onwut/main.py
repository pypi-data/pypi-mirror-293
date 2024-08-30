import sqlite3
import os

def fetch_data(search_string=None, start_date=None, end_date=None, db_path=None):
    if db_path is None:
        # パッケージ内のデータベースファイルのパスを取得
        db_path = os.path.join(os.path.dirname(__file__), 'onwut_data.db')

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"データベースファイルが見つかりません: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT title, date, url, content FROM reports WHERE 1=1"
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

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    for row in results:
        title, date, url, content = row
        preview_content = content[:100]  # 最初の100文字のみを取得
        print(f"タイトル: {title}\n日付: {date}\nURL: {url}\n内容: {preview_content}...\n")

if __name__ == "__main__":
    # これはテスト用に使用するか、スクリプトとして直接実行する際にのみ適用
    fetch_data(search_string="生産", start_date="2024-01", end_date="2024-12")
