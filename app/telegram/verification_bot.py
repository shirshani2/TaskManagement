import os
import telebot
from dotenv import load_dotenv
from app.models import users_collection, tasks_collection
from app.ai.openai_utils import ai_recommendation, generate_tasks_summary
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId


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
    print(f"DEBUG: מחפש משימות למשתמש עם ID: {user_id}, מסוג: {type(user_id)}")
    
    # ננסה למצוא משימות עם מספר וריאציות של user_id
    # אופציה 1: השתמש ב-user_id כפי שהוא
    open_tasks = list(tasks_collection.find({"user_id": user_id, "status": "open"}))
    print(f"DEBUG: נמצאו {len(open_tasks)} משימות באופציה 1")
    
    if not open_tasks:
        # אופציה 2: נסה להשתמש ב-user_id כמחרוזת
        user_id_str = str(user_id)
        open_tasks = list(tasks_collection.find({"user_id": user_id_str, "status": "open"}))
        print(f"DEBUG: נמצאו {len(open_tasks)} משימות באופציה 2")
    
    if not open_tasks:
        # אופציה 3: נסה להמיר את ה-user_id למחרוזת אם הוא לא ObjectId
        try:
            user_id_obj = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
            open_tasks = list(tasks_collection.find({"user_id": user_id_obj, "status": "open"}))
            print(f"DEBUG: נמצאו {len(open_tasks)} משימות באופציה 3")
        except:
            pass
    
    # בדיקה נוספת: הצג את כל המשימות ללא סינון לפי user_id
    all_tasks = list(tasks_collection.find({"status": "open"}))
    user_ids = set([task.get("user_id") for task in all_tasks])
    print(f"DEBUG: סה״כ משימות פתוחות במערכת: {len(all_tasks)}")
    print(f"DEBUG: מזהי משתמשים קיימים: {user_ids}")
    
    if not open_tasks:
        bot.reply_to(message, "אין לך משימות פתוחות כרגע. 🎉")
        return
    
    # יצירת מחרוזת המתארת את המשימות
    task_summary = "\n".join([f"- {task.get('title', '')}: {task.get('description', '')}" for task in open_tasks])
    
    bot.send_message(chat_id, "מייצר סיכום משימות שבועי חכם... ⏳")
    
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





bot.polling()
