import sqlite3

DB_PATH = "emails.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject TEXT,
            status TEXT,
            timestamp TEXT,
            task_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_email_log_sqlite(log_entry):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO emails (recipient, subject, status, timestamp, task_id)
        VALUES (?, ?, ?, ?, ?)
    """, (log_entry["recipient"], log_entry["subject"], log_entry["status"], log_entry["timestamp"], log_entry["task_id"]))
    conn.commit()
    conn.close()
