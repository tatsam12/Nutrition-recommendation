from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.food import FoodResponse


class RecommendationResponse(BaseModel):
    id: int
    food_id: int
    recommendation_type: str
    score: float
    reason: Optional[str]
    generated_at: datetime
    food: Optional[FoodResponse] = None

    model_config = {"from_attributes": True}


class HybridRecommendationResponse(BaseModel):
    foods: list[RecommendationResponse]
    meal_plan: Optional[dict] = None
    category_prediction: Optional[str] = None
    advice: Optional[str] = None
