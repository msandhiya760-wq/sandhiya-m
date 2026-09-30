import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Determine root directory for database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "fitbuddy.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLAlchemy engine & session setup
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(255), nullable=False)
    intensity = Column(String(50), nullable=False)
    schedule = Column(Integer, default=7)

    # Relationship to workout plans
    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="plans")


def init_db():
    """Create all database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency helper to yield database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str) -> User:
    """
    Save or update user details in SQLite database.
    """
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(id=user_id).first()
        if existing:
            existing.name = name
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
            db.commit()
            db.refresh(existing)
            return existing
        else:
            user = User(
                id=user_id,
                name=name,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                schedule=7
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
    finally:
        db.close()


def save_plan(user_id: int, plan: str) -> WorkoutPlan:
    """
    Stores the original workout plan for a user.
    If a plan record already exists for the user, update it; otherwise create a new one.
    """
    db = SessionLocal()
    try:
        existing_plan = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if existing_plan:
            existing_plan.original_plan = plan
            # Reset updated_plan when a fresh plan is generated
            existing_plan.updated_plan = None
            db.commit()
            db.refresh(existing_plan)
            return existing_plan
        else:
            workout = WorkoutPlan(user_id=user_id, original_plan=plan)
            db.add(workout)
            db.commit()
            db.refresh(workout)
            return workout
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str) -> bool:
    """
    Updates the plan based on user feedback.
    """
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if workout:
            workout.updated_plan = updated_text
            db.commit()
            return True
        return False
    finally:
        db.close()


def get_original_plan(user_id: int):
    """
    Fetch the original plan for a user.
    """
    db = SessionLocal()
    try:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        db.close()


def get_user(user_id: int):
    """
    Fetch a user by ID.
    """
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_all_users():
    """
    Fetch all users from the database.
    """
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


def get_all_plans():
    """
    Fetch all workout plans from the database.
    """
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).all()
    finally:
        db.close()


def delete_user(user_id: int) -> bool:
    """
    Delete a user and their associated workout plans.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    finally:
        db.close()
