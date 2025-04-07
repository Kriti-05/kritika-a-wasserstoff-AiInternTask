import sqlite3
import re
from dateutil import parser

def add_calendar_events(emails):
    # Connect to database
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    # Create meetings table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            body TEXT,
            meeting_date TEXT,
            meeting_time TEXT
        )
    """)
    conn.commit()

    meeting_keywords = ["meeting", "schedule", "call", "appointment"]

    # Updated regex patterns
    date_pattern = r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)[,]?\s+\d{4}|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    time_pattern = r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|AM|PM)\b"

    found_any_meeting = False

    for email in emails:
        sender = email.get("sender", "")
        body = email.get("summary", "")
        email_text = body

        words = email_text.split()
        if any(keyword in words for keyword in meeting_keywords):
            date_matches = re.findall(date_pattern, email_text, re.IGNORECASE)
            time_matches = re.findall(time_pattern, email_text, re.IGNORECASE)

            if date_matches and time_matches:
                # Try combining the first date and first time
                combined = f"{date_matches[0]} {time_matches[0]}"
                try:
                    dt = parser.parse(combined, fuzzy=True)
                    meeting_date = dt.strftime("%Y-%m-%d")
                    meeting_time = dt.strftime("%H:%M")
                    
                    found_any_meeting = True
                    print(f"✅ Meeting scheduled on {meeting_date} at {meeting_time}.")
                    
                    cursor.execute("""
                        INSERT INTO meetings (sender, body, meeting_date, meeting_time)
                        VALUES (?, ?, ?, ?)
                    """, (sender, body, meeting_date, meeting_time))
                    conn.commit()
                except Exception as e:
                    print(f"⚠️ Parsing failed for: {combined} → {e}")
            else:
                print(f"❌ No valid date/time found in email from: {sender}")

    if not found_any_meeting:
        print("📭 No meeting-related emails with valid date/time found.")

    conn.close()
