from typing import Optional
from pydantic import BaseModel, Field


class UserInput(BaseModel):
    """Schema for saving user details and generating workout plan via API."""
    username: str = Field(..., description="Full name or username of the user", examples=["Shreya"])
    user_id: int = Field(..., description="Unique numeric ID for the user", examples=[1])
    age: int = Field(..., ge=10, le=120, description="Age in years", examples=[22])
    weight: float = Field(..., gt=20, le=300, description="Weight in kilograms", examples=[55.0])
    goal: str = Field(..., description="Fitness goal (e.g. weight loss, muscle gain, general wellness)", examples=["muscle gain"])
    intensity: str = Field(..., description="Preferred intensity: low, medium, or high", examples=["high"])


class WorkoutRequest(BaseModel):
    """Schema for requesting a workout plan directly from Gemini Pro."""
    goal: str = Field(..., description="Fitness goal", examples=["muscle gain"])
    intensity: str = Field(..., description="Workout intensity: low, medium, high", examples=["high"])


class FeedbackRequest(BaseModel):
    """Schema for submitting feedback to update an existing plan."""
    feedback: str = Field(..., description="Feedback comments or modifications requested", examples=["Add 15 minutes of yoga and more cardio"])
    user_id: Optional[int] = Field(None, description="Optional user ID if not provided in URL path", examples=[1])


class NutritionTipResponse(BaseModel):
    """Schema for nutrition tip response."""
    goal: str
    nutrition_tip: str


class PlanResponse(BaseModel):
    """Schema for workout plan generation response."""
    message: str
    workout_plan: str


class UpdatePlanResponse(BaseModel):
    """Schema for feedback-updated plan response."""
    updated_plan: str
