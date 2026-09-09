import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
SQL_PATH = os.path.join(os.path.dirname(__file__), 't5_db.sql')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SQL_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()

def register_user(username, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user is not None

def truncate_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()

if __name__ == '__main__':
    # init_db()
    truncate_db()
    print("Database initialized.")
