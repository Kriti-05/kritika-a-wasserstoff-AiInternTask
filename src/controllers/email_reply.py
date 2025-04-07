# email_reply.py

import smtplib
from email.mime.text import MIMEText
from src.utils.config import EMAIL, PASSWORD  # Add these in config.py

def send_email_reply(to_email, body):
    msg = MIMEText(body) 
    msg['From'] = EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        print(f"✅ Reply sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
