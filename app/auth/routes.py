from flask import Blueprint, request, jsonify
from app.models import users_collection
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import random
import string

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

    return jsonify({
        "message": "User registered",
        "id": str(result.inserted_id),
        "telegram_verification_code": verification_code  
    }), 201

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
