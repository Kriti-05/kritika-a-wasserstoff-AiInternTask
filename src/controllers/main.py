# email_assistant_main.py

from src.services.fetch_pri_email import fetch_primary_emails, connect_to_gmail, connect_main
from src.utils.process_emails import extract_email_content
from src.services.store_emails import save_emails_to_db, initialize_db
from src.services.slack_notify import send_important_alerts
from src.controllers.calendar_tool import add_calendar_events
from src.services.web_search import is_question, serpapi_search
from src.utils.auto_reply_module import handle_auto_replies  # ✅ NEW

def main():
    print("🔄 Fetching emails...")
    raw_emails = connect_main()
    print(raw_emails[0])
    print()
    print("💾 Storing emails...")
    save_emails_to_db(raw_emails)
    print()
    print("🧹 Processing emails...")
    processed_emails = extract_email_content(raw_emails)
    print(processed_emails[0])
    print()
    # 🌐 Web search for questions in email
    for email in processed_emails:
        if is_question(email["summary"]):
            print("🌐 Web search triggered based on email content...")
            results = serpapi_search(email["summary"])
            print("🔎 Top Search Results:")
            for res in results:
                print(f"- {res['title']}\n  {res['link']}\n  {res['snippet']}\n")
    print()
    print("📣 Sending Slack notifications...")
    send_important_alerts(processed_emails)
    print()
    print("🗓️ Syncing calendar...")
    add_calendar_events(processed_emails)
    print()
    print("📬 Generating auto-replies...")
    handle_auto_replies(processed_emails)  # ✅ NEW

if __name__ == "__main__":
    main()
