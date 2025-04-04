from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.auth.routes import auth_bp
from app.tasks.routes import tasks_bp

app = Flask(__name__)

# הגדרות JWT
app.config['JWT_SECRET_KEY'] = 'supersecretjwtkey'  # שימי משהו חזק וייחודי
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

# הגדרת CORS
CORS(app)

# רישום של ה-blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

if __name__ == "__main__":
    app.run(debug=True)
