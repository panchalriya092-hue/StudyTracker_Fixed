"""
Study Tracker Module
Demonstrates: OOP, Exception Handling, File Operations, Data Structures
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np


class StudySession:
    """Represents a single study session (Immutable after creation)"""
    
    def __init__(self, subject: str, topic: str, duration: int, date: str, notes: str = ""):
        self._subject = subject
        self._topic = topic
        self._duration = duration  # in minutes
        self._date = date
        self._notes = notes
        self._timestamp = datetime.now().isoformat()
    
    # Properties (Encapsulation)
    @property
    def subject(self) -> str:
        return self._subject
    
    @property
    def topic(self) -> str:
        return self._topic
    
    @property
    def duration(self) -> int:
        return self._duration
    
    @property
    def date(self) -> str:
        return self._date
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @property
    def timestamp(self) -> str:
        return self._timestamp
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            'subject': self._subject,
            'topic': self._topic,
            'duration': self._duration,
            'date': self._date,
            'notes': self._notes,
            'timestamp': self._timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create StudySession from dictionary"""
        session = cls(
            data['subject'],
            data['topic'],
            data['duration'],
            data['date'],
            data.get('notes', '')
        )
        session._timestamp = data.get('timestamp', datetime.now().isoformat())
        return session
    
    def __str__(self) -> str:
        return f"{self.subject} - {self.topic} ({self.duration} min) on {self.date}"
    
    def __repr__(self) -> str:
        return f"StudySession(subject='{self.subject}', topic='{self.topic}', duration={self.duration})"


class Subject:
    """Represents a subject with goals and sessions"""
    
    def __init__(self, name: str, goal_hours: int = 0):
        self.name = name
        self.goal_hours = goal_hours
        self.sessions: List[StudySession] = []
        self.topics_covered = set()  # Using set for unique topics
    
    def add_session(self, session: StudySession) -> None:
        """Add a study session"""
        if session.subject != self.name:
            raise ValueError(f"Session subject '{session.subject}' doesn't match '{self.name}'")
        
        self.sessions.append(session)
        self.topics_covered.add(session.topic)
    
    def get_total_hours(self) -> float:
        """Calculate total study hours"""
        total_minutes = sum(session.duration for session in self.sessions)
        return round(total_minutes / 60, 2)
    
    def get_progress_percentage(self) -> float:
        """Get progress towards goal"""
        if self.goal_hours == 0:
            return 0.0
        return round((self.get_total_hours() / self.goal_hours) * 100, 2)
    
    def get_sessions_by_date_range(self, start_date: str, end_date: str) -> List[StudySession]:
        """Filter sessions by date range"""
        return [
            session for session in self.sessions
            if start_date <= session.date <= end_date
        ]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'goal_hours': self.goal_hours,
            'sessions': [session.to_dict() for session in self.sessions],
            'topics_covered': list(self.topics_covered)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Subject from dictionary"""
        subject = cls(data['name'], data.get('goal_hours', 0))
        subject.sessions = [StudySession.from_dict(s) for s in data.get('sessions', [])]
        subject.topics_covered = set(data.get('topics_covered', []))
        return subject


class StudyTracker:
    """Main Study Tracker class with file persistence"""
    
    DATA_FILE = "study_data.json"
    
    def __init__(self, data_directory: str = "."):
        self.data_directory = data_directory
        self.data_file_path = os.path.join(data_directory, self.DATA_FILE)
        self.subjects: Dict[str, Subject] = {}
        self.load_data()
    
    def add_subject(self, name: str, goal_hours: int = 0) -> None:
        """Add a new subject"""
        if name in self.subjects:
            raise ValueError(f"Subject '{name}' already exists")
        
        self.subjects[name] = Subject(name, goal_hours)
        self.save_data()
    
    def remove_subject(self, name: str) -> None:
        """Remove a subject"""
        if name not in self.subjects:
            raise KeyError(f"Subject '{name}' not found")
        
        del self.subjects[name]
        self.save_data()
    
    def add_study_session(self, subject: str, topic: str, duration: int, 
                         date: str, notes: str = "") -> None:
        """Add a study session"""
        if subject not in self.subjects:
            raise KeyError(f"Subject '{subject}' not found. Please add it first.")
        
        if duration <= 0:
            raise ValueError("Duration must be positive")
        
        session = StudySession(subject, topic, duration, date, notes)
        self.subjects[subject].add_session(session)
        self.save_data()
    
    def get_subject(self, name: str) -> Optional[Subject]:
        """Get a subject by name"""
        return self.subjects.get(name)
    
    def get_all_subjects(self) -> List[str]:
        """Get list of all subject names"""
        return list(self.subjects.keys())
    
    def get_total_study_time(self) -> float:
        """Get total study time across all subjects"""
        return sum(subject.get_total_hours() for subject in self.subjects.values())
    
    def get_study_statistics(self) -> Dict:
        """Get comprehensive study statistics using NumPy"""
        if not self.subjects:
            return {
                'total_hours': 0,
                'total_sessions': 0,
                'avg_session_duration': 0,
                'subjects_count': 0
            }
        
        all_durations = []
        total_sessions = 0
        
        for subject in self.subjects.values():
            durations = [s.duration for s in subject.sessions]
            all_durations.extend(durations)
            total_sessions += len(subject.sessions)
        
        if not all_durations:
            return {
                'total_hours': 0,
                'total_sessions': 0,
                'avg_session_duration': 0,
                'subjects_count': len(self.subjects)
            }
        
        durations_array = np.array(all_durations)
        
        return {
            'total_hours': round(np.sum(durations_array) / 60, 2),
            'total_sessions': total_sessions,
            'avg_session_duration': round(np.mean(durations_array), 2),
            'median_session_duration': round(np.median(durations_array), 2),
            'std_session_duration': round(np.std(durations_array), 2),
            'min_session_duration': int(np.min(durations_array)),
            'max_session_duration': int(np.max(durations_array)),
            'subjects_count': len(self.subjects)
        }
    
    def get_recent_sessions(self, days: int = 7) -> List[StudySession]:
        """Get sessions from the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_sessions = []
        
        for subject in self.subjects.values():
            for session in subject.sessions:
                if session.date >= cutoff_date:
                    recent_sessions.append(session)
        
        return sorted(recent_sessions, key=lambda s: s.date, reverse=True)
    
    def save_data(self) -> None:
        """Save data to JSON file"""
        try:
            data = {
                'subjects': {
                    name: subject.to_dict() 
                    for name, subject in self.subjects.items()
                },
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except IOError as e:
            raise IOError(f"Error saving data: {e}")
    
    def load_data(self) -> None:
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file_path):
                with open(self.data_file_path, 'r') as f:
                    data = json.load(f)
                
                self.subjects = {
                    name: Subject.from_dict(subject_data)
                    for name, subject_data in data.get('subjects', {}).items()
                }
            else:
                self.subjects = {}
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")
        except IOError as e:
            raise IOError(f"Error loading data: {e}")
    
    def export_to_csv(self, filename: str) -> None:
        """Export all sessions to CSV file"""
        import csv
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Subject', 'Topic', 'Duration (min)', 'Date', 'Notes'])
                
                for subject in self.subjects.values():
                    for session in subject.sessions:
                        writer.writerow([
                            session.subject,
                            session.topic,
                            session.duration,
                            session.date,
                            session.notes
                        ])
        except IOError as e:
            raise IOError(f"Error exporting to CSV: {e}")
    
    def search_sessions(self, keyword: str) -> List[StudySession]:
        """Search sessions by keyword in topic or notes"""
        keyword_lower = keyword.lower()
        results = []
        
        for subject in self.subjects.values():
            for session in subject.sessions:
                if (keyword_lower in session.topic.lower() or 
                    keyword_lower in session.notes.lower()):
                    results.append(session)
        
        return results
    
    def __str__(self) -> str:
        return f"StudyTracker with {len(self.subjects)} subjects and {sum(len(s.sessions) for s in self.subjects.values())} sessions"
    
    def __repr__(self) -> str:
        return f"StudyTracker(subjects={list(self.subjects.keys())})"


# Utility functions demonstrating functional programming
def calculate_study_streak(sessions: List[StudySession]) -> int:
    """Calculate current study streak in days"""
    if not sessions:
        return 0
    
    # Sort sessions by date
    sorted_sessions = sorted(sessions, key=lambda s: s.date, reverse=True)
    dates = [s.date for s in sorted_sessions]
    unique_dates = sorted(set(dates), reverse=True)
    
    if not unique_dates:
        return 0
    
    today = datetime.now().date()
    streak = 0
    
    for i, date_str in enumerate(unique_dates):
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        expected_date = today - timedelta(days=i)
        
        if date == expected_date:
            streak += 1
        else:
            break
    
    return streak


def get_productivity_score(subject: Subject) -> float:
    """Calculate productivity score based on consistency and volume"""
    if not subject.sessions:
        return 0.0
    
    total_hours = subject.get_total_hours()
    sessions_count = len(subject.sessions)
    avg_duration = np.mean([s.duration for s in subject.sessions])
    
    # Score based on total time (40%), consistency (40%), and average session length (20%)
    time_score = min(total_hours / subject.goal_hours, 1.0) * 40 if subject.goal_hours > 0 else 0
    consistency_score = min(sessions_count / 30, 1.0) * 40  # Assuming 30 sessions is excellent
    duration_score = min(avg_duration / 60, 1.0) * 20  # 60 min average is ideal
    
    return round(time_score + consistency_score + duration_score, 2)
