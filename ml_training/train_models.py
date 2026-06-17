"""
ML Training Pipeline
Trains Decision Tree and KNN models, saves to backend/app/ml/models/
Run: python train_models.py
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

DATA_DIR   = os.path.join("..", "backend", "app", "data")
MODELS_DIR = os.path.join("..", "backend", "app", "ml", "models")
os.makedirs(MODELS_DIR, exist_ok=True)



# DECISION TREE — food category prediction

print("Training Decision Tree...")

df_users = pd.read_csv(os.path.join(DATA_DIR, "user_profile_dataset.csv"))

FEATURES = ["age", "gender", "bmi", "activity_level", "nutrition_goal"]
TARGET   = "recommended_category"

le_gender   = LabelEncoder()
le_activity = LabelEncoder()
le_goal     = LabelEncoder()
le_category = LabelEncoder()

df_users["gender_enc"]   = le_gender.fit_transform(df_users["gender"])
df_users["activity_enc"] = le_activity.fit_transform(df_users["activity_level"])
df_users["goal_enc"]     = le_goal.fit_transform(df_users["nutrition_goal"])
df_users["target_enc"]   = le_category.fit_transform(df_users[TARGET])

X = df_users[["age", "gender_enc", "bmi", "activity_enc", "goal_enc"]].values
y = df_users["target_enc"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeClassifier(
    max_depth=8,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
)
dt_model.fit(X_train, y_train)

acc = accuracy_score(y_test, dt_model.predict(X_test))
print(f"  Decision Tree accuracy: {acc:.3f}")
print(classification_report(y_test, dt_model.predict(X_test),
                             target_names=le_category.classes_))

joblib.dump(dt_model,   os.path.join(MODELS_DIR, "decision_tree.pkl"))
joblib.dump(le_gender,  os.path.join(MODELS_DIR, "le_gender.pkl"))
joblib.dump(le_activity,os.path.join(MODELS_DIR, "le_activity.pkl"))
joblib.dump(le_goal,    os.path.join(MODELS_DIR, "le_goal.pkl"))
joblib.dump(le_category,os.path.join(MODELS_DIR, "le_category.pkl"))
print("[OK] Decision Tree saved")


# KNN — user-based collaborative filtering

print("\nTraining KNN Recommender...")

df_history = pd.read_csv(os.path.join(DATA_DIR, "food_history_dataset.csv"))

# Build user-food frequency matrix (sparse representation)
user_food_matrix = df_history.pivot_table(
    index="user_id", columns="food_id", values="frequency", aggfunc="sum", fill_value=0
)

scaler = StandardScaler()
matrix_scaled = scaler.fit_transform(user_food_matrix.values)

knn_model = NearestNeighbors(n_neighbors=10, metric="cosine", algorithm="brute")
knn_model.fit(matrix_scaled)

joblib.dump(knn_model,         os.path.join(MODELS_DIR, "knn_model.pkl"))
joblib.dump(scaler,            os.path.join(MODELS_DIR, "knn_scaler.pkl"))
joblib.dump(user_food_matrix,  os.path.join(MODELS_DIR, "user_food_matrix.pkl"))
print("[OK] KNN model saved")



# Save metadata for inference

import json

metadata = {
    "dt_feature_names":  ["age", "gender_enc", "bmi", "activity_enc", "goal_enc"],
    "dt_classes":        list(le_category.classes_),
    "gender_classes":    list(le_gender.classes_),
    "activity_classes":  list(le_activity.classes_),
    "goal_classes":      list(le_goal.classes_),
    "knn_user_ids":      list(user_food_matrix.index.astype(int)),
    "knn_food_ids":      list(user_food_matrix.columns.astype(int)),
}

with open(os.path.join(MODELS_DIR, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

print("[OK] metadata.json saved")
print("\nAll models trained successfully.")
