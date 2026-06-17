from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.food_log import FoodLog
from app.models.nutrition_summary import NutritionSummary
from app.models.food import Food


def get_weekly_calorie_trend(db: Session, user_id: int) -> list[dict]:
    today = date.today()
    result = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        summary = db.query(NutritionSummary).filter(
            NutritionSummary.user_id == user_id,
            NutritionSummary.summary_date == d,
        ).first()
        result.append({
            "date":     d.isoformat(),
            "day":      d.strftime("%a"),
            "calories": float(summary.total_calories) if summary else 0,
            "protein":  float(summary.total_protein) if summary else 0,
            "carbs":    float(summary.total_carbs) if summary else 0,
            "fat":      float(summary.total_fat) if summary else 0,
        })
    return result


def get_macronutrient_distribution(db: Session, user_id: int, target_date: date = None) -> dict:
    target_date = target_date or date.today()
    summary = db.query(NutritionSummary).filter(
        NutritionSummary.user_id == user_id,
        NutritionSummary.summary_date == target_date,
    ).first()
    if not summary:
        return {"protein": 0, "carbohydrates": 0, "fat": 0, "fiber": 0}
    return {
        "protein":       float(summary.total_protein),
        "carbohydrates": float(summary.total_carbs),
        "fat":           float(summary.total_fat),
        "fiber":         float(summary.total_fiber),
    }


def get_food_category_distribution(db: Session, user_id: int, days: int = 7) -> list[dict]:
    start = date.today() - timedelta(days=days)
    rows = (
        db.query(Food.category, func.sum(FoodLog.calories).label("total_cal"))
        .join(Food, Food.id == FoodLog.food_id)
        .filter(FoodLog.user_id == user_id, FoodLog.logged_at >= start)
        .group_by(Food.category)
        .order_by(func.sum(FoodLog.calories).desc())
        .all()
    )
    return [{"category": r.category, "calories": float(r.total_cal)} for r in rows]


def get_monthly_summary(db: Session, user_id: int, year: int, month: int) -> list[dict]:
    from calendar import monthrange
    _, days_in_month = monthrange(year, month)
    result = []
    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        summary = db.query(NutritionSummary).filter(
            NutritionSummary.user_id == user_id,
            NutritionSummary.summary_date == d,
        ).first()
        result.append({
            "date":     d.isoformat(),
            "calories": float(summary.total_calories) if summary else 0,
            "protein":  float(summary.total_protein) if summary else 0,
        })
    return result


def get_recent_food_logs(db: Session, user_id: int, limit: int = 5) -> list:
    from sqlalchemy.orm import joinedload
    return (
        db.query(FoodLog)
        .options(joinedload(FoodLog.food))
        .filter(FoodLog.user_id == user_id)
        .order_by(FoodLog.created_at.desc())
        .limit(limit)
        .all()
    )
