import http
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import auth, profile, foods, food_logs, recommendations, analytics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    import app.models  # noqa: F401 — register all models
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    # Seed food data from CSV if DB is empty
    from app.db.database import SessionLocal
    from app.models.food import Food
    from app.services.food_service import seed_foods_from_csv

    db = SessionLocal()
    try:
        food_count = db.query(Food).count()
        if food_count == 0:
            csv_path = os.path.join(os.path.dirname(__file__), "app", "data", "food_dataset.csv")
            if os.path.exists(csv_path):
                n = seed_foods_from_csv(db, csv_path)
                logger.info(f"Seeded {n} foods from CSV")
    finally:
        db.close()

    yield
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Nutrition Recommendation System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,            prefix="/api/v1")
app.include_router(profile.router,         prefix="/api/v1")
app.include_router(foods.router,           prefix="/api/v1")
app.include_router(food_logs.router,       prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(analytics.router,       prefix="/api/v1")


@app.get("/")
def root():
    return {"message": settings.APP_NAME, "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
