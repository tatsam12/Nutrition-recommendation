from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.food_log import MealType
from app.schemas.food import FoodResponse


class FoodLogCreate(BaseModel):
    food_id: int
    quantity: float = 1.0
    unit: str = "serving"
    meal_type: MealType = MealType.snack
    logged_at: Optional[date] = None


class FoodLogResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    quantity: float
    unit: str
    meal_type: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    fiber: float
    logged_at: date
    food: Optional[FoodResponse] = None

    model_config = {"from_attributes": True}


class DailyNutritionSummary(BaseModel):
    date: date
    total_calories: float
    total_protein: float
    total_carbohydrates: float
    total_fat: float
    total_fiber: float
    meal_count: int
    calorie_goal: int
    progress_percentage: float
