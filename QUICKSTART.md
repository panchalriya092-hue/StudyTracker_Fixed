# 🚀 Quick Start Guide - Study Tracker Pro

## Installation & Running (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install streamlit numpy pandas matplotlib --break-system-packages
```

### Step 2: Run the Demo (Optional)
```bash
python demo.py
```
This creates sample data and demonstrates all features.

### Step 3: Launch the Application
```bash
streamlit run app.py
```

### Step 4: Access the App
Open your browser to: `http://localhost:8501`

## 📱 Using the App

### First Time Setup

1. **Add Your First Subject**
   - Click "Manage Subjects" in the sidebar
   - Enter subject name (e.g., "Python Programming")
   - Set a goal in hours (e.g., 50)
   - Click "Add Subject"

2. **Log Your First Session**
   - Click "Add Session" in the sidebar
   - Select your subject
   - Enter topic (e.g., "Functions and Loops")
   - Set duration in minutes
   - Add optional notes
   - Click "Add Session"

3. **View Your Dashboard**
   - Click "Dashboard" to see your progress
   - Check statistics and recent activity
   - Monitor your study streak 🔥

## 🎯 Main Features

| Feature | Location | What It Does |
|---------|----------|--------------|
| Dashboard | Sidebar → Dashboard | Overview of all your study stats |
| Add Session | Sidebar → Add Session | Log new study sessions |
| Manage Subjects | Sidebar → Manage Subjects | Add/remove subjects, set goals |
| Analytics | Sidebar → Analytics | Detailed charts and visualizations |
| Reports | Sidebar → Reports | Search sessions, export data |
| Settings | Sidebar → Settings | Backup, reload, app info |

## 💡 Pro Tips

### Quick Add
Use the quick add buttons (30 min, 1 hour, 2 hours) for fast logging!

### Search
Find past sessions by searching for keywords in topics or notes.

### Export
Export your data to CSV for external analysis or backup.

### Goals
Set realistic weekly/monthly goals to stay motivated!

## 📊 Understanding Your Stats

- **Total Study Hours**: Sum of all study sessions
- **Average Session**: Mean duration of your study sessions
- **Progress**: Percentage towards your subject goals
- **Study Streak**: Consecutive days you've studied
- **Productivity Score**: Combination of time, consistency, and session quality

## 🎨 Visualizations Explained

1. **Pie Chart**: Shows time distribution across subjects
2. **Timeline**: Daily study hours over time
3. **Heatmap**: Activity pattern (week by week)
4. **Distribution**: How long your typical sessions are
5. **Progress Bars**: How close you are to your goals
6. **Topics Chart**: Which topics you've covered most

## 🐛 Common Issues

**App won't start?**
- Make sure all dependencies are installed
- Try a different port: `streamlit run app.py --server.port 8502`

**Data disappeared?**
- Check if `study_data.json` exists
- Use "Settings" → "Reload Data"

**Charts not showing?**
- Add some study sessions first
- Check that subjects have goal hours set

## 📚 Python Concepts Covered

This project demonstrates:
✅ Classes and OOP
✅ File I/O (JSON, CSV)
✅ Data structures (lists, dicts, sets, tuples)
✅ Functions and lambdas
✅ Exception handling
✅ NumPy for calculations
✅ Matplotlib for charts
✅ Streamlit for UI
✅ Modules and imports
✅ Type hints and docstrings

## 🎓 Perfect For

- College Python projects
- Learning Python concepts
- Tracking study habits
- Portfolio projects
- Understanding data visualization
- Practicing OOP design

## 📝 Example Study Session

```
Subject: Python Programming
Topic: Object-Oriented Programming - Classes and Inheritance
Duration: 90 minutes
Date: 2026-01-28
Notes: Learned about class creation, __init__, methods, and inheritance. 
       Practiced with StudyTracker example. Very clear now!
```

## 🚀 Next Steps

1. Log your first study session
2. Add all your subjects
3. Set realistic goals
4. Study consistently
5. Track your progress
6. Celebrate your achievements! 🎉

---

**Need Help?** Check README.md for detailed documentation!

**Enjoy tracking your studies!** 📚✨
