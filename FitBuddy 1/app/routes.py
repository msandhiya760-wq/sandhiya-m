import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    SessionLocal, User, WorkoutPlan,
    save_user, save_plan, update_plan,
    get_original_plan, get_user, delete_user
)
from app.schemas import UserInput, WorkoutRequest, FeedbackRequest, NutritionTipResponse, PlanResponse, UpdatePlanResponse
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

# Set up templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

router = APIRouter()


def is_api_key_configured() -> bool:
    """Helper to check whether a non-empty, non-placeholder Google API key is set."""
    load_dotenv(override=True)
    key = os.getenv("GOOGLE_API_KEY")
    return bool(key and key.strip() and key.strip() != "your_gemini_api_key_here")


# ---------------------------------------------------------------------------
# Frontend Web Routes (Jinja2 HTML Templates)
# ---------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Renders the homepage form (index.html) for user input.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"has_api_key": is_api_key_configured()}
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_form(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    """
    Receives user input from index.html form:
    1. Generates 7-day workout plan via Gemini 1.5 Pro
    2. Generates nutrition tip via Gemini Flash
    3. Saves user details & workout plan in SQLite database
    4. Renders result.html
    """
    user_dict = {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity
    }

    # Generate AI content using Gemini models
    workout_plan = generate_workout_gemini(user_dict)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Persist in Database
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )
    save_plan(user_id=user_id, plan=workout_plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "has_api_key": is_api_key_configured()
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback_form(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    """
    Updates an existing workout plan based on user feedback:
    1. Retrieves original plan from database
    2. Uses Gemini 1.5 Pro to revise plan
    3. Stores updated plan in database
    4. Renders result.html with updated plan and confirmation message
    """
    original_plan = get_original_plan(user_id)
    user = get_user(user_id)

    if not original_plan or not user:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user.name if user else "User",
                "user_id": user_id,
                "age": user.age if user else 25,
                "weight": user.weight if user else 70.0,
                "goal": user.goal if user else "General Fitness",
                "intensity": user.intensity if user else "Medium",
                "workout_plan": "Original plan not found for this user.",
                "nutrition_tip": "",
                "updated_message": "⚠️ Original plan not found for this user ID.",
                "has_api_key": is_api_key_configured()
            }
        )

    # Revise plan using Gemini Pro
    updated_plan_text = update_workout_plan(original_plan, feedback)
    update_plan(user_id, updated_plan_text)

    # Refresh nutrition tip
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated_plan_text,
            "nutrition_tip": nutrition_tip,
            "updated_message": "Your plan has been updated based on your feedback!",
            "has_api_key": is_api_key_configured()
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    """
    Admin View of All Users:
    Displays a list of all registered users and their original & updated workout plans in a structured table.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        user_data = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            user_data.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
            })
        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={"users": user_data}
        )
    finally:
        db.close()


@router.post("/delete-user/{user_id}", response_class=HTMLResponse)
def delete_user_action(request: Request, user_id: int):
    """
    Deletes a user and their plans from the database, then redirects back to /view-all-users.
    """
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)


# ---------------------------------------------------------------------------
# REST API Endpoints (Swagger /docs compatible)
# ---------------------------------------------------------------------------

@router.get("/api/check-api-key", tags=["API Endpoints"])
def check_api_key_status():
    """
    Check if a valid GOOGLE_API_KEY is configured in the environment.
    """
    return {"configured": is_api_key_configured()}


@router.post("/generate-workout/gemini", tags=["API Endpoints"])
async def generate_gemini_workout(request: WorkoutRequest):
    """
    # 1. API: Generate workout using Gemini Pro
    """
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip", response_model=NutritionTipResponse, tags=["API Endpoints"])
def get_flash_tip(goal: str):
    """
    # 2. API: Generate nutrition tip using Gemini Flash
    """
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


@router.post("/generate-plan", response_model=PlanResponse, tags=["API Endpoints"])
def generate_plan(user_data: UserInput):
    """
    # 3. API: Save user info & generate plan
    """
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity,
            "username": user_data.username
        })
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}", response_model=UpdatePlanResponse, tags=["API Endpoints"])
def update_user_plan(user_id: int, data: FeedbackRequest):
    """
    # 4. API: Update workout plan based on user feedback
    """
    original = get_original_plan(user_id)
    if not original:
        raise HTTPException(status_code=404, detail="Original plan not found for this user.")
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}


@router.get("/api/users", tags=["API Endpoints"])
def get_all_users_api():
    """
    API: Returns list of all users and their workout plans.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        results = []
        for u in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).first()
            results.append({
                "id": u.id,
                "name": u.name,
                "age": u.age,
                "weight": u.weight,
                "goal": u.goal,
                "intensity": u.intensity,
                "original_plan": plan.original_plan if plan else None,
                "updated_plan": plan.updated_plan if plan else None
            })
        return results
    finally:
        db.close()
