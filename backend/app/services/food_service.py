from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.food import Food
from app.schemas.food import FoodCreate, FoodUpdate


def get_foods(db: Session, skip: int = 0, limit: int = 50,
              category: Optional[str] = None) -> list[Food]:
    q = db.query(Food).filter(Food.is_active == True)
    if category:
        q = q.filter(Food.category == category)
    return q.offset(skip).limit(limit).all()


def search_foods(db: Session, query: str, limit: int = 20) -> list[Food]:
    pattern = f"%{query}%"
    return (
        db.query(Food)
        .filter(Food.is_active == True)
        .filter(or_(Food.food_name.ilike(pattern), Food.category.ilike(pattern)))
        .limit(limit)
        .all()
    )


def get_food(db: Session, food_id: int) -> Food:
    food = db.query(Food).filter(Food.id == food_id, Food.is_active == True).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


def create_food(db: Session, data: FoodCreate) -> Food:
    food = Food(**data.model_dump())
    db.add(food)
    db.commit()
    db.refresh(food)
    return food


def update_food(db: Session, food_id: int, data: FoodUpdate) -> Food:
    food = get_food(db, food_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(food, field, value)
    db.commit()
    db.refresh(food)
    return food


def delete_food(db: Session, food_id: int) -> None:
    food = get_food(db, food_id)
    food.is_active = False
    db.commit()


def seed_foods_from_csv(db: Session, csv_path: str) -> int:
    import csv
    count = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = db.query(Food).filter(Food.food_name == row["food_name"]).first()
            if not existing:
                food = Food(
                    food_name=row["food_name"],
                    category=row["category"],
                    calories=float(row["calories"]),
                    protein=float(row["protein"]),
                    carbohydrates=float(row["carbohydrates"]),
                    fat=float(row["fat"]),
                    fiber=float(row["fiber"]),
                    serving_size=row.get("serving_size", "100g"),
                    image_url=row.get("image_url"),
                    recommended_goal=row.get("recommended_goal"),
                )
                db.add(food)
                count += 1
    db.commit()
    return count
