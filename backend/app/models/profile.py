from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class ActivityLevel(str, enum.Enum):
    sedentary         = "sedentary"
    lightly_active    = "lightly_active"
    moderately_active = "moderately_active"
    very_active       = "very_active"


class NutritionGoal(str, enum.Enum):
    weight_loss  = "weight_loss"
    weight_gain  = "weight_gain"
    muscle_gain  = "muscle_gain"
    maintenance  = "maintenance"


class Gender(str, enum.Enum):
    male   = "male"
    female = "female"
    other  = "other"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                                 unique=True, nullable=False, index=True)
    age                 = Column(Integer, nullable=False)
    gender              = Column(Enum(Gender), nullable=False)
    height_cm           = Column(Numeric(5, 2), nullable=False)
    weight_kg           = Column(Numeric(5, 2), nullable=False)
    activity_level      = Column(Enum(ActivityLevel), nullable=False)
    nutrition_goal      = Column(Enum(NutritionGoal), nullable=False)
    daily_calorie_goal  = Column(Integer, nullable=False, default=2000)
    created_at          = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at          = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="profile")

    @property
    def bmi(self) -> float:
        h = float(self.height_cm) / 100
        return round(float(self.weight_kg) / (h * h), 2)

    @property
    def bmi_category(self) -> str:
        b = self.bmi
        if b < 16:    return "Severe Thinness"
        if b < 17:    return "Moderate Thinness"
        if b < 18.5:  return "Mild Thinness"
        if b < 25:    return "Normal Weight"
        if b < 27.5:  return "Pre-Obese"
        if b < 30:    return "Overweight"
        if b < 35:    return "Obese Class I"
        if b < 40:    return "Obese Class II"
        return "Obese Class III"
