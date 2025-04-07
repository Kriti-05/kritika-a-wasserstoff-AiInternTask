import sqlite3

# Connect to SQLite and create table if it doesn't exist
def initialize_db():
    conn = sqlite3.connect("src/data/emails.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_emails_to_db(emails):
    """Insert emails into database from list."""
    if not emails:
        print("ℹ️ No emails to store.")
        return

    initialize_db()

    conn = sqlite3.connect("src/data/emails.db")
    cursor = conn.cursor()

    for email in emails:
        cursor.execute('''
            INSERT INTO emails (sender, subject, body, timestamp) 
            VALUES (?, ?, ?, ?)
        ''', (email["sender"], email["subject"], email["body"], email["timestamp"]))

    conn.commit()
    conn.close()
    print(f"✅ {len(emails)} emails stored in the database.")
