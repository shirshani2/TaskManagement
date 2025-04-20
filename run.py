from flask import Flask, render_template, send_from_directory
from flask_jwt_extended import JWTManager
from app.auth.routes import auth_bp
from app.tasks.routes import tasks_bp
from app.ai.routes import ai_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def home():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/tasks')
def tasks():
    return render_template("tasks.html")

@app.route('/recommendation')
def recommendation_page():
    return render_template('recommendation.html')



app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)


# רישום של ה-blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
app.register_blueprint(ai_bp, url_prefix='/api/ai')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

