from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.food_log import FoodLogCreate, FoodLogResponse, DailyNutritionSummary
from app.services import food_log_service

router = APIRouter(prefix="/food-logs", tags=["Food Logs"])


@router.post("", response_model=FoodLogResponse, status_code=201)
def create_log(
    data: FoodLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return food_log_service.create_food_log(db, current_user.id, data)


@router.get("", response_model=list[FoodLogResponse])
def get_logs(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return food_log_service.get_food_logs(db, current_user.id, start_date, end_date)


@router.get("/today", response_model=list[FoodLogResponse])
def get_today_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return food_log_service.get_today_logs(db, current_user.id)


@router.get("/summary/daily", response_model=DailyNutritionSummary)
def get_daily_summary(
    target_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return food_log_service.get_daily_summary(db, current_user.id, target_date)


@router.delete("/{log_id}", status_code=204)
def delete_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    food_log_service.delete_food_log(db, current_user.id, log_id)
