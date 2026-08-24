@echo off
echo ===============================================
echo   STUDY TRACKER - Quick Start
echo ===============================================
echo.

echo Checking if demo data exists...
if not exist study_data.json (
    echo No data found! Creating sample data...
    python demo.py
    echo.
)

echo Starting Streamlit app...
echo.
echo Your browser will open automatically!
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py

pause
