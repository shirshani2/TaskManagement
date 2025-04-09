# 🧠 Task Management API with AI-Powered Insights

This is a full-stack task management application built with **Flask**, **MongoDB**, and **HTML/CSS/JS**.  
It includes **AI features using OpenAI's API** and **Telegram integration** for smart notifications.

> this project demonstrates backend and frontend development, RESTful API design, AI integration, and Docker support.

---

## ⚙️ Setup Instructions

### 🧪 Option 1: Run locally (without Docker)

1. **Clone the repository**  
```bash
git clone https://github.com/shirshani2/TaskManagement.git
cd TaskManagement
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the root directory:
```
MONGO_URI=your_mongo_uri
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
```

5. **Run the app**
```bash
flask run
```

6. **Run the Telegram bot**

In a separate terminal window, run the Telegram bot:

```bash
python -m app.telegram.telegram_bot

Then open your browser at: [http://localhost:5000](http://localhost:5000)

---

### 🐳 Option 2: Run with Docker

1. **Install Docker**: https://www.docker.com/products/docker-desktop

2. **Clone the repository**
```bash
git clone https://github.com/shirshani2/TaskManagement.git
cd TaskManagement
```

3. **Create a `.env` file** (same as above)

4. **Run the app**
```bash
docker-compose up --build
```
This will run both the Flask API and the Telegram bot in separate containers

Visit: [http://localhost:5001](http://localhost:5001)

---

## 📡 Updated API Documentation (Based on Your Real Code)

### 🔐 Auth

| Method | Endpoint                 | Description                                                                 | Requires Auth |
|--------|--------------------------|-----------------------------------------------------------------------------|----------------|
| POST   | `/api/auth/register`     | Register user + return JWT + Telegram verification code                     | ❌              |
| POST   | `/api/auth/login`        | Login with email/password → returns JWT                                     | ❌              |
| GET    | `/api/auth/telegram-code`| Get your Telegram verification code or connection status                    | ✅              |

---

### ✅ Tasks

| Method | Endpoint                  | Description                                      | Requires Auth |
|--------|---------------------------|--------------------------------------------------|----------------|
| GET    | `/api/tasks`              | Get all tasks for current user                  | ✅              |
| POST   | `/api/tasks`              | Create a new task                               | ✅              |
| GET    | `/api/tasks/<task_id>`    | Get specific task by ID                         | ✅              |
| PUT    | `/api/tasks/<task_id>`    | Update a task by ID                             | ✅              |
| DELETE | `/api/tasks/<task_id>`    | Delete a task by ID                             | ✅              |

---

### 🤖 AI Integration

| Method | Endpoint               | Description                                                                 | Requires Auth |
|--------|------------------------|-----------------------------------------------------------------------------|----------------|
| POST   | `/api/ai/recommend`    | Generate a smart time management recommendation based on **all tasks**     | ✅              |

> 📌 This endpoint is inspired by *Atomic Habits* and gives free-text advice.  
> It doesn’t save anything in the database.

---

### 📬 Telegram Integration

| Source | Description                                                                 |
|--------|-----------------------------------------------------------------------------|
| **GET `/api/auth/telegram-code`** | Returns the user's Telegram verification code (see above) |
| **Telegram bot command** `/start` | Starts the verification process via Telegram             |
| **Message with code**            | Automatically links Telegram to your account              |
| **Telegram bot command** `/summary` | Sends AI-generated weekly summary of open tasks        |
| **Background job** (scheduler)  | Sends summaries every Sunday at 10:31 (via `telegram_bot.py`) |

> ✅ All Telegram alerts (task added/completed) are triggered automatically via backend logic using `send_telegram_message(...)`


---

## ✅ Features Implemented 

### 🔐 Authentication & Authorization
- User registration with name, email, and password
- Passwords securely hashed using bcrypt
- JWT token generation upon login
- All sensitive routes are protected using `@jwt_required()`
- User identity is extracted via `get_jwt_identity()` to ensure data isolation and ownership
- Each user can access only their own tasks based on their token

---

### ✅ Task Management
- Full CRUD operations for tasks (Create, Read, Update, Delete)
- Each task is tied to a specific user (`user_id`)
- Tasks include a `status` field (e.g., `"open"`) to support filtering and summaries
- Secure task access using `ObjectId` and per-user query filtering

---

### 🤖 AI Integration (OpenAI)
- AI generates personalized time management advice based on all user tasks
- Prompts are dynamically built from task titles and descriptions
- Output is helpful, motivational, and inspired by *Atomic Habits*
- AI summaries are used both in frontend and in Telegram weekly updates

---

### 📬 Telegram Bot Integration
- Telegram bot built using `telebot` listens to messages
- Verification code is generated at registration and linked via chat
- `/summary` command provides weekly AI-generated summary of open tasks
- Weekly automatic summary is sent every Sunday at 10:31 using `APScheduler`
- Real-time Telegram messages sent upon task creation or completion
- Bot responses and interface are written in Hebrew for localized experience

---

### 🌐 Frontend (HTML/CSS/JavaScript)
- Registration and login forms using vanilla JS
- Task dashboard allows adding, completing, and deleting tasks
- API requests sent via `fetch` and authorized using saved JWT
- JWT stored in `localStorage` to persist sessions
- Clean and minimal user interface for task management

---

### 🔒 Security & Configuration
- All API keys and secrets are stored in `.env` file and never hardcoded
- Secrets loaded using `python-dotenv` (`os.getenv(...)`)
- CORS configured via `flask-cors` to enable secure communication between frontend and backend
- Authentication protected via JWT with token-based authorization
- All user-related queries filtered explicitly by authenticated user

---

### 🐳 Docker & Environment Setup
- `Dockerfile` for containerizing Flask application
- `docker-compose.yml` for simplified development and deployment
- Environment variable support with `.env` files for all config values
- Clear separation between code and environment configuration

---

### 🧼 Project Structure & Code Quality
- Code organized using Flask Blueprints: `auth`, `tasks`, `ai`, `telegram`
- External service logic abstracted into utility modules (`openai_utils`, `telegram_utils`)
- Modular structure allows easy expansion and separation of concerns
- MongoDB queries are explicit, efficient, and secured

---

### 🇮🇱 Localization
- Telegram bot fully supports Hebrew language
- All bot messages are intuitive and accessible for Israeli users





## 🎨 Design Decisions 

These are the most meaningful implementation choices I made throughout the project — beyond what's written in the assignment.

---

### 🧩 Blueprint Architecture
I split the app into Blueprints (`auth`, `tasks`, `ai`, `telegram`) early on to keep things modular and maintainable. It allowed me to focus on one domain at a time and avoid spaghetti code.

---

### 🧠 AI Recommendation Reimagined
Instead of returning a category/time per task, I built a system that analyzes the full task list and generates holistic productivity advice. This made the AI genuinely useful.

---

### 📬 Telegram as an Interface
I didn’t stop at notifications — I made Telegram a second UI. It includes account linking, `/summary` command, and weekly smart summaries, all in Hebrew.

---

### 📦 Dockerized Only at the End
I avoided Docker at first to focus on learning Flask and MongoDB. Once the app worked locally, I added containerization for reproducibility and clarity.

---

### 🔄 Utility-Driven Logic
To keep routes clean, I offloaded external logic (OpenAI, Telegram) into dedicated files. This separation helped me focus each part and made the code easy to debug and expand.

---

### 🔐 Scoped Security
I didn’t just secure routes — I scoped every DB query using `get_jwt_identity()`, ensuring users only access their own data. No shortcuts.

---

