from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import openai
from app.models import tasks_collection
from .openai_utils import ai_recommendation


ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/recommend', methods=['POST'])
@jwt_required()
def create_recommendation():
    user_id = get_jwt_identity()

    # שליפת כל המשימות של המשתמש
    user_tasks = list(tasks_collection.find({"user_id": user_id}))

    if not user_tasks:
        return jsonify({'message': 'No tasks found for user.'}), 404

    # בניית מחרוזת המתארת את כל המשימות
    task_summary = "\n".join([f"- {task.get('title', '')}: {task.get('description', '')}" for task in user_tasks])

    try:
       recommendation = ai_recommendation(task_summary)
       return jsonify({'recommendation': recommendation}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
