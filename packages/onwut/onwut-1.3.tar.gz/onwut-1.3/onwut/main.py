import os
import sqlite3

def get_database_path():
    # パッケージに含まれるデータベースファイルのパスを取得
    package_dir = os.path.dirname(__file__)
    db_path = os.path.join(package_dir, 'onwut_data.db')
    return db_path

def fetch_data(search_string=None, start_date=None, end_date=None, source=None, limit=None, fields=None, db_path=None):
    if db_path is None:
        db_path = get_database_path()

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"データベースファイルが見つかりません: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 出力する項目を指定するための処理
    all_fields = ['title', 'date', 'url', 'content', 'source']
    if fields is None:
        fields = all_fields
    else:
        fields = [field for field in fields if field in all_fields]

    selected_fields = ", ".join(fields)
    
    query = f"SELECT {selected_fields} FROM reports WHERE 1=1"
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

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    for row in results:
        output = []
        for field, value in zip(fields, row):
            if field == 'content':
                value = value[:30]  # contentフィールドは最初の30文字のみ表示
            output.append(f"{field.capitalize()}: {value}")
        print("\n".join(output) + "\n")

if __name__ == "__main__":
    # 例: 産業に関するデータを2024年1月から12月の間に5件取得、表示する項目はタイトルと日付
    fetch_data(search_string="産業", start_date="2024-01", end_date="2024-12", limit=5, fields=['title', 'date'])
