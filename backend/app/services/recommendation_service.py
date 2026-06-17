from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation, RecommendationType
from app.models.profile import UserProfile
from app.models.food import Food
from app.ml.recommendation_engine import generate_hybrid_recommendations, generate_meal_plan


def get_or_generate_recommendations(db: Session, user_id: int, force: bool = False) -> dict:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Complete your profile first to get recommendations")

    # Check for recent recommendations (within 1 hour)
    if not force:
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
        recent = (
            db.query(Recommendation)
            .filter(
                Recommendation.user_id == user_id,
                Recommendation.recommendation_type == RecommendationType.hybrid,
                Recommendation.generated_at >= cutoff,
            )
            .count()
        )
        if recent >= 5:
            return _load_recommendations(db, user_id)

    # Generate new recommendations
    hybrid_results = generate_hybrid_recommendations(
        db=db,
        user_id=user_id,
        age=profile.age,
        gender=profile.gender.value,
        bmi=profile.bmi,
        activity_level=profile.activity_level.value,
        nutrition_goal=profile.nutrition_goal.value,
        top_n=10,
    )

    # Clear old recommendations
    db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.recommendation_type == RecommendationType.hybrid,
    ).delete()

    # Persist new ones
    for item in hybrid_results:
        food  = item["food"]
        rec_type = RecommendationType.hybrid
        rec = Recommendation(
            user_id=user_id,
            food_id=food.id,
            recommendation_type=rec_type,
            score=item["score"],
            reason=item["reason"],
        )
        db.add(rec)
    db.commit()

    # Generate meal plan
    meal_plan = generate_meal_plan(db, profile.nutrition_goal.value)

    return {
        "recommendations": [
            {
                "food_id": item["food"].id,
                "food":    item["food"],
                "score":   item["score"],
                "reason":  item["reason"],
                "recommendation_type": "hybrid",
            }
            for item in hybrid_results
        ],
        "meal_plan": meal_plan,
        "nutrition_advice": _get_nutrition_advice(profile),
    }


def _load_recommendations(db: Session, user_id: int) -> dict:
    from sqlalchemy.orm import joinedload
    recs = (
        db.query(Recommendation)
        .options(joinedload(Recommendation.food))
        .filter(
            Recommendation.user_id == user_id,
            Recommendation.recommendation_type == RecommendationType.hybrid,
        )
        .order_by(Recommendation.score.desc())
        .limit(10)
        .all()
    )
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    meal_plan = generate_meal_plan(db, profile.nutrition_goal.value) if profile else {}
    return {
        "recommendations": [
            {
                "food_id": r.food_id,
                "food":    r.food,
                "score":   float(r.score),
                "reason":  r.reason,
                "recommendation_type": r.recommendation_type.value,
            }
            for r in recs
        ],
        "meal_plan": meal_plan,
        "nutrition_advice": _get_nutrition_advice(profile) if profile else "",
    }


def _get_nutrition_advice(profile: UserProfile) -> str:
    bmi    = profile.bmi
    goal   = profile.nutrition_goal.value
    advice_map = {
        "weight_loss":  "Focus on high-fiber, low-calorie foods. Eat smaller, frequent meals. "
                        "Include plenty of vegetables and lean proteins like dal and fish.",
        "weight_gain":  "Increase calorie intake with nutrient-dense foods. Include ghee, nuts, "
                        "dairy, and complex carbohydrates like chiura and rice.",
        "muscle_gain":  "Prioritize protein-rich foods like buff meat, chicken, eggs, dal, and "
                        "paneer. Combine with complex carbs for energy.",
        "maintenance":  "Maintain a balanced diet with Dal Bhat, seasonal vegetables, and moderate "
                        "protein. Stay hydrated and avoid processed foods.",
    }
    base  = advice_map.get(goal, "Follow a balanced Nepali diet rich in whole foods.")
    if bmi < 18.5:
        base += " Your BMI indicates underweight — consider increasing caloric intake."
    elif bmi >= 30:
        base += " Your BMI indicates obesity — prioritize low-calorie, high-fiber foods."
    elif bmi >= 25:
        base += " Your BMI is slightly elevated — monitor portion sizes."
    return base
