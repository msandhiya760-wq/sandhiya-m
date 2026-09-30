# FitBuddy – AI Fitness Plan Generator using Gemini Models

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Pro_%26_Flash-4285F4.svg)](https://aistudio.google.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy_2.0-D71F00.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/pytest-Passing-brightgreen.svg)](https://docs.pytest.org/)

FitBuddy is an intelligent, full-stack web application that uses Google’s Gemini generative AI models to generate personalized 7-day workout plans and tailored nutrition/recovery tips based on user goals, age, weight, and workout intensity. FitBuddy also provides a dynamic feedback loop that enables users to revise and adapt their workout routines, as well as an administrative dashboard for trainers and coaches to track user plans.

---

## 🏗️ Architecture Overview

```
                               ┌────────────────────────┐
                               │   User Web Browser     │
                               │ (HTML5 / CSS / Jinja2) │
                               └───────────┬────────────┘
                                           │ HTTP Requests (GET / POST)
                                           ▼
                               ┌────────────────────────┐
                               │     FastAPI Server     │
                               │     (app/main.py)      │
                               └───────────┬────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
        ┌──────────────────────┐ ┌──────────────────┐  ┌──────────────────────┐
        │   HTML Templating    │ │  Workouts & Tips │  │   Admin Dashboard    │
        │  (templates/*.html)  │ │ (app/routes.py)  │  │   /view-all-users    │
        └──────────────────────┘ └─────────┬────────┘  └──────────────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
           ┌────────────────────────┐            ┌────────────────────────┐
           │     Gemini 1.5 Pro     │            │      Gemini Flash      │
           │  (7-Day Plan & Updates)│            │(Fast Nutrition & Tips) │
           │  gemini_generator.py   │            │gemini_flash_generator.py│
           │    updated_plan.py     │            └────────────────────────┘
           └────────────────────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │ SQLite + SQLAlchemy ORM│
           │     (fitbuddy.db)      │
           │  - User Table          │
           │  - WorkoutPlan Table   │
           └────────────────────────┘
```

---

## 📁 Project Directory Structure

```text
FitBuddy/
│
├── app/
│   ├── __init__.py               # Python package initialization
│   ├── main.py                   # FastAPI application entry point & lifespan
│   ├── routes.py                 # Core routing (Jinja2 HTML views + REST APIs)
│   ├── database.py               # SQLAlchemy models (User, WorkoutPlan) & DB CRUD
│   ├── schemas.py                # Pydantic schemas for data validation
│   ├── gemini_generator.py       # Gemini 1.5 Pro - 7-day workout generator
│   ├── gemini_flash_generator.py # Gemini Flash - quick nutrition/recovery tips
│   ├── updated_plan.py           # Feedback-driven workout updater
│   └── nutrition.py              # Macro calculations & recovery logic
│
├── templates/
│   ├── index.html                # User input form (Home Page)
│   ├── result.html               # Plan display, nutrition tip & feedback form
│   └── all_users.html            # Admin dashboard with plans and management
│
├── static/
│   └── images/
│       └── gym-bg.jpg            # High-resolution gym background image
│
├── fitbuddy.db                   # SQLite database (auto-generated)
├── requirements.txt              # Project dependencies
├── .env.example                  # Environment template for Gemini API key
├── .env                          # Local environment configuration
├── seed_db.py                    # Database seeder with demo sample records
├── test_app.py                   # Automated test suite (Pytest)
├── run.py                        # Quick runner script
└── README.md                     # Comprehensive project documentation
```

---

## 🛠️ VS Code Setup & Installation Guide

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File** > **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the `FitBuddy` project folder.

### Step 2: Install Recommended Extensions
Open the Extensions view (`Ctrl + Shift + X`) and install:
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- **SQLite Viewer** (by Florian Klampfer) – optional, to inspect `fitbuddy.db` directly in VS Code.

### Step 3: Create & Activate Virtual Environment
Open the integrated terminal in VS Code (`Ctrl + ~` or **Terminal** > **New Terminal**):

```powershell
# In PowerShell (Windows):
python -m venv fitbuddy-env
fitbuddy-env\Scripts\activate
```

*(On macOS/Linux: `python3 -m venv fitbuddy-env && source fitbuddy-env/bin/activate`)*

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Google Gemini API Key
1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. Open the `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=AIzaSy...your_gemini_api_key_here
   ```
*(Note: Ensure you add a valid Gemini API key to your .env file so the Gemini models can generate your workout plans and nutrition tips).*

### Step 6: (Optional) Seed the Database with Sample Data
Populate the database with a pre-configured demo user (`shreya`) matching the project documentation:
```bash
python seed_db.py
```

---

## 🚀 Running the Application

### Option A: Using the Launcher Script (Recommended)
```bash
python run.py
```

### Option B: Using Uvicorn Directly
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once started, access the following in your web browser:

| Interface | URL | Description |
| :--- | :--- | :--- |
| **Home Page** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | Form to input user details and generate 7-day workout |
| **Admin Dashboard** | [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users) | View all users, original & updated plans, delete records |
| **Interactive API Docs** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Swagger UI for testing REST API endpoints |
| **ReDoc Documentation** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | Alternative OpenAPI specifications view |

---

## 🧪 Testing the Application

### 1. Automated Test Suite (Pytest)
Run the full test suite covering database operations, AI generators, template rendering, and REST endpoints:
```bash
pytest test_app.py -v
```

### 2. Manual Testing Workflow
1. Navigate to `http://127.0.0.1:8000/`.
2. Fill out the form:
   - **Name**: `Alex Parker`
   - **User ID**: `202`
   - **Age**: `26`
   - **Weight**: `74.5`
   - **Fitness Goal**: `muscle gain`
   - **Intensity**: `High`
3. Click **Generate Plan**. The app calls Gemini 1.5 Pro & Flash, saves the data to `fitbuddy.db`, and navigates to the result page.
4. On the result page, scroll down to **Share Your Feedback**:
   - Enter `Add 15 minutes of yoga and increase cardio on Day 3`.
   - Click **Submit Feedback**.
   - Notice the green confirmation alert: `"✅ Your plan has been updated based on your feedback!"`.
5. Click **View All Users (Admin)** or go to `http://127.0.0.1:8000/view-all-users` to inspect the side-by-side original and updated plans.

### 3. REST API Testing via cURL

**Generate Workout (Direct API):**
```bash
curl -X POST "http://127.0.0.1:8000/generate-workout/gemini" \
     -H "Content-Type: application/json" \
     -d "{\"goal\": \"weight loss\", \"intensity\": \"high\"}"
```

**Fetch Nutrition Tip:**
```bash
curl -X GET "http://127.0.0.1:8000/nutrition-tip?goal=muscle%20gain"
```

**Save User & Generate Plan:**
```bash
curl -X POST "http://127.0.0.1:8000/generate-plan" \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"David\", \"user_id\": 301, \"age\": 29, \"weight\": 82.0, \"goal\": \"strength\", \"intensity\": \"high\"}"
```

**Submit Feedback Update:**
```bash
curl -X POST "http://127.0.0.1:8000/update-plan/301" \
     -H "Content-Type: application/json" \
     -d "{\"feedback\": \"Add core exercises on Day 2 and Day 4\"}"
```

---

## 📋 Technology Stack Summary

- **Backend Web Framework**: FastAPI (0.110+)
- **ASGI Server**: Uvicorn
- **AI / LLM Layer**: Google Generative AI SDK (`gemini-1.5-pro` and `gemini-1.5-flash`)
- **Database & ORM**: SQLite with SQLAlchemy 2.0
- **Templating Engine**: Jinja2 with HTML5 & modern CSS3 (Flexbox/Grid, Roboto typography)
- **Testing**: Pytest & Starlette TestClient
