from db import get_connection

def add_news(title, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(('INSERT INTO svt_news (title, url, date) VALUES (?, ?, date("now"))'), (title, url))
    conn.commit()
    conn.close()

def news_exists(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM svt_news WHERE title = ?', (title,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def check_if_news_exist(title, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(('INSERT INTO svt_news (title, url, date) VALUES (?, ?, date("now"))'), (title, url))
    conn.commit()
    conn.close()

def get_all_news():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM svt_news')
    rows = cursor.fetchall()
    conn.close()
    return rows

def execute_query(query, param = None):
    conn = get_connection()
    cursor = conn.cursor()
    if param :
        cursor.execute(query, param)
    else :
        cursor.execute(query)
    result = cursor.fetchall()  # Fetch the result after executing the query
    conn.commit()
    conn.close()
    return result  # Return the result

def process_news(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE svt_news SET processed = 1 WHERE title = ?', (title,))
    conn.commit()
    conn.close()

def news_is_processed(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT processed FROM svt_news WHERE title = ?', (title,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bool(result[0])  # Convert the result to a boolean value
    else:
        return False