import os
import telebot
from dotenv import load_dotenv
from app.models import users_collection, tasks_collection
from app.ai.openai_utils import ai_recommendation

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['summary'])
def send_summary(message):
    chat_id = message.chat.id

    user = users_collection.find_one({"telegram_chat_id": chat_id})
    if not user:
        bot.reply_to(message, "🤖 לא הצלחנו לזהות אותך. אנא קשר/י את החשבון שלך תחילה דרך האתר.")
        return

    tasks = list(tasks_collection.find({"user_id": user["_id"], "status": "pending"}))
    if not tasks:
        bot.reply_to(message, "👏 כל הכבוד! אין לך משימות פתוחות.")
        return

    summary = "\n".join([f"- {t['title']}: {t.get('description', '')}" for t in tasks])

    try:
        recommendation = ai_recommendation(summary)
        bot.reply_to(message, f"🧠 סיכום חכם:\n\n{recommendation}")
    except Exception as e:
        bot.reply_to(message, f"❌ שגיאה בהפקת הסיכום: {str(e)}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 היי! שלח/י לי את קוד האימות שלך כדי לקשר את החשבון.")


@bot.message_handler(func=lambda message: True)
def handle_verification(message):
    print("📩 התקבלה הודעה בטלגרם:", message.text)

    code = message.text.strip()
    chat_id = message.chat.id

    user = users_collection.find_one({"telegram_verification_code": code})

    if user:
        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {"telegram_chat_id": chat_id},
                "$unset": {"telegram_verification_code": ""}
            }
        )
        bot.reply_to(message, "✅ החשבון שלך קושר בהצלחה!")
    else:
        bot.reply_to(message, "❌ קוד לא נמצא. ודאי שהזנת את הקוד נכון.")



bot.polling()
