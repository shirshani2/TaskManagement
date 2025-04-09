FROM python:3.10-slim

# הגדרת תקיית העבודה בתוך הקונטיינר
WORKDIR /app

# העתקת הקבצים לפרויקט
COPY . .

# התקנת ספריות
RUN pip install --no-cache-dir -r requirements.txt

# פתיחת הפורט שבו Flask רץ
EXPOSE 5000

# הרצת האפליקציה
CMD ["python", "run.py"]
