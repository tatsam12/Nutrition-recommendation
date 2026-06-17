from pydantic import BaseModel
from typing import Optional


class FoodCreate(BaseModel):
    food_name: str
    category: str
    calories: float
    protein: float = 0
    carbohydrates: float = 0
    fat: float = 0
    fiber: float = 0
    serving_size: str = "100g"
    image_url: Optional[str] = None
    recommended_goal: Optional[str] = None


class FoodUpdate(BaseModel):
    food_name: Optional[str] = None
    category: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    serving_size: Optional[str] = None
    image_url: Optional[str] = None
    recommended_goal: Optional[str] = None


class FoodResponse(BaseModel):
    id: int
    food_name: str
    category: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    fiber: float
    serving_size: str
    image_url: Optional[str]
    recommended_goal: Optional[str]

    model_config = {"from_attributes": True}
