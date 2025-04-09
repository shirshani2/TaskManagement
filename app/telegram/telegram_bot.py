import os
import telebot
from dotenv import load_dotenv
from app.models import users_collection, tasks_collection
from app.ai.openai_utils import ai_recommendation, generate_tasks_summary
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler
from app.telegram.telegram_utils import send_weekly_summaries


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)




@bot.message_handler(commands=['summary'])
def send_tasks_summary(message):
    chat_id = message.chat.id
    
    # מצא את המשתמש לפי מזהה הצ'אט
    user = users_collection.find_one({"telegram_chat_id": chat_id})
    
    if not user:
        bot.reply_to(message, "❌ החשבון שלך לא מקושר למערכת. אנא התחבר דרך האפליקציה תחילה.")
        return
    
    user_id = user["_id"]
    user_id_str = str(user_id)
    open_tasks = list(tasks_collection.find({"user_id": user_id_str, "status": "open"}))
    
    
   
    
    if not open_tasks:
        bot.reply_to(message, "אין לך משימות פתוחות כרגע. 🎉")
        return
    
    # יצירת מחרוזת המתארת את המשימות
    task_summary = "\n".join([f"- {task.get('title', '')}: {task.get('description', '')}" for task in open_tasks])
    
    bot.send_message(chat_id, "מייצר סיכום משימות שבועי חכם מבוסס AI⏳... ")
    
    try:
        # שימוש בפונקציה החדשה ליצירת סיכום חכם
        summary = generate_tasks_summary(task_summary)
        bot.send_message(chat_id, summary)
    except Exception as e:
        bot.send_message(chat_id, f"❌ אירעה שגיאה: {str(e)}")
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




scheduler = BackgroundScheduler()
scheduler.add_job(send_weekly_summaries, 'cron', day_of_week='sun', hour=10, minute=31)
scheduler.start()
bot.polling()
