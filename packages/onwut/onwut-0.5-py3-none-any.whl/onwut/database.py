import sqlite3

def init_db():
    conn = sqlite3.connect('onwut.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            url TEXT,
            content_preview TEXT
        )
    ''')
    conn.commit()
    return conn

def save_report(conn, title, date, url, content_preview):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (title, date, url, content_preview)
        VALUES (?, ?, ?, ?)
    ''', (title, date, url, content_preview))
    conn.commit()

def get_reports(conn, start_date=None, end_date=None, search_string=None):
    cursor = conn.cursor()
    query = 'SELECT title, date, url, content_preview FROM reports WHERE 1=1'
    params = []

    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    if search_string:
        query += ' AND content_preview LIKE ?'
        params.append(f'%{search_string}%')

    cursor.execute(query, params)
    return cursor.fetchall()
