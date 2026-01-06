"""
Database module for Productivity Dashboard
Handles all SQLite operations
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json


class Database:
    """SQLite database handler for all productivity data"""
    
    def __init__(self, db_name: str = "productivity.db"):
        """Initialize database connection and create tables"""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                due_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
        ''')
        
        # Habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                frequency TEXT DEFAULT 'daily',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Habit logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                logged_date TEXT,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')
        
        # Mood entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood_score INTEGER,
                mood_emoji TEXT,
                notes TEXT,
                sentiment_score REAL,
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                target_value REAL,
                current_value REAL DEFAULT 0,
                unit TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pomodoro sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                duration_minutes INTEGER DEFAULT 25,
                completed INTEGER DEFAULT 0,
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        self.conn.commit()
    
    # ============ TASK METHODS ============
    
    def add_task(self, title: str, description: str = "", 
                 priority: str = "medium", due_date: str = None) -> int:
        """Add a new task and return its ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, due_date)
            VALUES (?, ?, ?, ?)
        ''', (title, description, priority, due_date))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_tasks(self, status: str = None) -> List[Dict]:
        """Get all tasks, optionally filtered by status"""
        cursor = self.conn.cursor()
        if status:
            cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str):
        """Update task status (pending, in_progress, completed)"""
        cursor = self.conn.cursor()
        completed_at = datetime.now().isoformat() if status == 'completed' else None
        cursor.execute('''
            UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?
        ''', (status, completed_at, task_id))
        self.conn.commit()
    
    def delete_task(self, task_id: int):
        """Delete a task by ID"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
    
    # ============ HABIT METHODS ============
    
    def add_habit(self, name: str, description: str = "", 
                  frequency: str = "daily") -> int:
        """Add a new habit to track"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO habits (name, description, frequency)
            VALUES (?, ?, ?)
        ''', (name, description, frequency))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_habits(self) -> List[Dict]:
        """Get all habits with their current streak"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM habits ORDER BY created_at DESC')
        habits = [dict(row) for row in cursor.fetchall()]
        
        # Calculate streak for each habit
        for habit in habits:
            habit['streak'] = self.calculate_streak(habit['id'])
            habit['completed_today'] = self.is_habit_completed_today(habit['id'])
        
        return habits
    
    def log_habit(self, habit_id: int, logged_date: str = None):
        """Log a habit completion for a specific date"""
        if logged_date is None:
            logged_date = date.today().isoformat()
        
        cursor = self.conn.cursor()
        # Check if already logged
        cursor.execute('''
            SELECT id FROM habit_logs 
            WHERE habit_id = ? AND logged_date = ?
        ''', (habit_id, logged_date))
        
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO habit_logs (habit_id, logged_date, completed)
                VALUES (?, ?, 1)
            ''', (habit_id, logged_date))
            self.conn.commit()
    
    def is_habit_completed_today(self, habit_id: int) -> bool:
        """Check if habit is completed today"""
        cursor = self.conn.cursor()
        today = date.today().isoformat()
        cursor.execute('''
            SELECT id FROM habit_logs 
            WHERE habit_id = ? AND logged_date = ? AND completed = 1
        ''', (habit_id, today))
        return cursor.fetchone() is not None
    
    def calculate_streak(self, habit_id: int) -> int:
        """Calculate current streak for a habit"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT logged_date FROM habit_logs 
            WHERE habit_id = ? AND completed = 1
            ORDER BY logged_date DESC
        ''', (habit_id,))
        
        logs = cursor.fetchall()
        if not logs:
            return 0
        
        streak = 0
        current_date = date.today()
        
        for log in logs:
            log_date = date.fromisoformat(log[0])
            expected_date = current_date - timedelta(days=streak)
            
            if log_date == expected_date:
                streak += 1
            elif log_date == expected_date - timedelta(days=1):
                streak += 1
                current_date = log_date + timedelta(days=streak - 1)
            else:
                break
        
        return streak
    
    def delete_habit(self, habit_id: int):
        """Delete a habit and its logs"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.conn.commit()
    
    # ============ MOOD METHODS ============
    
    def add_mood_entry(self, mood_score: int, mood_emoji: str, 
                       notes: str = "", sentiment_score: float = 0.0) -> int:
        """Add a mood entry with optional notes"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO mood_entries (mood_score, mood_emoji, notes, sentiment_score)
            VALUES (?, ?, ?, ?)
        ''', (mood_score, mood_emoji, notes, sentiment_score))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_mood_entries(self, days: int = 30) -> List[Dict]:
        """Get mood entries for the last N days"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM mood_entries 
            ORDER BY logged_at DESC 
            LIMIT ?
        ''', (days,))
        return [dict(row) for row in cursor.fetchall()]
    
    # ============ GOAL METHODS ============
    
    def add_goal(self, title: str, target_value: float, unit: str,
                 description: str = "", deadline: str = None) -> int:
        """Add a new goal"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO goals (title, description, target_value, unit, deadline)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, target_value, unit, deadline))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_goals(self, status: str = "active") -> List[Dict]:
        """Get all goals with progress percentage"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM goals WHERE status = ?
            ORDER BY created_at DESC
        ''', (status,))
        goals = [dict(row) for row in cursor.fetchall()]
        
        for goal in goals:
            if goal['target_value'] > 0:
                goal['progress'] = min(100, (goal['current_value'] / goal['target_value']) * 100)
            else:
                goal['progress'] = 0
        
        return goals
    
    def update_goal_progress(self, goal_id: int, current_value: float):
        """Update goal progress"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE goals SET current_value = ? WHERE id = ?
        ''', (current_value, goal_id))
        self.conn.commit()
    
    def delete_goal(self, goal_id: int):
        """Delete a goal"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
        self.conn.commit()
    
    # ============ ANALYTICS METHODS ============
    
    def get_productivity_stats(self) -> Dict:
        """Get overall productivity statistics"""
        cursor = self.conn.cursor()
        
        # Task stats
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
        completed_tasks = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = cursor.fetchone()[0]
        
        # Habit stats
        cursor.execute('SELECT COUNT(*) FROM habit_logs WHERE completed = 1')
        total_habit_completions = cursor.fetchone()[0]
        
        # Mood average
        cursor.execute('SELECT AVG(mood_score) FROM mood_entries')
        avg_mood = cursor.fetchone()[0] or 0
        
        # Goals stats
        cursor.execute('SELECT COUNT(*) FROM goals WHERE status = "active"')
        active_goals = cursor.fetchone()[0]
        
        return {
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'total_habit_completions': total_habit_completions,
            'average_mood': round(avg_mood, 1),
            'active_goals': active_goals
        }
    
    def get_weekly_activity(self) -> Dict:
        """Get activity data for the past week"""
        cursor = self.conn.cursor()
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        # Tasks completed this week
        cursor.execute('''
            SELECT DATE(completed_at) as day, COUNT(*) as count
            FROM tasks 
            WHERE completed_at >= ? AND status = 'completed'
            GROUP BY DATE(completed_at)
        ''', (week_ago,))
        tasks_by_day = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Habits completed this week
        cursor.execute('''
            SELECT logged_date, COUNT(*) as count
            FROM habit_logs 
            WHERE logged_date >= ?
            GROUP BY logged_date
        ''', (week_ago[:10],))
        habits_by_day = {row[0]: row[1] for row in cursor.fetchall()}
        
        return {
            'tasks_by_day': tasks_by_day,
            'habits_by_day': habits_by_day
        }


# Test the database if run directly
if __name__ == "__main__":
    db = Database()
    print("✅ Database created successfully!")
    print("✅ All tables initialized!")
    
    # Test adding a task
    task_id = db.add_task("Test Task", "This is a test", "high")
    print(f"✅ Test task created with ID: {task_id}")
    
    # Clean up test
    db.delete_task(task_id)
    print("✅ Test task deleted")
    print("\n🎉 Database is working correctly!")