from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch     = "lunch"
    dinner    = "dinner"
    snack     = "snack"


class FoodLog(Base):
    __tablename__ = "food_logs"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    food_id       = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    quantity      = Column(Numeric(6, 2), nullable=False, default=1.0)
    unit          = Column(String(30), nullable=False, default="serving")
    meal_type     = Column(Enum(MealType), nullable=False, default=MealType.snack)
    calories      = Column(Numeric(7, 2), nullable=False)
    protein       = Column(Numeric(6, 2), nullable=False, default=0)
    carbohydrates = Column(Numeric(6, 2), nullable=False, default=0)
    fat           = Column(Numeric(6, 2), nullable=False, default=0)
    fiber         = Column(Numeric(6, 2), nullable=False, default=0)
    logged_at     = Column(Date, nullable=False, server_default=func.current_date())
    created_at    = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="food_logs")
    food = relationship("Food", back_populates="food_logs")
