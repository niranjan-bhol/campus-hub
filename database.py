"""
Database module for Campus Hub Portal
Handles database initialization, schema creation, and basic operations
"""

import sqlite3
from datetime import datetime
import os

DB_NAME = "campus_hub.db"


class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def initialize_database(self):
        """Create all necessary tables"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Users table (for both students and faculty)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'faculty')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                start_date DATE,
                end_date DATE,
                status TEXT DEFAULT 'In Progress',
                github_link TEXT,
                live_link TEXT,
                marks INTEGER,
                graded_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(user_id),
                FOREIGN KEY (graded_by) REFERENCES users(user_id)
            )
        """)
        
        # Internships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internships (
                internship_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                position TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                status TEXT DEFAULT 'Applied',
                marks INTEGER,
                graded_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(user_id),
                FOREIGN KEY (graded_by) REFERENCES users(user_id)
            )
        """)
        
        # Seminars table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seminars (
                seminar_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                description TEXT,
                seminar_date DATE,
                venue TEXT,
                marks INTEGER,
                graded_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(user_id),
                FOREIGN KEY (graded_by) REFERENCES users(user_id)
            )
        """)
        
        # Faculty-Student assignments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty_id TEXT NOT NULL,
                student_id TEXT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (faculty_id) REFERENCES users(user_id),
                FOREIGN KEY (student_id) REFERENCES users(user_id),
                UNIQUE(faculty_id, student_id)
            )
        """)
        
        conn.commit()
        self.close()
        print("✓ Database initialized successfully!")
    
    def get_next_user_id(self, role):
        """Generate next progressive user ID"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id FROM users WHERE role = ? ORDER BY id DESC LIMIT 1",
            (role,)
        )
        result = cursor.fetchone()
        self.close()
        
        if result:
            last_id = result[0]
            num = int(last_id.split('_')[1]) + 1
        else:
            num = 1
        
        return f"{role}_{num}"
    
    def get_next_submission_id(self, submission_type, student_id):
        """Generate next progressive submission ID"""
        conn = self.connect()
        cursor = conn.cursor()
        
        table_map = {
            'project': 'projects',
            'internship': 'internships',
            'seminar': 'seminars'
        }
        
        table = table_map.get(submission_type)
        id_field = f"{submission_type}_id"
        
        cursor.execute(
            f"SELECT {id_field} FROM {table} WHERE student_id = ? ORDER BY created_at DESC LIMIT 1",
            (student_id,)
        )
        result = cursor.fetchone()
        self.close()
        
        if result:
            last_id = result[0]
            num = int(last_id.split('_')[-1]) + 1
        else:
            num = 1
        
        return f"{student_id}_{submission_type}_{num}"


def init_db():
    """Initialize the database"""
    db = Database()
    db.initialize_database()


if __name__ == "__main__":
    init_db()
