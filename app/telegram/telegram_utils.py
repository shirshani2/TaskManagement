import os
import requests
from dotenv import load_dotenv
from app.models import users_collection, tasks_collection
from app.ai.openai_utils import generate_tasks_summary

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def send_weekly_summaries():
    print("🚀 מריץ שליחת סיכומים שבועיים...")  # ✅ שורה חדשה

    users = users_collection.find({"telegram_chat_id": {"$exists": True}})

    for user in users:
        chat_id = user["telegram_chat_id"]
        user_id = user["_id"]
        user_id_str = str(user_id)
        open_tasks = list(tasks_collection.find({"user_id": user_id_str, "status": "open"}))
    

        if not open_tasks:
            print(f"📭 אין משימות פתוחות למשתמש {chat_id}")
            continue

        task_summary = "\n".join([f"- {task.get('title', '')}: {task.get('description', '')}" for task in open_tasks])

        try:
            summary = generate_tasks_summary(task_summary)
            send_telegram_message(chat_id, "🧠 סיכום משימות שבועי חכם:\n\n" + summary)
            print(f"✅ נשלח סיכום ל־{chat_id}")
        except Exception as e:
            print(f"❌ שגיאה בשליחת סיכום ל־{chat_id}: {str(e)}")
