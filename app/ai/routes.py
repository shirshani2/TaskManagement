from flask import Blueprint, request, jsonify
from .openai_utils import analyze_task_description
from app.models import ai_collection  
from datetime import datetime

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Missing task description'}), 400

    try:
        analysis = analyze_task_description(description)

        # שמירת ההמלצה ל-MongoDB
        ai_collection.insert_one({
            "description": description,
            "analysis": analysis,
            "timestamp": datetime.utcnow()
        })

        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
