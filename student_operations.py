"""
Student operations module for Campus Hub Portal
Handles project submission, internship applications, and seminar presentations
"""

import sqlite3
from database import Database


class StudentOperations:
    def __init__(self, student_id):
        self.student_id = student_id
        self.db = Database()
    
    def submit_project(self, title, description, start_date, end_date, status, github_link, live_link):
        """Submit a new project"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Generate project ID
            project_id = self.db.get_next_submission_id('project', self.student_id)
            
            cursor.execute(
                """INSERT INTO projects 
                   (project_id, student_id, title, description, start_date, end_date, status, github_link, live_link)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (project_id, self.student_id, title, description, start_date, end_date, status, github_link, live_link)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Project submitted successfully! Project ID: {project_id}"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Error submitting project: {str(e)}"
    
    def apply_internship(self, company_name, position, start_date, end_date, status):
        """Apply for an internship"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Generate internship ID
            internship_id = self.db.get_next_submission_id('internship', self.student_id)
            
            cursor.execute(
                """INSERT INTO internships 
                   (internship_id, student_id, company_name, position, start_date, end_date, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (internship_id, self.student_id, company_name, position, start_date, end_date, status)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Internship application submitted! Internship ID: {internship_id}"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Error applying for internship: {str(e)}"
    
    def present_seminar(self, topic, description, seminar_date, venue):
        """Register a seminar presentation"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Generate seminar ID
            seminar_id = self.db.get_next_submission_id('seminar', self.student_id)
            
            cursor.execute(
                """INSERT INTO seminars 
                   (seminar_id, student_id, topic, description, seminar_date, venue)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (seminar_id, self.student_id, topic, description, seminar_date, venue)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Seminar registered successfully! Seminar ID: {seminar_id}"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Error registering seminar: {str(e)}"
    
    def view_my_submissions(self):
        """View all submissions by the student"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Get projects
            cursor.execute(
                "SELECT * FROM projects WHERE student_id = ?",
                (self.student_id,)
            )
            projects = cursor.fetchall()
            
            # Get internships
            cursor.execute(
                "SELECT * FROM internships WHERE student_id = ?",
                (self.student_id,)
            )
            internships = cursor.fetchall()
            
            # Get seminars
            cursor.execute(
                "SELECT * FROM seminars WHERE student_id = ?",
                (self.student_id,)
            )
            seminars = cursor.fetchall()
            
            self.db.close()
            
            return {
                'projects': [dict(p) for p in projects],
                'internships': [dict(i) for i in internships],
                'seminars': [dict(s) for s in seminars]
            }
        
        except sqlite3.Error as e:
            self.db.close()
            return None
