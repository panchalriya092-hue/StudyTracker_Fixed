"""
Visualization Module for Study Tracker
Demonstrates: NumPy operations, Data Visualization
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import matplotlib.dates as mdates
from study_tracker import StudyTracker, Subject


class StudyVisualizer:
    """Handles all visualizations for study data"""
    
    @staticmethod
    def plot_subject_distribution(tracker: StudyTracker) -> plt.Figure:
        """Create pie chart of study time distribution by subject"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if not tracker.subjects:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return fig
        
        subjects = list(tracker.subjects.keys())
        hours = [tracker.subjects[s].get_total_hours() for s in subjects]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(subjects)))
        
        ax.pie(hours, labels=subjects, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Study Time Distribution by Subject', fontsize=14, fontweight='bold')
        
        return fig
    
    @staticmethod
    def plot_progress_bars(tracker: StudyTracker) -> plt.Figure:
        """Create horizontal bar chart showing progress towards goals"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        subjects = []
        progress = []
        colors_list = []
        
        for name, subject in tracker.subjects.items():
            if subject.goal_hours > 0:
                subjects.append(name)
                prog = subject.get_progress_percentage()
                progress.append(min(prog, 100))  # Cap at 100%
                
                # Color coding: red < 50%, yellow 50-80%, green > 80%
                if prog < 50:
                    colors_list.append('#ff6b6b')
                elif prog < 80:
                    colors_list.append('#ffd93d')
                else:
                    colors_list.append('#6bcf7f')
        
        if not subjects:
            ax.text(0.5, 0.5, 'No goals set for any subject', ha='center', va='center')
            return fig
        
        y_pos = np.arange(len(subjects))
        ax.barh(y_pos, progress, color=colors_list)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(subjects)
        ax.set_xlabel('Progress (%)', fontweight='bold')
        ax.set_title('Progress Towards Study Goals', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        # Add percentage labels
        for i, v in enumerate(progress):
            ax.text(v + 2, i, f'{v:.1f}%', va='center')
        
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_study_timeline(tracker: StudyTracker, days: int = 30) -> plt.Figure:
        """Create line chart showing daily study time over the last N days"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Create date range
        date_range = [start_date + timedelta(days=i) for i in range(days + 1)]
        date_strings = [d.strftime('%Y-%m-%d') for d in date_range]
        
        # Initialize daily study time
        daily_time = np.zeros(len(date_range))
        
        # Aggregate study time by day
        for subject in tracker.subjects.values():
            for session in subject.sessions:
                if session.date in date_strings:
                    idx = date_strings.index(session.date)
                    daily_time[idx] += session.duration / 60  # Convert to hours
        
        # Plot
        ax.plot(date_range, daily_time, marker='o', linewidth=2, markersize=4, color='#4a90e2')
        ax.fill_between(date_range, daily_time, alpha=0.3, color='#4a90e2')
        
        # Formatting
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Study Hours', fontweight='bold')
        ax.set_title(f'Daily Study Time - Last {days} Days', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Add statistics
        avg_time = np.mean(daily_time)
        max_time = np.max(daily_time)
        ax.axhline(y=avg_time, color='r', linestyle='--', label=f'Average: {avg_time:.1f}h', alpha=0.7)
        ax.legend()
        
        return fig
    
    @staticmethod
    def plot_heatmap(tracker: StudyTracker, subject_name: str = None) -> plt.Figure:
        """Create heatmap of study activity (7 days x 4 weeks)"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get last 28 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=27)
        
        # Create 4 weeks x 7 days matrix
        heatmap_data = np.zeros((4, 7))
        
        # Collect sessions
        sessions = []
        if subject_name and subject_name in tracker.subjects:
            sessions = tracker.subjects[subject_name].sessions
        else:
            for subject in tracker.subjects.values():
                sessions.extend(subject.sessions)
        
        # Fill heatmap
        for session in sessions:
            session_date = datetime.strptime(session.date, '%Y-%m-%d')
            if start_date <= session_date <= end_date:
                days_diff = (session_date - start_date).days
                week = days_diff // 7
                day = days_diff % 7
                if week < 4:
                    heatmap_data[week][day] += session.duration / 60
        
        # Create heatmap
        im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
        
        # Labels
        ax.set_xticks(np.arange(7))
        ax.set_yticks(np.arange(4))
        ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax.set_yticklabels([f'Week {i+1}' for i in range(4)])
        
        title = f'Study Activity Heatmap - Last 4 Weeks'
        if subject_name:
            title += f' ({subject_name})'
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Color bar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Study Hours', rotation=270, labelpad=20)
        
        # Add text annotations
        for i in range(4):
            for j in range(7):
                if heatmap_data[i, j] > 0:
                    text = ax.text(j, i, f'{heatmap_data[i, j]:.1f}',
                                 ha="center", va="center", color="black", fontsize=9)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_session_duration_distribution(tracker: StudyTracker) -> plt.Figure:
        """Create histogram of session durations"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        all_durations = []
        for subject in tracker.subjects.values():
            all_durations.extend([s.duration for s in subject.sessions])
        
        if not all_durations:
            ax.text(0.5, 0.5, 'No sessions recorded', ha='center', va='center')
            return fig
        
        durations_array = np.array(all_durations)
        
        # Create histogram
        n, bins, patches = ax.hist(durations_array, bins=20, color='#4a90e2', 
                                   alpha=0.7, edgecolor='black')
        
        # Add statistics
        mean_duration = np.mean(durations_array)
        median_duration = np.median(durations_array)
        
        ax.axvline(mean_duration, color='red', linestyle='--', 
                  label=f'Mean: {mean_duration:.1f} min', linewidth=2)
        ax.axvline(median_duration, color='green', linestyle='--', 
                  label=f'Median: {median_duration:.1f} min', linewidth=2)
        
        ax.set_xlabel('Duration (minutes)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Session Duration Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_topics_covered(tracker: StudyTracker, subject_name: str) -> plt.Figure:
        """Create bar chart of topics covered for a subject"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if subject_name not in tracker.subjects:
            ax.text(0.5, 0.5, f'Subject "{subject_name}" not found', 
                   ha='center', va='center')
            return fig
        
        subject = tracker.subjects[subject_name]
        
        # Count time per topic
        topic_time = {}
        for session in subject.sessions:
            topic_time[session.topic] = topic_time.get(session.topic, 0) + session.duration / 60
        
        if not topic_time:
            ax.text(0.5, 0.5, 'No topics recorded', ha='center', va='center')
            return fig
        
        # Sort by time
        sorted_topics = sorted(topic_time.items(), key=lambda x: x[1], reverse=True)
        topics = [t[0] for t in sorted_topics]
        times = [t[1] for t in sorted_topics]
        
        # Create bar chart
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(topics)))
        bars = ax.bar(range(len(topics)), times, color=colors)
        
        ax.set_xticks(range(len(topics)))
        ax.set_xticklabels(topics, rotation=45, ha='right')
        ax.set_ylabel('Study Time (hours)', fontweight='bold')
        ax.set_title(f'Topics Covered - {subject_name}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, (bar, time) in enumerate(zip(bars, times)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'{time:.1f}h', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_summary_dashboard(tracker: StudyTracker) -> plt.Figure:
        """Create a comprehensive dashboard with multiple charts"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Get statistics
        stats = tracker.get_study_statistics()
        
        # 1. Subject Distribution (Pie)
        ax1 = fig.add_subplot(gs[0, 0])
        if tracker.subjects:
            subjects = list(tracker.subjects.keys())
            hours = [tracker.subjects[s].get_total_hours() for s in subjects]
            colors = plt.cm.Set3(np.linspace(0, 1, len(subjects)))
            ax1.pie(hours, labels=subjects, autopct='%1.1f%%', colors=colors)
            ax1.set_title('Study Distribution', fontweight='bold')
        
        # 2. Weekly Timeline
        ax2 = fig.add_subplot(gs[0, 1])
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        date_range = [start_date + timedelta(days=i) for i in range(8)]
        date_strings = [d.strftime('%Y-%m-%d') for d in date_range]
        daily_time = np.zeros(8)
        
        for subject in tracker.subjects.values():
            for session in subject.sessions:
                if session.date in date_strings:
                    idx = date_strings.index(session.date)
                    daily_time[idx] += session.duration / 60
        
        ax2.plot(date_range, daily_time, marker='o', color='#4a90e2', linewidth=2)
        ax2.fill_between(date_range, daily_time, alpha=0.3)
        ax2.set_title('Last 7 Days', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Statistics Panel
        ax3 = fig.add_subplot(gs[1, :])
        ax3.axis('off')
        
        stats_text = f"""
        STUDY STATISTICS
        
        Total Study Time: {stats['total_hours']} hours
        Total Sessions: {stats['total_sessions']}
        Average Session: {stats['avg_session_duration']} minutes
        Median Session: {stats['median_session_duration']} minutes
        Subjects Tracked: {stats['subjects_count']}
        Longest Session: {stats['max_session_duration']} minutes
        Shortest Session: {stats['min_session_duration']} minutes
        """
        
        ax3.text(0.5, 0.5, stats_text, ha='center', va='center',
                fontsize=12, fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 4. Progress Bars
        ax4 = fig.add_subplot(gs[2, :])
        subjects_with_goals = []
        progress = []
        colors_list = []
        
        for name, subject in tracker.subjects.items():
            if subject.goal_hours > 0:
                subjects_with_goals.append(name)
                prog = subject.get_progress_percentage()
                progress.append(min(prog, 100))
                colors_list.append('#6bcf7f' if prog >= 80 else '#ffd93d' if prog >= 50 else '#ff6b6b')
        
        if subjects_with_goals:
            y_pos = np.arange(len(subjects_with_goals))
            ax4.barh(y_pos, progress, color=colors_list)
            ax4.set_yticks(y_pos)
            ax4.set_yticklabels(subjects_with_goals)
            ax4.set_xlabel('Progress (%)')
            ax4.set_title('Goal Progress', fontweight='bold')
            ax4.set_xlim(0, 100)
            for i, v in enumerate(progress):
                ax4.text(v + 2, i, f'{v:.1f}%', va='center')
        
        fig.suptitle('Study Tracker Dashboard', fontsize=16, fontweight='bold')
        
        return fig
