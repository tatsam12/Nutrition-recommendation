from datetime import date
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.food_log import FoodLog
from app.models.food import Food
from app.models.nutrition_summary import NutritionSummary
from app.schemas.food_log import FoodLogCreate, DailyNutritionSummary
from app.services.profile_service import get_profile


def _compute_nutrients(food: Food, quantity: float) -> dict:
    factor = quantity
    return {
        "calories":      round(float(food.calories)      * factor, 2),
        "protein":       round(float(food.protein)       * factor, 2),
        "carbohydrates": round(float(food.carbohydrates) * factor, 2),
        "fat":           round(float(food.fat)           * factor, 2),
        "fiber":         round(float(food.fiber)         * factor, 2),
    }


def _upsert_summary(db: Session, user_id: int, log_date: date) -> None:
    totals = (
        db.query(
            func.sum(FoodLog.calories).label("cal"),
            func.sum(FoodLog.protein).label("prot"),
            func.sum(FoodLog.carbohydrates).label("carbs"),
            func.sum(FoodLog.fat).label("fat"),
            func.sum(FoodLog.fiber).label("fiber"),
            func.count(FoodLog.id).label("cnt"),
        )
        .filter(FoodLog.user_id == user_id, FoodLog.logged_at == log_date)
        .one()
    )
    summary = db.query(NutritionSummary).filter(
        NutritionSummary.user_id == user_id,
        NutritionSummary.summary_date == log_date,
    ).first()

    if summary:
        summary.total_calories = totals.cal or 0
        summary.total_protein  = totals.prot or 0
        summary.total_carbs    = totals.carbs or 0
        summary.total_fat      = totals.fat or 0
        summary.total_fiber    = totals.fiber or 0
        summary.meal_count     = totals.cnt or 0
    else:
        summary = NutritionSummary(
            user_id=user_id,
            summary_date=log_date,
            total_calories=totals.cal or 0,
            total_protein=totals.prot or 0,
            total_carbs=totals.carbs or 0,
            total_fat=totals.fat or 0,
            total_fiber=totals.fiber or 0,
            meal_count=totals.cnt or 0,
        )
        db.add(summary)
    db.commit()


def create_food_log(db: Session, user_id: int, data: FoodLogCreate) -> FoodLog:
    food = db.query(Food).filter(Food.id == data.food_id, Food.is_active == True).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    nutrients  = _compute_nutrients(food, data.quantity)
    log_date   = data.logged_at or date.today()

    log = FoodLog(
        user_id=user_id,
        food_id=data.food_id,
        quantity=data.quantity,
        unit=data.unit,
        meal_type=data.meal_type,
        logged_at=log_date,
        **nutrients,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    _upsert_summary(db, user_id, log_date)
    return log


def get_food_logs(db: Session, user_id: int,
                  start_date: date = None, end_date: date = None) -> List[FoodLog]:
    q = (
        db.query(FoodLog)
        .options(joinedload(FoodLog.food))
        .filter(FoodLog.user_id == user_id)
    )
    if start_date:
        q = q.filter(FoodLog.logged_at >= start_date)
    if end_date:
        q = q.filter(FoodLog.logged_at <= end_date)
    return q.order_by(FoodLog.logged_at.desc(), FoodLog.created_at.desc()).all()


def get_today_logs(db: Session, user_id: int) -> List[FoodLog]:
    return get_food_logs(db, user_id, start_date=date.today(), end_date=date.today())


def delete_food_log(db: Session, user_id: int, log_id: int) -> None:
    log = db.query(FoodLog).filter(FoodLog.id == log_id, FoodLog.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Food log not found")
    log_date = log.logged_at
    db.delete(log)
    db.commit()
    _upsert_summary(db, user_id, log_date)


def get_daily_summary(db: Session, user_id: int, target_date: date = None) -> DailyNutritionSummary:
    target_date = target_date or date.today()
    try:
        profile = get_profile(db, user_id)
        calorie_goal = profile.daily_calorie_goal
    except Exception:
        calorie_goal = 2000

    summary = db.query(NutritionSummary).filter(
        NutritionSummary.user_id == user_id,
        NutritionSummary.summary_date == target_date,
    ).first()

    if not summary:
        return DailyNutritionSummary(
            date=target_date,
            total_calories=0,
            total_protein=0,
            total_carbohydrates=0,
            total_fat=0,
            total_fiber=0,
            meal_count=0,
            calorie_goal=calorie_goal,
            progress_percentage=0.0,
        )

    progress = min(round(float(summary.total_calories) / calorie_goal * 100, 1), 100.0)
    return DailyNutritionSummary(
        date=target_date,
        total_calories=float(summary.total_calories),
        total_protein=float(summary.total_protein),
        total_carbohydrates=float(summary.total_carbs),
        total_fat=float(summary.total_fat),
        total_fiber=float(summary.total_fiber),
        meal_count=summary.meal_count,
        calorie_goal=calorie_goal,
        progress_percentage=progress,
    )
