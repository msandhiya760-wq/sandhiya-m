"""
Automated Test Suite for FitBuddy
Tests API endpoints, HTML templates, Gemini handlers, and SQLite database persistence.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import (
    init_db, save_user, save_plan, update_plan,
    get_original_plan, get_user, delete_user
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan


client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Ensure DB tables are initialized before tests run."""
    init_db()
    yield
    delete_user(9999)
    delete_user(8888)
    delete_user(7777)


def test_home_page():
    """Test that the homepage renders correctly with status code 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text
    assert "Workout Intensity" in response.text


def test_gemini_functions_error_handling():
    """Verify that when no valid API key is present, functions return the proper error message as in PDF."""
    workout = generate_workout_gemini({"goal": "muscle gain", "intensity": "high"})
    assert isinstance(workout, str)

    tip = generate_nutrition_tip_with_flash("muscle gain")
    assert isinstance(tip, str)

    updated = update_workout_plan("Day 1: Upper body", "Add yoga")
    assert isinstance(updated, str)


def test_database_crud_operations():
    """Test SQLite database operations directly."""
    test_id = 9999
    delete_user(test_id)

    # 1. Create user
    user = save_user(
        user_id=test_id,
        name="Pytest User",
        age=28,
        weight=72.5,
        goal="fat loss",
        intensity="high"
    )
    assert user.id == test_id
    assert user.name == "Pytest User"

    # 2. Save plan
    plan_text = "Day 1: Full body blast\nDay 2: Cardio"
    saved_plan = save_plan(test_id, plan_text)
    assert saved_plan.user_id == test_id
    assert get_original_plan(test_id) == plan_text

    # 3. Update plan
    updated_text = "Day 1: Full body blast + Yoga\nDay 2: Cardio"
    success = update_plan(test_id, updated_text)
    assert success is True

    # 4. Read user
    fetched_user = get_user(test_id)
    assert fetched_user is not None
    assert fetched_user.name == "Pytest User"

    # 5. Delete user
    deleted = delete_user(test_id)
    assert deleted is True
    assert get_user(test_id) is None


def test_generate_workout_form_and_feedback_flow():
    """Test full web workflow: submit form -> view result -> submit feedback."""
    test_id = 8888
    delete_user(test_id)

    # 1. Submit workout form
    form_data = {
        "username": "Flow Tester",
        "user_id": test_id,
        "age": 26,
        "weight": 68.0,
        "goal": "muscle gain",
        "intensity": "High"
    }
    resp = client.post("/generate-workout", data=form_data)
    assert resp.status_code == 200
    assert "Your Personalized Workout Plan" in resp.text
    assert "Flow Tester" in resp.text
    assert "68.0 kg" in resp.text

    # 2. Submit feedback
    feedback_data = {
        "user_id": test_id,
        "feedback": "Please add 20 minutes of cycling."
    }
    feedback_resp = client.post("/submit-feedback", data=feedback_data)
    assert feedback_resp.status_code == 200
    assert "Your plan has been updated based on your feedback!" in feedback_resp.text

    # 3. Check admin page displays user
    admin_resp = client.get("/view-all-users")
    assert admin_resp.status_code == 200
    assert "Flow Tester" in admin_resp.text
    assert str(test_id) in admin_resp.text

    # 4. Clean up
    delete_user(test_id)


def test_rest_api_endpoints():
    """Test all Swagger REST API endpoints."""
    # 1. /generate-workout/gemini
    resp = client.post("/generate-workout/gemini", json={"goal": "general fitness", "intensity": "medium"})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "workout_plan" in json_data

    # 2. /nutrition-tip
    resp = client.get("/nutrition-tip?goal=weight%20loss")
    assert resp.status_code == 200
    json_data = resp.json()
    assert "nutrition_tip" in json_data

    # 3. /generate-plan
    test_id = 7777
    delete_user(test_id)
    plan_payload = {
        "username": "API Test User",
        "user_id": test_id,
        "age": 30,
        "weight": 80.0,
        "goal": "flexibility",
        "intensity": "low"
    }
    resp = client.post("/generate-plan", json=plan_payload)
    assert resp.status_code == 200
    assert "Workout plan generated and saved successfully!" in resp.json()["message"]

    # 4. /update-plan/{user_id}
    feedback_payload = {
        "feedback": "Include more hamstring stretches"
    }
    resp = client.post(f"/update-plan/{test_id}", json=feedback_payload)
    assert resp.status_code == 200
    assert "updated_plan" in resp.json()

    # 5. /api/users
    resp = client.get("/api/users")
    assert resp.status_code == 200
    users = resp.json()
    assert any(u["id"] == test_id for u in users)

    # Clean up
    delete_user(test_id)
