from flask import Blueprint, request, jsonify
from app.models import users_collection
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import random
import string
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId


auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Name, email, and password are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    verification_code = generate_verification_code()

    user = {
        "name": name,
        "email": email,
        "password": hashed_pw,
        "telegram_verification_code": verification_code 
    }

    result = users_collection.insert_one(user)
    access_token = create_access_token(identity=str(result.inserted_id))

    # ✅ החזרת הטוקן + הקוד
    return jsonify({
        "access_token": access_token,
        "telegram_verification_code": verification_code
    }), 200
    

# 🟢 פונקציית login צריכה להיות בחוץ!
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200


@auth_bp.route('/telegram-code', methods=['GET'])
@jwt_required()
def get_telegram_code():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("telegram_chat_id"):
        return jsonify({"status": "connected"}), 200

    if "telegram_verification_code" in user:
        return jsonify({"telegram_verification_code": user["telegram_verification_code"]}), 200

    return jsonify({"error": "No Telegram code found"}), 404
