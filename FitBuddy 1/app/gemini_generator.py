import os
from dotenv import load_dotenv
import google.generativeai as genai


# Function to generate workout
def generate_workout_gemini(user_input):
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
        return "Error: API key not found. Please set your GOOGLE_API_KEY in the .env file."

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input.get('goal', '')}**, and prefers **{user_input.get('intensity', '')}** workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
