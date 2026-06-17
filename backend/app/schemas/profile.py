from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.profile import ActivityLevel, NutritionGoal, Gender


class ProfileCreate(BaseModel):
    age: int
    gender: Gender
    height_cm: float
    weight_kg: float
    activity_level: ActivityLevel
    nutrition_goal: NutritionGoal
    daily_calorie_goal: Optional[int] = None

    @field_validator("age")
    @classmethod
    def valid_age(cls, v: int) -> int:
        if not (1 <= v <= 120):
            raise ValueError("Age must be between 1 and 120")
        return v

    @field_validator("height_cm")
    @classmethod
    def valid_height(cls, v: float) -> float:
        if not (50 <= v <= 300):
            raise ValueError("Height must be between 50 and 300 cm")
        return v

    @field_validator("weight_kg")
    @classmethod
    def valid_weight(cls, v: float) -> float:
        if not (10 <= v <= 500):
            raise ValueError("Weight must be between 10 and 500 kg")
        return v


class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    nutrition_goal: Optional[NutritionGoal] = None
    daily_calorie_goal: Optional[int] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    bmi: float
    bmi_category: str
    activity_level: str
    nutrition_goal: str
    daily_calorie_goal: int

    model_config = {"from_attributes": True}
