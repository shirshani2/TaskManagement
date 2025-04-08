from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from datetime import datetime
from app.models import tasks_collection, ai_collection, users_collection
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.ai.openai_utils import analyze_task_description
from app.telegram.telegram_utils import send_telegram_message

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


# Get all tasks for the current user
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = tasks_collection.find({"user_id": user_id})  
    result = []
    for task in tasks:
        task['_id'] = str(task['_id'])
        result.append(task)
    return jsonify(result), 200


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json

    title = data.get("title")
    description = data.get("description", "")
    due_date = data.get("due_date")
    status = data.get("status", "open")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # ✨ הרצת AI על התיאור
    try:
        ai_result = analyze_task_description(title, description)
        category = ai_result.get("category")
        time_estimate = ai_result.get("time_estimate")

        ai_collection.insert_one({
            "user_id": user_id,
            "description": description,
            "category": category,
            "time_estimate": time_estimate,
            "timestamp": datetime.utcnow()
        })

    except Exception as e:
        category = None
        time_estimate = None
        print("⚠️ שגיאה בניתוח AI:", e)

    task = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": status,
        "category": category,
        "time_estimate": time_estimate,
        "created_at": datetime.utcnow(),
    }

    result = tasks_collection.insert_one(task)
    task['_id'] = str(result.inserted_id)

    # ✅ שליחת טלגרם אם יש chat_id
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            chat_id = user.get("telegram_chat_id")
            if chat_id:
                from app.telegram.telegram_utils import send_telegram_message
                send_telegram_message(chat_id, f" נוספה משימה חדשה:📌\n{title}")
    except Exception as e:
        print("⚠️ לא נשלחה הודעת טלגרם:", e)

    return jsonify(task), 201


# Update a specific task – כולל category ו־time_estimate
@tasks_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        data = request.json

        # 🛠 כל השדות שמותר לעדכן
        allowed_fields = {
            "title", "description", "due_date", "status", "category", "time_estimate"
        }
        update = {key: value for key, value in data.items() if key in allowed_fields}

        if not update:
            return jsonify({"error": "No valid fields to update"}), 400

        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": update}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Task not found or not authorized"}), 404

        # ✉️ אם המשימה סומנה כבוצעה - שלח עדכון בטלגרם
        if update.get("status") == "done":
            user = users_collection.find_one({"_id": user_id})
            chat_id = user.get("telegram_chat_id")
            task = tasks_collection.find_one({"_id": ObjectId(task_id)})
            if chat_id and task:
                send_telegram_message(chat_id, f"✅ סימנת את המשימה כבוצעה: *{task['title']}*")

        return jsonify({"message": "Task updated"}), 200

    except errors.InvalidId:
        return jsonify({"error": "Invalid task ID"}), 400


# Delete a specific task
@tasks_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        result = tasks_collection.delete_one({"_id": ObjectId(task_id), "user_id": user_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Task not found or not authorized"}), 404
        return jsonify({"message": "Task deleted"}), 200
    except errors.InvalidId:
        return jsonify({"error": "Invalid task ID"}), 400
