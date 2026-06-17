from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import UserProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate


def _calculate_calorie_goal(profile: UserProfile) -> int:
    """Harris-Benedict BMR * activity multiplier."""
    weight = float(profile.weight_kg)
    height = float(profile.height_cm)
    age    = profile.age

    if profile.gender.value == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    multipliers = {
        "sedentary":         1.2,
        "lightly_active":    1.375,
        "moderately_active": 1.55,
        "very_active":       1.725,
    }
    tdee = bmr * multipliers.get(profile.activity_level.value, 1.2)

    goal_adjustments = {
        "weight_loss": -500,
        "weight_gain": +500,
        "muscle_gain": +300,
        "maintenance": 0,
    }
    return max(1200, int(tdee + goal_adjustments.get(profile.nutrition_goal.value, 0)))


def create_profile(db: Session, user_id: int, data: ProfileCreate) -> UserProfile:
    if db.query(UserProfile).filter(UserProfile.user_id == user_id).first():
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = UserProfile(
        user_id=user_id,
        age=data.age,
        gender=data.gender,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        activity_level=data.activity_level,
        nutrition_goal=data.nutrition_goal,
    )
    if data.daily_calorie_goal:
        profile.daily_calorie_goal = data.daily_calorie_goal
    else:
        profile.daily_calorie_goal = _calculate_calorie_goal(profile)

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, user_id: int) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please complete your profile.")
    return profile


def update_profile(db: Session, user_id: int, data: ProfileUpdate) -> UserProfile:
    profile = get_profile(db, user_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(profile, field, value)
    if not data.daily_calorie_goal:
        profile.daily_calorie_goal = _calculate_calorie_goal(profile)
    db.commit()
    db.refresh(profile)
    return profile
