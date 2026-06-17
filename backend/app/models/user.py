from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    full_name  = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, index=True, nullable=False)
    password   = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    profile         = relationship("UserProfile", back_populates="user", uselist=False,
                                   cascade="all, delete-orphan")
    food_logs       = relationship("FoodLog", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    meal_plans      = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens  = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    nutrition_summaries = relationship("NutritionSummary", back_populates="user", cascade="all, delete-orphan")
