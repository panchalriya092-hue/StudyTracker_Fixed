"""
Demo Script for Study Tracker
Demonstrates all features and creates sample data
"""

from study_tracker import StudyTracker, calculate_study_streak, get_productivity_score
from visualizations import StudyVisualizer
from datetime import datetime, timedelta
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass



def create_sample_data():
    """Create sample study data for demonstration"""
    
    print("Creating Study Tracker with sample data...\n")
    
    # Initialize tracker
    tracker = StudyTracker()
    
    # Add subjects
    subjects = {
        'Python Programming': 50,
        'Data Structures': 40,
        'Web Development': 35,
        'Machine Learning': 45,
        'Database Systems': 30
    }
    
    print("Adding subjects:")
    for subject, goal in subjects.items():
        if subject not in tracker.subjects:
            tracker.add_subject(subject, goal)
            print(f"  ✓ {subject} (Goal: {goal} hours)")
        else:
            print(f"  ✓ {subject} (Already exists)")

    
    print("\nAdding study sessions:")
    
    # Topics for each subject
    topics = {
        'Python Programming': [
            'Introduction to Python',
            'Conditional Execution',
            'Loops and Iterations',
            'Functions',
            'Data Structures - Lists',
            'Data Structures - Dictionaries',
            'File Operations',
            'OOP - Classes',
            'OOP - Inheritance',
            'Exception Handling'
        ],
        'Data Structures': [
            'Arrays',
            'Linked Lists',
            'Stacks',
            'Queues',
            'Trees',
            'Graphs',
            'Sorting Algorithms',
            'Searching Algorithms'
        ],
        'Web Development': [
            'HTML Basics',
            'CSS Styling',
            'JavaScript Fundamentals',
            'DOM Manipulation',
            'React Basics',
            'Backend with Flask',
            'REST APIs'
        ],
        'Machine Learning': [
            'ML Introduction',
            'Linear Regression',
            'Logistic Regression',
            'Decision Trees',
            'Neural Networks',
            'Deep Learning Basics'
        ],
        'Database Systems': [
            'SQL Basics',
            'Database Design',
            'Normalization',
            'Joins and Queries',
            'Transactions',
            'NoSQL Databases'
        ]
    }
    
    # Generate sessions for the last 30 days
    session_count = 0
    
    for i in range(30, 0, -1):
        # Random number of sessions per day (0-3)
        num_sessions = random.randint(0, 3)
        
        if num_sessions > 0:
            study_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            # Pick random subjects for the day
            daily_subjects = random.sample(list(subjects.keys()), min(num_sessions, len(subjects)))
            
            for subject in daily_subjects:
                topic = random.choice(topics[subject])
                duration = random.choice([30, 45, 60, 90, 120])
                
                notes_options = [
                    "Good progress today",
                    "Challenging but interesting",
                    "Need to review this again",
                    "Very productive session",
                    "Practice exercises completed",
                    "Watched tutorial videos",
                    "Completed coding exercises"
                ]
                
                notes = random.choice(notes_options)
                
                tracker.add_study_session(subject, topic, duration, study_date, notes)
                session_count += 1
    
    print(f"  ✓ Added {session_count} study sessions over 30 days")
    
    return tracker


def demonstrate_features(tracker):
    """Demonstrate all tracker features"""
    
    print("\n" + "="*70)
    print("STUDY TRACKER FEATURES DEMONSTRATION")
    print("="*70)
    
    # 1. Basic statistics
    print("\n1. BASIC STATISTICS:")
    stats = tracker.get_study_statistics()
    print(f"   Total Study Hours: {stats['total_hours']} hours")
    print(f"   Total Sessions: {stats['total_sessions']}")
    print(f"   Average Session Duration: {stats['avg_session_duration']} minutes")
    print(f"   Median Session Duration: {stats['median_session_duration']} minutes")
    print(f"   Standard Deviation: {stats['std_session_duration']:.2f} minutes")
    
    # 2. Subject details
    print("\n2. SUBJECT BREAKDOWN:")
    for name, subject in tracker.subjects.items():
        hours = subject.get_total_hours()
        progress = subject.get_progress_percentage()
        productivity = get_productivity_score(subject)
        
        print(f"\n   {name}:")
        print(f"      Hours: {hours}/{subject.goal_hours} ({progress:.1f}% complete)")
        print(f"      Sessions: {len(subject.sessions)}")
        print(f"      Topics Covered: {len(subject.topics_covered)}")
        print(f"      Productivity Score: {productivity:.1f}/100")
    
    # 3. Recent sessions
    print("\n3. RECENT SESSIONS (Last 7 days):")
    recent = tracker.get_recent_sessions(7)
    for session in recent[:5]:  # Show first 5
        print(f"   • {session.date}: {session.subject} - {session.topic} ({session.duration} min)")
    
    # 4. Study streak
    print("\n4. STUDY STREAK:")
    all_sessions = []
    for subject in tracker.subjects.values():
        all_sessions.extend(subject.sessions)
    
    streak = calculate_study_streak(all_sessions)
    print(f"   Current Streak: {streak} days 🔥")
    
    # 5. Search functionality
    print("\n5. SEARCH FUNCTIONALITY:")
    search_results = tracker.search_sessions("OOP")
    print(f"   Found {len(search_results)} sessions matching 'OOP':")
    for session in search_results[:3]:
        print(f"   • {session.subject} - {session.topic}")
    
    # 6. Data export
    print("\n6. DATA EXPORT:")
    csv_filename = "study_export_demo.csv"
    tracker.export_to_csv(csv_filename)
    print(f"   ✓ Exported data to {csv_filename}")
    
    # 7. File operations
    print("\n7. FILE PERSISTENCE:")
    print(f"   Data saved to: {tracker.data_file_path}")
    print(f"   Total subjects: {len(tracker.subjects)}")
    print(f"   Data can be reloaded across sessions")
    
    print("\n" + "="*70)


def demonstrate_visualizations(tracker):
    """Create and save visualizations"""
    
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    viz = StudyVisualizer()
    
    visualizations = [
        ("subject_distribution.png", lambda: viz.plot_subject_distribution(tracker)),
        ("progress_bars.png", lambda: viz.plot_progress_bars(tracker)),
        ("study_timeline.png", lambda: viz.plot_study_timeline(tracker, 30)),
        ("activity_heatmap.png", lambda: viz.plot_heatmap(tracker)),
        ("duration_distribution.png", lambda: viz.plot_session_duration_distribution(tracker)),
        ("dashboard.png", lambda: viz.create_summary_dashboard(tracker))
    ]
    
    for filename, plot_func in visualizations:
        try:
            fig = plot_func()
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"   ✓ Saved: {filename}")
        except Exception as e:
            print(f"   ✗ Error creating {filename}: {e}")
    
    print("\n" + "="*70)


def main():
    """Main demo function"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         STUDY TRACKER - COMPREHENSIVE DEMO                     ║")
    print("║         Python College Project Demonstration                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Create sample data
    tracker = create_sample_data()
    
    # Demonstrate features
    demonstrate_features(tracker)
    
    # Create visualizations
    demonstrate_visualizations(tracker)
    
    print("\n✅ Demo completed successfully!")
    print("\nTo run the Streamlit app, execute:")
    print("   streamlit run app.py")
    print("\n")


if __name__ == "__main__":
    main()
