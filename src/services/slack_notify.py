from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.utils.config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID

 

def send_important_alerts(emails):
    client = WebClient(token=SLACK_BOT_TOKEN)
    IMPORTANT_KEYWORDS = ["urgent", "asap", "important", "meeting", "deadline"]
    for email in emails:
        sender = email.get("sender", "")
         
        body = email.get("summary", "")

        if any(keyword in body.lower() for keyword in IMPORTANT_KEYWORDS):
            message = (
                f"🚨 *Important Email Alert* 🚨\n"
                f"📩 *From:* {sender}\n"
                f"{body[:300]}..."
            )

            try:
                client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
                print("✅ Slack notification sent!")
            except SlackApiError as e:
                print(f"❌ Slack Error: {e.response['error']}")
