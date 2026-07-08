# NutriHealth - Nutrition Recommendation System

NutriNepal is an MVP nutrition recommendation system developed as a capstone project. The application focuses on Nepali dietary habits and currently uses a synthetic dataset to demonstrate personalized meal recommendations. Future work includes integrating real-world nutritional datasets, hybrid recommendation algorithms, and AI-based nutrient prediction.

## Tech Stack
- **Frontend**: React + Vite + Tailwind CSS + Recharts
- **Backend**: FastAPI + SQLAlchemy + JWT Auth
- **Database**: MySQL (XAMPP)
- **ML**: Decision Tree + KNN + Hybrid Engine

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- XAMPP (MySQL running)

### 1. Database Setup
Start XAMPP MySQL, then:
```sql
mysql -u root < backend/app/db/schema.sql
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API available at: http://localhost:8000
Docs available at: http://localhost:8000/docs

### 3. ML Training (optional — improves recommendations)
```bash
cd ml_training
python train_models.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
App available at: http://localhost:5173

### Or run setup.bat for automated setup

## Features
- JWT authentication with refresh tokens
- BMI auto-calculation with Harris-Benedict formula
- Nepal-focused food database (215+ foods)
- Decision Tree food category prediction
- KNN user-based collaborative filtering
- Hybrid recommendation engine
- 7 dashboard charts with Recharts
- Responsive mobile-friendly design
- Food image display throughout
