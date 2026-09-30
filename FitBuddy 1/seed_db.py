"""
Database seeder for FitBuddy
Initializes the database with sample demo data matching the project documentation.
"""
from app.database import init_db, save_user, save_plan, update_plan, SessionLocal, User


def seed():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(id=1).first()
        if not existing:
            save_user(
                user_id=1,
                name="shreya",
                age=22,
                weight=55.0,
                goal="muscle gain",
                intensity="high"
            )
            original_plan = """**7-Day Muscle Gain Workout Plan (High Intensity)**

This plan focuses on compound exercises to maximize muscle growth and utilizes a push-pull-legs split with rest days strategically placed for optimal recovery.

**Day 1: Upper Body Push**
* Warm-up (5-10 mins): Arm circles, shoulder rotations, push-ups.
* Main Workout:
  - Bench Press: 3 sets of 8-12 reps
  - Incline Dumbbell Press: 3 sets of 8-12 reps
  - Overhead Press: 3 sets of 8-12 reps
  - Triceps Pushdown: 3 sets of 10-15 reps
  - Lateral Raises: 3 sets of 12-15 reps
* Cooldown: Static stretching focusing on chest, shoulders, and triceps (30 seconds each).

**Day 2: Lower Body (Legs & Core)**
* Warm-up (5-10 mins): Bodyweight squats, lunges, glute bridges.
* Main Workout:
  - Barbell Squats: 4 sets of 8-10 reps
  - Romanian Deadlifts: 3 sets of 10-12 reps
  - Walking Lunges: 3 sets of 12 reps per leg
  - Standing Calf Raises: 3 sets of 15-20 reps
  - Hanging Leg Raises: 3 sets to failure
* Cooldown: Hamstring and quad stretches.

**Day 3: Rest or Active Recovery**
* Active Recovery: 30 minutes light walking, mobility, and foam rolling.

**Day 4: Upper Body Pull**
* Warm-up (5 mins): Band pull-aparts, light cardio.
* Main Workout:
  - Pull-ups / Lat Pulldowns: 4 sets of 8-10 reps
  - Bent-over Barbell Rows: 3 sets of 8-10 reps
  - Seated Cable Rows: 3 sets of 10-12 reps
  - Barbell Bicep Curls: 3 sets of 10-12 reps
  - Hammer Curls: 3 sets of 12 reps
* Cooldown: Upper back and bicep static stretches.

**Day 5: Lower Body Power & Core**
* Warm-up (5 mins): Dynamic leg stretches.
* Main Workout:
  - Leg Press: 3 sets of 10-12 reps
  - Leg Curls: 3 sets of 12 reps
  - Bulgarian Split Squats: 3 sets of 10 reps/leg
  - Planks: 3 sets of 60 seconds
* Cooldown: Hip flexor and quad stretches.

**Day 6: Full Body Hypertrophy & Conditioning**
* Warm-up (5 mins): Jumping jacks, arm circles.
* Main Workout:
  - Dumbbell Thrusters: 3 sets of 12 reps
  - Kettlebell Swings: 3 sets of 15 reps
  - Dips: 3 sets of 10-12 reps
  - Chin-ups: 3 sets of 8-10 reps
* Cooldown: 10 mins full-body cooldown.

**Day 7: Rest & Nutrition Focus**
* Full rest day, high protein intake, 8+ hours sleep."""

            save_plan(user_id=1, plan=original_plan)

            updated_plan = """**7-Day Muscle Gain Workout Plan (High Intensity - Updated with Yoga & Cardio)**

Key Modifications Made:
- Integrated user feedback: "Include 15 minutes of yoga and 20 mins cardio".
- Day 3 and Day 7 enhanced with Vinyasa yoga and low-impact steady state cardio.

**Day 1: Upper Body Push**
* Warm-up: 5-10 mins arm circles, dynamic chest openers.
* Main Workout: Bench Press (3x8-12), Incline Press (3x8-12), Overhead Press (3x8-12), Lateral Raises (3x12-15).
* Cooldown: Static chest and shoulder stretch.

**Day 2: Lower Body (Legs & Core)**
* Warm-up: Air squats, hip openers.
* Main Workout: Barbell Squats (4x8-10), RDLs (3x10-12), Lunges (3x12), Calf Raises (3x15-20).
* Cooldown: Hamstring stretch.

**Day 3: Yoga & Recovery Cardio [UPDATED]**
* 15 minutes morning Vinyasa yoga flow for spinal mobility and hip flexibility.
* 20 minutes Zone 2 cardio (incline treadmill walk).

**Day 4: Upper Body Pull**
* Main Workout: Pull-ups (4x8-10), Barbell Rows (3x8-10), Cable Rows (3x10-12), Bicep Curls (3x10-12).
* Cooldown: 5 minutes bicep and lat stretches.

**Day 5: Lower Body & Abs**
* Main Workout: Leg Press (3x10-12), Leg Curls (3x12), Split Squats (3x10), Planks (3x60s).

**Day 6: Full Body Hypertrophy**
* Main Workout: Dumbbell Thrusters (3x12), Kettlebell Swings (3x15), Dips (3x10-12).

**Day 7: Rest, Yoga & Nutrition [UPDATED]**
* 15 minutes gentle restorative yoga and full relaxation."""

            update_plan(user_id=1, updated_text=updated_plan)
            print("Successfully seeded sample user 'shreya' (ID: 1) with original and updated workout plans.")
        else:
            print("Database already contains seed data.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
