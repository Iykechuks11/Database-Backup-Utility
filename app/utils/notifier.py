import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_notification(message, success=True):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("⚠️ Warning: SLACK_WEBHOOK_URL not set. Skipping notification.")
        return

    emoji = "✅" if success else "❌"
    payload = {
        "text": f"{emoji} *Database Backup Report*\n{message}"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("✅ Slack notification sent.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Slack notification: {e}")