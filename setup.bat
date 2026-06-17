@echo off
echo ==========================================
echo  NutriNepal Setup Script
echo ==========================================

echo.
echo [1/5] Installing backend dependencies...
cd backend
python -m pip install -r requirements.txt
cd ..

echo.
echo [2/5] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo [3/5] Generating datasets...
cd datasets
python generate_datasets.py
cd ..

echo.
echo [4/5] Copying datasets to backend...
copy datasets\*.csv backend\app\data\

echo.
echo [5/5] Training ML models (requires scikit-learn)...
cd ml_training
python train_models.py
cd ..

echo.
echo ==========================================cd
echo  Setup complete!
echo.
echo  NEXT STEPS:
echo  1. Start XAMPP MySQL server
echo  2. Run: mysql -u root < backend/app/db/schema.sql
echo  3. Start backend:  cd backend && uvicorn main:app --reload
echo  4. Start frontend: cd frontend && npm run dev
echo  5. Open: http://localhost:5173
echo ==========================================
pause
