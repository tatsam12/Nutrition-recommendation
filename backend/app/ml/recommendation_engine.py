"""
Hybrid Recommendation Engine
Combines Rule-Based (30%) + Decision Tree (30%) + KNN (40%)
"""

import os
import json
import logging
from typing import Optional
import numpy as np
import joblib

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

# Lazy-loaded singletons
_dt_model    = None
_knn_model   = None
_knn_scaler  = None
_user_matrix = None
_meta        = None
_encoders    = {}


def _load_models():
    global _dt_model, _knn_model, _knn_scaler, _user_matrix, _meta, _encoders
    if _dt_model is not None:
        return
    try:
        _dt_model   = joblib.load(os.path.join(MODELS_DIR, "decision_tree.pkl"))
        _knn_model  = joblib.load(os.path.join(MODELS_DIR, "knn_model.pkl"))
        _knn_scaler = joblib.load(os.path.join(MODELS_DIR, "knn_scaler.pkl"))
        _user_matrix= joblib.load(os.path.join(MODELS_DIR, "user_food_matrix.pkl"))
        with open(os.path.join(MODELS_DIR, "metadata.json")) as f:
            _meta = json.load(f)
        _encoders = {
            "gender":   joblib.load(os.path.join(MODELS_DIR, "le_gender.pkl")),
            "activity": joblib.load(os.path.join(MODELS_DIR, "le_activity.pkl")),
            "goal":     joblib.load(os.path.join(MODELS_DIR, "le_goal.pkl")),
            "category": joblib.load(os.path.join(MODELS_DIR, "le_category.pkl")),
        }
        logger.info("ML models loaded successfully")
    except Exception as e:
        logger.warning(f"ML models not loaded: {e}. Falling back to rule-based only.")


def predict_food_category(age: int, gender: str, bmi: float,
                           activity_level: str, nutrition_goal: str) -> Optional[str]:
    _load_models()
    if _dt_model is None:
        return _rule_based_category(bmi, nutrition_goal)
    try:
        g = _encoders["gender"].transform([gender])[0]
        a = _encoders["activity"].transform([activity_level])[0]
        gl= _encoders["goal"].transform([nutrition_goal])[0]
        X = np.array([[age, g, bmi, a, gl]])
        pred = _dt_model.predict(X)[0]
        return _encoders["category"].inverse_transform([pred])[0]
    except Exception as e:
        logger.warning(f"DT predict error: {e}")
        return _rule_based_category(bmi, nutrition_goal)


def get_knn_food_ids(user_id: int, top_n: int = 10) -> list[int]:
    _load_models()
    if _knn_model is None or _user_matrix is None:
        return []
    try:
        user_ids = _meta["knn_user_ids"]
        food_ids = _meta["knn_food_ids"]
        if user_id not in user_ids:
            return []
        idx = user_ids.index(user_id)
        row = _user_matrix.values[idx].reshape(1, -1)
        row_scaled = _knn_scaler.transform(row)
        distances, indices = _knn_model.kneighbors(row_scaled, n_neighbors=min(10, len(user_ids)))
        neighbor_indices = indices[0][1:]  # exclude self
        food_scores: dict[int, float] = {}
        for ni in neighbor_indices:
            neighbor_row = _user_matrix.values[ni]
            for fi, freq in enumerate(neighbor_row):
                if freq > 0 and _user_matrix.values[idx][fi] == 0:
                    fid = food_ids[fi]
                    food_scores[fid] = food_scores.get(fid, 0) + freq
        top = sorted(food_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [fid for fid, _ in top]
    except Exception as e:
        logger.warning(f"KNN error: {e}")
        return []


def _rule_based_category(bmi: float, goal: str) -> str:
    if goal == "weight_loss" or bmi >= 27.5:
        return "Low Calorie"
    if goal == "muscle_gain":
        return "High Protein"
    if goal == "weight_gain" or bmi < 18.5:
        return "High Energy"
    if bmi >= 25:
        return "Fiber Rich"
    return "Balanced Diet"


CATEGORY_GOAL_MAP = {
    "Low Calorie": ["weight_loss"],
    "High Protein": ["muscle_gain", "weight_gain"],
    "High Energy": ["weight_gain", "muscle_gain"],
    "Fiber Rich": ["weight_loss", "maintenance"],
    "Balanced Diet": ["maintenance"],
}


def generate_hybrid_recommendations(
    db,
    user_id: int,
    age: int,
    gender: str,
    bmi: float,
    activity_level: str,
    nutrition_goal: str,
    top_n: int = 10,
) -> list[dict]:
    from app.models.food import Food

    # Step 1: Decision Tree category prediction
    dt_category = predict_food_category(age, gender, bmi, activity_level, nutrition_goal)

    # Step 2: Rule-based food IDs (goal-aligned foods)
    rule_foods = (
        db.query(Food)
        .filter(Food.is_active == True, Food.recommended_goal == nutrition_goal)
        .limit(30)
        .all()
    )

    # Step 3: KNN food IDs
    knn_food_ids = get_knn_food_ids(user_id, top_n=20)

    # Step 4: DT category foods
    dt_foods = (
        db.query(Food)
        .filter(Food.is_active == True)
        .all()
    )
    dt_filtered = _filter_by_category(dt_foods, dt_category)

    # Step 5: Hybrid scoring
    scores: dict[int, dict] = {}

    for food in rule_foods:
        entry = scores.setdefault(food.id, {"food": food, "score": 0.0, "sources": []})
        entry["score"] += 0.30
        entry["sources"].append("rule_based")

    for fid in knn_food_ids:
        food = db.query(Food).filter(Food.id == fid, Food.is_active == True).first()
        if food:
            entry = scores.setdefault(fid, {"food": food, "score": 0.0, "sources": []})
            entry["score"] += 0.40
            entry["sources"].append("knn")

    for food in dt_filtered[:20]:
        entry = scores.setdefault(food.id, {"food": food, "score": 0.0, "sources": []})
        entry["score"] += 0.30
        entry["sources"].append("decision_tree")

    # Sort and return top_n
    ranked = sorted(scores.values(), key=lambda x: x["score"], reverse=True)[:top_n]
    return [
        {
            "food":    r["food"],
            "score":   round(min(r["score"], 1.0), 4),
            "sources": list(set(r["sources"])),
            "reason":  _build_reason(r["sources"], dt_category, nutrition_goal),
        }
        for r in ranked
    ]


def _filter_by_category(foods: list, category: str) -> list:
    category_filters = {
        "Low Calorie":  lambda f: float(f.calories) < 200,
        "High Protein": lambda f: float(f.protein) > 10,
        "High Energy":  lambda f: float(f.calories) > 250,
        "Fiber Rich":   lambda f: float(f.fiber) > 3,
        "Balanced Diet": lambda f: 150 <= float(f.calories) <= 400,
    }
    fn = category_filters.get(category, lambda f: True)
    return [f for f in foods if fn(f)]


def _build_reason(sources: list, category: str, goal: str) -> str:
    parts = []
    if "rule_based" in sources:
        parts.append(f"matches your {goal.replace('_',' ')} goal")
    if "decision_tree" in sources:
        parts.append(f"fits {category} category (ML prediction)")
    if "knn" in sources:
        parts.append("popular among similar users")
    return "; ".join(parts).capitalize() if parts else "Recommended for your profile"


def generate_meal_plan(db, nutrition_goal: str) -> dict:
    from app.models.food import Food
    import random

    MEAL_GOALS = {
        "breakfast": {"weight_loss": ("< 400 cal",  lambda f: float(f.calories) < 400),
                      "weight_gain": ("> 500 cal",  lambda f: float(f.calories) > 500),
                      "muscle_gain": ("high protein",lambda f: float(f.protein) > 15),
                      "maintenance": ("balanced",    lambda f: 200 <= float(f.calories) <= 500)},
        "lunch":     {"weight_loss": ("< 500 cal",  lambda f: float(f.calories) < 500),
                      "weight_gain": ("> 600 cal",  lambda f: float(f.calories) > 600),
                      "muscle_gain": ("high protein",lambda f: float(f.protein) > 20),
                      "maintenance": ("balanced",    lambda f: 300 <= float(f.calories) <= 700)},
        "dinner":    {"weight_loss": ("< 450 cal",  lambda f: float(f.calories) < 450),
                      "weight_gain": ("> 550 cal",  lambda f: float(f.calories) > 550),
                      "muscle_gain": ("high protein",lambda f: float(f.protein) > 18),
                      "maintenance": ("balanced",    lambda f: 250 <= float(f.calories) <= 600)},
        "snack":     {"weight_loss": ("< 150 cal",  lambda f: float(f.calories) < 150),
                      "weight_gain": ("> 250 cal",  lambda f: float(f.calories) > 250),
                      "muscle_gain": ("protein snack",lambda f: float(f.protein) > 5),
                      "maintenance": ("light snack", lambda f: float(f.calories) < 300)},
    }

    plan = {}
    all_foods = db.query(Food).filter(Food.is_active == True).all()

    for meal in ["breakfast", "lunch", "dinner", "snack"]:
        _, fn = MEAL_GOALS[meal].get(nutrition_goal, ("any", lambda f: True))
        filtered = [f for f in all_foods if fn(f)]
        if not filtered:
            filtered = all_foods
        chosen = random.choice(filtered)
        plan[meal] = {
            "id":       chosen.id,
            "name":     chosen.food_name,
            "calories": float(chosen.calories),
            "protein":  float(chosen.protein),
            "image_url":chosen.image_url,
        }

    plan["total_calories"] = sum(v["calories"] for v in plan.values() if isinstance(v, dict))
    return plan
