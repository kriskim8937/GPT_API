from db import get_connection


def add_news(table, title, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        (f'INSERT INTO {table} (title, url, date) VALUES (?, ?, date("now"))'),
        (title, url),
    )
    conn.commit()
    conn.close()


def news_exists(table, title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE title = ?", (title,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def check_if_news_exist(title, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        ('INSERT INTO svt_news (title, url, date) VALUES (?, ?, date("now"))'),
        (title, url),
    )
    conn.commit()
    conn.close()


def get_all_news():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM svt_news")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_url(new_title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM svt_news where new_title = ?", (new_title,))
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]


def execute_query(query, param=None):
    conn = get_connection()
    cursor = conn.cursor()
    if param:
        cursor.execute(query, param)
    else:
        cursor.execute(query)
    result = cursor.fetchall()  # Fetch the result after executing the query
    conn.commit()
    conn.close()
    return result  # Return the result


def set_status_to_video_generated(new_title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE svt_news SET status = 'video_generated' WHERE new_title = ?", (new_title,))
    conn.commit()
    conn.close()

def set_status_to_video_uploaded(new_title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE svt_news SET status = 'video_uploaded' WHERE new_title = ?", (new_title,))
    conn.commit()
    conn.close()

def set_video_id(new_title, video_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE svt_news SET video_id = ? WHERE new_title = ?", (video_id, new_title,))
    conn.commit()
    conn.close()

def get_uploaded_videos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT video_id, url FROM svt_news where status = 'video_uploaded' AND video_id IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return rows