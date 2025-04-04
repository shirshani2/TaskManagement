from flask import Flask, request, jsonify
from db import users_collection


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Task Manager API!"


@app.route('/api/users', methods=['POST'])
def create_user():
    print("🎯 POST התקבל")
    print("Headers:", request.headers)
    print("Raw body:", request.get_data())

    data = request.get_json()
    print("Parsed JSON:", data)

    name = data.get('name') if data else None
    if not name:
        return jsonify({"error": "Name is required"}), 400

    user = {"name": name}
    result = users_collection.insert_one(user)
    return jsonify({"message": "User created", "id": str(result.inserted_id)}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # מחזירים בלי ה-ID
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
