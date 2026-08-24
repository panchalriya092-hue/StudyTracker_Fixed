"""
Study Tracker - Streamlit Application
FIXED VERSION - Handles empty data properly
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from study_tracker import StudyTracker, calculate_study_streak, get_productivity_score
from visualizations import StudyVisualizer


# Page configuration
st.set_page_config(
    page_title="Study Tracker Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'tracker' not in st.session_state:
    st.session_state.tracker = StudyTracker()

tracker = st.session_state.tracker


def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📚 Study Tracker Pro</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Session", "Manage Subjects", "Analytics", "Reports", "Settings"]
    )
    
    # Display selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Session":
        show_add_session()
    elif page == "Manage Subjects":
        show_manage_subjects()
    elif page == "Analytics":
        show_analytics()
    elif page == "Reports":
        show_reports()
    elif page == "Settings":
        show_settings()


def show_dashboard():
    """Display main dashboard"""
    st.header("📊 Dashboard")
    
    # Quick stats
    stats = tracker.get_study_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Study Hours", f"{stats['total_hours']} hrs")
    
    with col2:
        st.metric("Total Sessions", stats['total_sessions'])
    
    with col3:
        st.metric("Active Subjects", stats['subjects_count'])
    
    with col4:
        avg_session = stats['avg_session_duration']
        st.metric("Avg. Session", f"{avg_session} min")
    
    st.divider()
    
    # Recent activity
    st.subheader("🕐 Recent Activity")
    
    recent_sessions = tracker.get_recent_sessions(days=7)
    
    if recent_sessions:
        # Calculate streak
        all_sessions = []
        for subject in tracker.subjects.values():
            all_sessions.extend(subject.sessions)
        
        streak = calculate_study_streak(all_sessions)
        
        if streak > 0:
            st.markdown(f'<div class="success-box">🔥 Current Streak: {streak} days! Keep it up!</div>', 
                       unsafe_allow_html=True)
        
        # Display recent sessions table
        recent_data = []
        for session in recent_sessions[:10]:
            recent_data.append({
                'Date': session.date,
                'Subject': session.subject,
                'Topic': session.topic,
                'Duration': f"{session.duration} min",
                'Notes': session.notes[:50] + '...' if len(session.notes) > 50 else session.notes
            })
        
        df = pd.DataFrame(recent_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No recent study sessions. Start tracking your study time!")
    
    st.divider()
    
    # Subject overview
    st.subheader("📚 Subject Overview")
    
    if tracker.subjects:
        subject_data = []
        
        for name, subject in tracker.subjects.items():
            productivity = get_productivity_score(subject)
            
            subject_data.append({
                'Subject': name,
                'Total Hours': subject.get_total_hours(),
                'Sessions': len(subject.sessions),
                'Topics Covered': len(subject.topics_covered),
                'Goal (hrs)': subject.goal_hours,
                'Progress': f"{subject.get_progress_percentage():.1f}%",
                'Productivity': f"{productivity:.1f}"
            })
        
        df_subjects = pd.DataFrame(subject_data)
        st.dataframe(df_subjects, use_container_width=True)
        
        # Quick visualization - FIXED: Check for sessions first
        if stats['total_sessions'] > 0:
            st.subheader("📈 Study Distribution")
            viz = StudyVisualizer()
            try:
                fig = viz.plot_subject_distribution(tracker)
                st.pyplot(fig)
            except Exception as e:
                st.info("Add some study sessions to see the distribution chart!")
        else:
            st.info("📊 Add some study sessions to see visualizations!")
    else:
        st.warning("No subjects added yet. Go to 'Manage Subjects' to add your first subject!")


def show_add_session():
    """Add new study session"""
    st.header("➕ Add Study Session")
    
    if not tracker.subjects:
        st.warning("Please add at least one subject first in 'Manage Subjects' tab.")
        return
    
    with st.form("add_session_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Subject", tracker.get_all_subjects())
            topic = st.text_input("Topic", placeholder="e.g., Functions and Recursion")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=60)
        
        with col2:
            study_date = st.date_input("Date", datetime.now())
            notes = st.text_area("Notes (optional)", placeholder="What did you learn?")
        
        # Quick duration buttons
        st.write("**Quick Duration:**")
        col_a, col_b, col_c = st.columns(3)
        
        submit = st.form_submit_button("Add Session", use_container_width=True)
        
        if submit:
            if not topic:
                st.error("Please enter a topic!")
            else:
                try:
                    date_str = study_date.strftime('%Y-%m-%d')
                    tracker.add_study_session(subject, topic, duration, date_str, notes)
                    st.success(f"✅ Added {duration} min session for {subject}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")


def show_manage_subjects():
    """Manage subjects"""
    st.header("📚 Manage Subjects")
    
    # Add new subject
    st.subheader("Add New Subject")
    
    with st.form("add_subject_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject_name = st.text_input("Subject Name", placeholder="e.g., Python Programming")
        
        with col2:
            goal_hours = st.number_input("Goal Hours", min_value=0, value=50)
        
        submit = st.form_submit_button("Add Subject", use_container_width=True)
        
        if submit:
            if not subject_name:
                st.error("Please enter a subject name!")
            else:
                try:
                    tracker.add_subject(subject_name, goal_hours)
                    st.success(f"✅ Added {subject_name} with {goal_hours} hour goal!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.divider()
    
    # List existing subjects
    st.subheader("Existing Subjects")
    
    if tracker.subjects:
        for name, subject in tracker.subjects.items():
            with st.expander(f"📖 {name}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Hours", f"{subject.get_total_hours()} hrs")
                
                with col2:
                    st.metric("Sessions", len(subject.sessions))
                
                with col3:
                    st.metric("Progress", f"{subject.get_progress_percentage():.1f}%")
                
                st.write(f"**Goal:** {subject.goal_hours} hours")
                st.write(f"**Topics Covered:** {len(subject.topics_covered)}")
                
                if st.button(f"Delete {name}", key=f"del_{name}"):
                    try:
                        tracker.remove_subject(name)
                        st.success(f"Deleted {name}")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
    else:
        st.info("No subjects added yet.")


def show_analytics():
    """Show detailed analytics"""
    st.header("📊 Analytics")
    
    if not tracker.subjects:
        st.warning("No data available. Add subjects and study sessions first.")
        return
    
    # FIXED: Check if there are any sessions
    stats = tracker.get_study_statistics()
    if stats['total_sessions'] == 0:
        st.warning("No study sessions recorded yet. Add some sessions to see analytics!")
        return
    
    viz = StudyVisualizer()
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Timeline", "Distribution", "Topics"])
    
    with tab1:
        st.subheader("Comprehensive Dashboard")
        try:
            fig = viz.create_summary_dashboard(tracker)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating dashboard: {str(e)}")
    
    with tab2:
        st.subheader("Study Timeline")
        
        days = st.slider("Days to show", 7, 90, 30)
        try:
            fig = viz.plot_study_timeline(tracker, days)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating timeline: {str(e)}")
        
        st.divider()
        
        st.subheader("Activity Heatmap")
        
        subject_for_heatmap = st.selectbox(
            "Select subject (or leave for all)",
            ["All"] + tracker.get_all_subjects()
        )
        
        selected_subject = None if subject_for_heatmap == "All" else subject_for_heatmap
        try:
            fig = viz.plot_heatmap(tracker, selected_subject)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating heatmap: {str(e)}")
    
    with tab3:
        st.subheader("Session Duration Distribution")
        try:
            fig = viz.plot_session_duration_distribution(tracker)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating distribution: {str(e)}")
        
        st.divider()
        
        st.subheader("Progress Towards Goals")
        try:
            fig = viz.plot_progress_bars(tracker)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error creating progress bars: {str(e)}")
    
    with tab4:
        st.subheader("Topics Analysis")
        
        subject = st.selectbox("Select Subject", tracker.get_all_subjects())
        
        if subject:
            try:
                fig = viz.plot_topics_covered(tracker, subject)
                st.pyplot(fig)
            except Exception as e:
                st.info("No topics recorded for this subject yet.")
            
            st.divider()
            
            # List all topics
            subject_obj = tracker.get_subject(subject)
            if subject_obj and subject_obj.topics_covered:
                st.write("**All Topics Covered:**")
                topics_list = sorted(list(subject_obj.topics_covered))
                
                cols = st.columns(3)
                for idx, topic in enumerate(topics_list):
                    with cols[idx % 3]:
                        st.write(f"✓ {topic}")


def show_reports():
    """Generate and export reports"""
    st.header("📄 Reports")
    
    # Search functionality
    st.subheader("🔍 Search Sessions")
    
    search_keyword = st.text_input("Search by topic or notes", placeholder="Enter keyword...")
    
    if search_keyword:
        results = tracker.search_sessions(search_keyword)
        
        if results:
            st.write(f"Found {len(results)} matching sessions:")
            
            search_data = []
            for session in results:
                search_data.append({
                    'Date': session.date,
                    'Subject': session.subject,
                    'Topic': session.topic,
                    'Duration': f"{session.duration} min",
                    'Notes': session.notes
                })
            
            df = pd.DataFrame(search_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No matching sessions found.")
    
    st.divider()
    
    # Export functionality
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export to CSV", use_container_width=True):
            try:
                filename = f"study_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                tracker.export_to_csv(filename)
                
                with open(filename, 'r') as f:
                    csv_data = f.read()
                
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )
                st.success("✅ Data exported successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.info("Export all your study data to CSV format for backup or analysis in Excel.")


def show_settings():
    """App settings and info"""
    st.header("⚙️ Settings")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reload Data", use_container_width=True):
            try:
                tracker.load_data()
                st.success("✅ Data reloaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Clear All Data", use_container_width=True):
            if st.checkbox("I'm sure I want to delete all data"):
                tracker.subjects = {}
                tracker.save_data()
                st.success("✅ All data cleared!")
                st.rerun()
    
    st.divider()
    
    st.subheader("📊 Statistics")
    
    stats = tracker.get_study_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Subjects", stats['subjects_count'])
    
    with col2:
        st.metric("Total Sessions", stats['total_sessions'])
    
    with col3:
        st.metric("Total Hours", f"{stats['total_hours']} hrs")
    
    st.divider()
    
    st.subheader("ℹ️ About")
    
    st.info("""
    **Study Tracker Pro v1.0**
    
    A comprehensive study tracking application built with Python.
    
    Features:
    - Track study sessions by subject and topic
    - Set and monitor study goals
    - Visualize your progress with charts
    - Search and export your data
    - Calculate study streaks
    
    Built with: Python, Streamlit, NumPy, Pandas, Matplotlib
    """)


if __name__ == "__main__":
    main()
