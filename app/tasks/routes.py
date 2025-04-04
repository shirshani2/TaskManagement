from flask import Blueprint, request, jsonify
from bson import ObjectId, errors
from datetime import datetime
from app.models import tasks_collection  
from flask_jwt_extended import jwt_required, get_jwt_identity

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

# Create a new task
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    task = {
        "user_id": user_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "due_date": data.get("due_date"),
        "status": data.get("status", "open"),
        "created_at": datetime.utcnow(),
    }
    result = tasks_collection.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return jsonify(task), 201

# Get a specific task
@tasks_bp.route('/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            return jsonify({"error": "Task not found"}), 404
        task['_id'] = str(task['_id'])
        return jsonify(task), 200
    except errors.InvalidId:
        return jsonify({"error": "Invalid task ID"}), 400

# Update a specific task
@tasks_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        data = request.json
        update = {key: value for key, value in data.items() if key in ["title", "description", "due_date", "status"]}
        if not update:
            return jsonify({"error": "No valid fields to update"}), 400

        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id), "user_id": user_id},  # ← לוודא שהמשתמש יכול לעדכן רק את המשימות שלו
            {"$set": update}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Task not found or not authorized"}), 404

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
