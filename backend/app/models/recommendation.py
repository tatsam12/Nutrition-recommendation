from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class RecommendationType(str, enum.Enum):
    rule_based    = "rule_based"
    decision_tree = "decision_tree"
    knn           = "knn"
    hybrid        = "hybrid"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                                 nullable=False, index=True)
    food_id             = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"),
                                 nullable=False)
    recommendation_type = Column(Enum(RecommendationType), nullable=False, index=True)
    score               = Column(Numeric(5, 4), nullable=False, default=0)
    reason              = Column(Text, nullable=True)
    generated_at        = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    user = relationship("User", back_populates="recommendations")
    food = relationship("Food", back_populates="recommendations")
