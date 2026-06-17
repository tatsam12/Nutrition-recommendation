from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id                = Column(Integer, primary_key=True, index=True)
    user_id           = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                               nullable=False, index=True)
    plan_date         = Column(Date, nullable=False)
    breakfast_food_id = Column(Integer, ForeignKey("foods.id", ondelete="SET NULL"), nullable=True)
    lunch_food_id     = Column(Integer, ForeignKey("foods.id", ondelete="SET NULL"), nullable=True)
    dinner_food_id    = Column(Integer, ForeignKey("foods.id", ondelete="SET NULL"), nullable=True)
    snack_food_id     = Column(Integer, ForeignKey("foods.id", ondelete="SET NULL"), nullable=True)
    total_calories    = Column(Numeric(7, 2), nullable=False, default=0)
    nutrition_goal    = Column(String(50), nullable=True)
    created_at        = Column(DateTime, server_default=func.now(), nullable=False)

    user      = relationship("User", back_populates="meal_plans")
    breakfast = relationship("Food", foreign_keys=[breakfast_food_id])
    lunch     = relationship("Food", foreign_keys=[lunch_food_id])
    dinner    = relationship("Food", foreign_keys=[dinner_food_id])
    snack     = relationship("Food", foreign_keys=[snack_food_id])
