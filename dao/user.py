import sqlite3
from datetime import datetime


def account_exist_or_not(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return True
    return False


def add_account(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def get_failed_attempts(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT attempts, last_attempt_time FROM failed_attempts WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    if row:
        attempts, last_attempt_time = row
        return attempts, last_attempt_time
    else:
        return None, None


def get_password_by_username(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None


def upsert_failed_attempts_db(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    attempts, last_attempt_time = get_failed_attempts(username)
    if attempts is None:
        cursor.execute("INSERT INTO failed_attempts (username, attempts, last_attempt_time) VALUES (?, ?, ?)",
                       (username, 1, datetime.now().isoformat()))
    else:
        cursor.execute("UPDATE failed_attempts SET attempts = attempts + 1, last_attempt_time = ? WHERE username = ?",
                       (datetime.now().isoformat(), username))
    conn.commit()
    conn.close()


def delete_failed_attempts(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM failed_attempts WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def remove_test_data(username: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    cursor.execute("DELETE FROM failed_attempts WHERE username = ?", (username,))
    conn.commit()
    conn.close()