#!/bin/bash
echo "==============================================="
echo "  STUDY TRACKER - Quick Start"
echo "==============================================="
echo ""

if [ ! -f "study_data.json" ]; then
    echo "No data found! Creating sample data..."
    python demo.py
    echo ""
fi

echo "Starting Streamlit app..."
echo ""
echo "Your browser will open automatically!"
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run app.py
