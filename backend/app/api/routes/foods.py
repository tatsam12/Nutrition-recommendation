from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.food import FoodCreate, FoodUpdate, FoodResponse
from app.services import food_service

router = APIRouter(prefix="/foods", tags=["Foods"])


@router.get("", response_model=list[FoodResponse])
def list_foods(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return food_service.get_foods(db, skip=skip, limit=limit, category=category)


@router.get("/search", response_model=list[FoodResponse])
def search_foods(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return food_service.search_foods(db, q, limit=limit)


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return food_service.get_food(db, food_id)


@router.post("", response_model=FoodResponse, status_code=201)
def create_food(
    data: FoodCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return food_service.create_food(db, data)


@router.put("/{food_id}", response_model=FoodResponse)
def update_food(
    food_id: int,
    data: FoodUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return food_service.update_food(db, food_id, data)


@router.delete("/{food_id}", status_code=204)
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    food_service.delete_food(db, food_id)
