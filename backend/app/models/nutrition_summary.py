from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class NutritionSummary(Base):
    __tablename__ = "nutrition_summaries"
    __table_args__ = (UniqueConstraint("user_id", "summary_date"),)

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False, index=True)
    summary_date   = Column(Date, nullable=False, index=True)
    total_calories = Column(Numeric(8, 2), nullable=False, default=0)
    total_protein  = Column(Numeric(7, 2), nullable=False, default=0)
    total_carbs    = Column(Numeric(7, 2), nullable=False, default=0)
    total_fat      = Column(Numeric(7, 2), nullable=False, default=0)
    total_fiber    = Column(Numeric(7, 2), nullable=False, default=0)
    meal_count     = Column(Integer, nullable=False, default=0)
    created_at     = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at     = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="nutrition_summaries")
