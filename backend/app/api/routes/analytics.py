from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/weekly-trend")
def weekly_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics_service.get_weekly_calorie_trend(db, current_user.id)


@router.get("/macros")
def macros(
    target_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics_service.get_macronutrient_distribution(db, current_user.id, target_date)


@router.get("/category-distribution")
def category_dist(
    days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics_service.get_food_category_distribution(db, current_user.id, days)


@router.get("/monthly")
def monthly_summary(
    year:  int = Query(..., ge=2020, le=2100),
    month: int = Query(..., ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics_service.get_monthly_summary(db, current_user.id, year, month)


@router.get("/recent-logs")
def recent_logs(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.schemas.food_log import FoodLogResponse
    logs = analytics_service.get_recent_food_logs(db, current_user.id, limit)
    return [FoodLogResponse.model_validate(log) for log in logs]
