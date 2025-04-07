import re
from src.controllers.email_reply import send_email_reply

def extract_meeting_info(body):
    """
    Extract meeting date and time using regex.
    Returns (meeting_date, meeting_time) or (None, None) if not found.
    """
    date_match = re.search(r"postponed to (\d{1,2}(st|nd|rd|th)?\s+\w+|\w+\s+\d{1,2}(st|nd|rd|th)?|\d{1,2}/\d{1,2}/\d{2,4})", body)
    time_match = re.search(r"(\d{1,2}(:\d{2})?\s*(am|pm|AM|PM))", body)

    date = date_match.group(1) if date_match else None
    time = time_match.group(1) if time_match else None
    return date, time

def extract_sender_name(sender):
    """
    Extracts name from the sender field (e.g., "John Doe <email@gmail.com>")
    """
    name_match = re.match(r"(.+?)\s*<", sender)
    return name_match.group(1).strip() if name_match else sender

def generate_ack_reply(sender_name, meeting_date, meeting_time):
    return f"""Hi {sender_name},

Thanks for the update. I've noted that the meeting has been postponed to {meeting_date} at {meeting_time}.

Looking forward to it!

Best regards,  
Your Assistant 🤖
"""

def handle_auto_replies(processed_emails):
    for email in processed_emails:
        sender = email.get("sender", "") 
        body = email.get("summary", "").lower()

        if "meeting" in body and "postponed to" in body:
            meeting_date, meeting_time = extract_meeting_info(body)

            if meeting_date and meeting_time:
                sender_name = extract_sender_name(sender)
                reply_body = generate_ack_reply(sender_name, meeting_date, meeting_time)
                send_email_reply(sender, reply_body)
                print(f"✅ Auto-replied to {sender_name}")
            else:
                print(f"⚠️ Could not extract meeting time/date from email: {subject}")
