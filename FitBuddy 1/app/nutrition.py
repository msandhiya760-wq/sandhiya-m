"""
Nutrition and Recovery Logic Module for FitBuddy.
Provides goal-specific macronutrient calculations, hydration targets, and dietary guidelines.
"""
from typing import Dict, Any


def calculate_macronutrients(weight_kg: float, goal: str, intensity: str) -> Dict[str, Any]:
    """
    Calculates estimated daily calories and macronutrient splits based on weight, goal, and intensity.
    """
    goal_lower = goal.lower()
    intensity_lower = intensity.lower()

    # Activity multiplier
    activity_multiplier = 1.35
    if intensity_lower == "high":
        activity_multiplier = 1.6
    elif intensity_lower == "low":
        activity_multiplier = 1.2

    # Baseline BMR estimation (Mifflin-St Jeor rough baseline)
    base_calories = weight_kg * 22 * activity_multiplier

    if "muscle" in goal_lower or "gain" in goal_lower:
        target_calories = round(base_calories + 350)
        protein_g = round(weight_kg * 2.0)
        fat_g = round(weight_kg * 0.9)
        # 4 calories per gram of protein and carb, 9 per gram of fat
        carb_calories = target_calories - (protein_g * 4 + fat_g * 9)
        carbs_g = max(round(carb_calories / 4), 100)
        focus = "Caloric surplus for muscle hypertrophy and strength"
    elif "weight" in goal_lower or "fat" in goal_lower or "loss" in goal_lower:
        target_calories = round(max(base_calories - 450, 1400))
        protein_g = round(weight_kg * 2.2)  # Higher protein during deficit
        fat_g = round(weight_kg * 0.7)
        carb_calories = target_calories - (protein_g * 4 + fat_g * 9)
        carbs_g = max(round(carb_calories / 4), 80)
        focus = "Moderate caloric deficit prioritizing high satiety and lean mass retention"
    else:
        target_calories = round(base_calories)
        protein_g = round(weight_kg * 1.6)
        fat_g = round(weight_kg * 0.8)
        carb_calories = target_calories - (protein_g * 4 + fat_g * 9)
        carbs_g = max(round(carb_calories / 4), 120)
        focus = "Equilibrium maintenance for endurance and overall wellness"

    hydration_liters = round(weight_kg * 0.035, 1)

    return {
        "target_calories": target_calories,
        "protein_grams": protein_g,
        "carbohydrate_grams": carbs_g,
        "fat_grams": fat_g,
        "water_liters": hydration_liters,
        "nutrition_focus": focus
    }


def get_recovery_checklist(intensity: str) -> list:
    """
    Returns tailored recovery recommendations based on workout intensity.
    """
    intensity_lower = intensity.lower()
    base_tips = [
        "Aim for 7 to 9 hours of uninterrupted sleep for cellular repair.",
        "Perform 5-10 minutes of active stretching post-workout.",
        "Maintain steady hydration with essential electrolytes."
    ]

    if intensity_lower == "high":
        base_tips.extend([
            "Consider contrast showers (hot/cold) or foam rolling for delayed onset muscle soreness (DOMS).",
            "Take at least 1-2 dedicated active recovery days weekly."
        ])
    elif intensity_lower == "low":
        base_tips.append("Focus on daily step counts (7,000 - 10,000 steps) for active longevity.")

    return base_tips
