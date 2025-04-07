#!/usr/bin/env python
# coding: utf-8

import imaplib
import email
import json
from email.header import decode_header
from bs4 import BeautifulSoup
from src.utils.config import EMAIL, PASSWORD, IMAP_SERVER, MAILBOX

def connect_to_gmail():
    """Securely connect to Gmail's IMAP server."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        print("✅ Successfully connected to Gmail!")
        return mail
    except imaplib.IMAP4.error:
        print("❌ Failed to authenticate. Check your email/password.")
        return None

def fetch_primary_emails(mail, max_count=10):
    """
    Fetch all (read & unread) emails from Gmail's 'Primary' inbox category.
    """
    mail.select("inbox")
    status, messages = mail.uid('SEARCH', None, 'X-GM-RAW', 'category:primary')

    if status != "OK":
        print("❌ Error searching for primary emails.")
        return []

    email_uids = messages[0].split()
    if not email_uids:
        print("✅ No emails found in Primary.")
        return []

    emails_data = []

    # Process only the latest `max_count` emails
    for uid in reversed(email_uids[-max_count:]):
        status, msg_data = mail.uid('FETCH', uid, '(RFC822)')
        if status != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                # Decode sender
                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding or "utf-8", errors="ignore")

                # Extract email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() in ["text/plain", "text/html"]:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                # Convert HTML to plain text
                clean_body = BeautifulSoup(body, "html.parser").text.strip()

                # Store in list
                emails_data.append({
                    "sender": sender,
                    "subject": subject,
                    "body": clean_body,
                    "timestamp": msg["Date"]
                })

    # Save to file
    with open("primary_emails.json", "w", encoding="utf-8") as f:
        json.dump(emails_data, f, indent=4)

    print(f"✅ {len(emails_data)} primary emails saved to primary_emails.json")

    mail.logout()
    return emails_data

def connect_main():
    mail = connect_to_gmail()
    if mail:
        return fetch_primary_emails(mail, max_count=5)  # You can change this count

# Run it
if __name__ == "__main__":
    connect_main()
