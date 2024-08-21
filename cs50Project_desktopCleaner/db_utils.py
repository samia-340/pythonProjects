import sqlite3
from typing import Tuple
import sys
def create_activity_log_table(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            timestamp TEXT,
            action TEXT,
            source TEXT,
            destination TEXT
        )
    ''')
    conn.commit()

def insert_activity_log(conn: sqlite3.Connection, session_id: str, action: str, source: str, destination: str) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (session_id, timestamp, action, source, destination)
        VALUES (?, datetime('now'), ?, ?, ?)
    ''', (session_id, action, source, destination))
    conn.commit()

def fetch_activity_summary(conn: sqlite3.Connection, session_id: str) -> Tuple:
    cursor = conn.cursor()
    cursor.execute('''
        SELECT action, COUNT(*)
        FROM activity_log
        WHERE session_id = ?
        GROUP BY action
    ''', (session_id,))
    action_counts = cursor.fetchall()

    cursor.execute('''
        SELECT timestamp, action, source, destination
        FROM activity_log
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT 10
    ''', (session_id,))
    recent_actions = cursor.fetchall()
    return action_counts, recent_actions

if __name__ == "__main__":
    print("db_utils is successful")
   
    print(sys.path)