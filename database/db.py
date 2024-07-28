import sqlite3


# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY,
                       password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS failed_attempts
                      (username TEXT PRIMARY KEY,
                       attempts INTEGER,
                       last_attempt_time TIMESTAMP)''')
    conn.commit()
    conn.close()


