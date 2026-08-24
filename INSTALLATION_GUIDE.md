# 📚 Study Tracker - Installation Guide

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install streamlit numpy pandas matplotlib --break-system-packages
```

### Step 2: Run Demo (Creates Sample Data)
```bash
python demo.py
```

### Step 3: Start the App
```bash
streamlit run app.py
```

That's it! Your app will open in your browser at `http://localhost:8501`

---

## 🔧 What Was Fixed

Your original app had a bug - it crashed when trying to show charts with no data.

**The Error:**
```
ValueError: need at least one array to concatenate
```

**What I Fixed:**
1. ✅ Added checks before creating visualizations
2. ✅ Filter out subjects with zero hours
3. ✅ Show helpful messages when no data exists
4. ✅ Wrapped all chart code in error handling

---

## 📁 Files in This Package

```
StudyTracker_Fixed/
├── app.py                 ← FIXED: Main Streamlit app
├── visualizations.py      ← FIXED: Chart generation
├── study_tracker.py       ← Core logic (no changes needed)
├── demo.py                ← Creates sample data
├── requirements.txt       ← Python packages needed
└── INSTALLATION_GUIDE.md  ← This file
```

---

## 🎯 Complete Installation Steps

### For Windows:

1. **Open Command Prompt** in the folder containing these files

2. **Install dependencies:**
   ```cmd
   pip install streamlit numpy pandas matplotlib --break-system-packages
   ```

3. **Create sample data:**
   ```cmd
   python demo.py
   ```
   
   You'll see output like:
   ```
   Creating Study Tracker with sample data...
   Adding subjects:
     ✓ Python Programming (Goal: 50 hours)
     ✓ Data Structures (Goal: 40 hours)
     ...
   ✓ Added 36 study sessions over 30 days
   ```

4. **Run the app:**
   ```cmd
   streamlit run app.py
   ```
   
   Your browser will open automatically!

### For Mac/Linux:

Same steps, but use Terminal instead of Command Prompt.

---

## 🎮 Using the App

### First Time (With Sample Data):

1. **Dashboard** - See your study stats and charts
2. **Analytics** - View detailed visualizations
3. **Reports** - Search and export data

### Starting Fresh:

1. **Delete** `study_data.json` (if it exists)
2. **Run** `streamlit run app.py`
3. **Go to** "Manage Subjects" → Add a subject
4. **Go to** "Add Session" → Log your first study session
5. **Back to** "Dashboard" → See your data!

---

## 📊 Features

✅ Track study sessions by subject and topic
✅ Set study goals and track progress  
✅ Beautiful charts and visualizations
✅ Search your study history
✅ Export data to CSV
✅ Calculate study streaks
✅ Activity heatmaps

---

## ❓ Troubleshooting

### Problem: App won't start
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --break-system-packages
```

### Problem: "Port already in use"
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Problem: Charts not showing
**Solution:** You need at least one study session. Either:
- Run `python demo.py` to create sample data, OR
- Add a subject and log a session manually

### Problem: "Module not found" error
**Solution:** Make sure all 5 Python files are in the same folder:
- app.py
- visualizations.py  
- study_tracker.py
- demo.py
- requirements.txt

---

## 🎓 For Your College Project

This app demonstrates:
- ✅ Object-Oriented Programming (Classes)
- ✅ File Operations (JSON, CSV)
- ✅ Data Structures (Lists, Dicts, Sets)
- ✅ NumPy for calculations
- ✅ Matplotlib for visualizations
- ✅ Streamlit for web interface
- ✅ Exception handling
- ✅ Functions and modules

**Total Lines of Code:** ~1500+  
**Files:** 5 Python modules  
**Features:** 10+ major features

---

## 💡 Pro Tips

1. **Run demo first** - See how everything works with sample data
2. **Set realistic goals** - Start with achievable hour targets
3. **Log daily** - Build a study streak! 🔥
4. **Use search** - Find topics you studied before
5. **Export regularly** - Backup your data to CSV

---

## 🆘 Need Help?

### Can't run the app?
1. Check Python is installed: `python --version`
2. Should be Python 3.8 or higher
3. Install packages one by one if needed:
   ```bash
   pip install streamlit --break-system-packages
   pip install numpy --break-system-packages
   pip install pandas --break-system-packages
   pip install matplotlib --break-system-packages
   ```

### App crashes when you click something?
1. Delete `study_data.json`
2. Run `python demo.py` to start fresh
3. Then `streamlit run app.py`

---

## 🎉 You're Ready!

Just run these 3 commands:

```bash
# 1. Install
pip install streamlit numpy pandas matplotlib --break-system-packages

# 2. Create sample data
python demo.py

# 3. Start app
streamlit run app.py
```

**That's it! Happy studying!** 📚✨
