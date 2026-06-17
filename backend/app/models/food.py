from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Food(Base):
    __tablename__ = "foods"

    id               = Column(Integer, primary_key=True, index=True)
    food_name        = Column(String(150), nullable=False, index=True)
    category         = Column(String(100), nullable=False, index=True)
    calories         = Column(Numeric(7, 2), nullable=False)
    protein          = Column(Numeric(6, 2), nullable=False, default=0)
    carbohydrates    = Column(Numeric(6, 2), nullable=False, default=0)
    fat              = Column(Numeric(6, 2), nullable=False, default=0)
    fiber            = Column(Numeric(6, 2), nullable=False, default=0)
    serving_size     = Column(String(50), nullable=False, default="100g")
    image_url        = Column(Text, nullable=True)
    recommended_goal = Column(String(50), nullable=True, index=True)
    is_active        = Column(Boolean, default=True, nullable=False)
    created_at       = Column(DateTime, server_default=func.now(), nullable=False)

    food_logs       = relationship("FoodLog", back_populates="food")
    recommendations = relationship("Recommendation", back_populates="food")
