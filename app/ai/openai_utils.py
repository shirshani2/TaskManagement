from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def analyze_task_description(title, description):
    prompt = f"""
אתה עוזר אישי חכם שמקבל משימה עם כותרת ותיאור, ומחזיר:
1. קטגוריה מתאימה (עבודה, לימודים, אישי, קניות, דחוף וכו') – בעברית ועם גיוון, תענה במילה אחת
2. הערכת זמן לביצוע – תמיד מספר שעות, גם אם מדובר בהערכה גסה

כותרת המשימה: "{title}"
תיאור המשימה: "{description or 'אין תיאור'}"

החזר תשובה בפורמט JSON עם המפתחות 'category' ו־'time_estimate' בלבד.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    content = response.choices[0].message.content
    return json.loads(content)

def ai_recommendation(tasks):
    
    prompt = f"""
        יש לי רשימת משימות שכתבתי לעצמי, והן מופיעות כאן:

        {tasks}

        אני רוצה שתתייחס לכל המשימות שכתבתי באופן אישי, תסביר לי מה אפשר ללמוד מהן, איך לנהל אותן טוב יותר לפי עקרונות הספר 'הרגלים אטומיים', ושתיתן לי המלצות קונקרטיות לשיפור ניהול הזמן שלי.

        חשוב לי ש:
        - תתייחס למשימות עצמן, לא תתן טיפים כלליים.
        - תציין דוגמאות מתוך המשימות שכתבתי.
        - תענה בעברית בלבד.
        - ההמלצות צריכות להיות מבוססות על הספר atomic habits (ותציין את זה)
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    content = response.choices[0].message.content
    return content


