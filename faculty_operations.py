"""
Faculty operations module for Campus Hub Portal
Handles faculty operations like viewing student submissions and grading
"""

import sqlite3
from database import Database


class FacultyOperations:
    def __init__(self, faculty_id):
        self.faculty_id = faculty_id
        self.db = Database()
    
    def assign_student(self, student_id):
        """Assign a student to this faculty for assistance"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT * FROM users WHERE user_id = ? AND role = 'student'", (student_id,))
            if not cursor.fetchone():
                self.db.close()
                return False, "Student not found"
            
            # Check if already assigned
            cursor.execute(
                "SELECT * FROM faculty_assignments WHERE faculty_id = ? AND student_id = ?",
                (self.faculty_id, student_id)
            )
            if cursor.fetchone():
                self.db.close()
                return False, "Student already assigned to you"
            
            # Assign student
            cursor.execute(
                "INSERT INTO faculty_assignments (faculty_id, student_id) VALUES (?, ?)",
                (self.faculty_id, student_id)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Student {student_id} assigned successfully!"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Error assigning student: {str(e)}"
    
    def list_all_students(self):
        """List all students in the system"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_id, name, username, email FROM users WHERE role = 'student'")
            students = cursor.fetchall()
            self.db.close()
            
            return [dict(s) for s in students]
        
        except sqlite3.Error as e:
            self.db.close()
            return []
    
    def list_my_students(self):
        """List students assigned to this faculty"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT u.user_id, u.name, u.username, u.email 
                   FROM users u
                   JOIN faculty_assignments fa ON u.user_id = fa.student_id
                   WHERE fa.faculty_id = ?""",
                (self.faculty_id,)
            )
            students = cursor.fetchall()
            self.db.close()
            
            return [dict(s) for s in students]
        
        except sqlite3.Error as e:
            self.db.close()
            return []
    
    def view_student_submissions(self, student_id):
        """View all submissions by a specific student"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if student is assigned to this faculty
            cursor.execute(
                "SELECT * FROM faculty_assignments WHERE faculty_id = ? AND student_id = ?",
                (self.faculty_id, student_id)
            )
            if not cursor.fetchone():
                self.db.close()
                return None, "Student not assigned to you"
            
            # Get projects
            cursor.execute(
                "SELECT * FROM projects WHERE student_id = ?",
                (student_id,)
            )
            projects = cursor.fetchall()
            
            # Get internships
            cursor.execute(
                "SELECT * FROM internships WHERE student_id = ?",
                (student_id,)
            )
            internships = cursor.fetchall()
            
            # Get seminars
            cursor.execute(
                "SELECT * FROM seminars WHERE student_id = ?",
                (student_id,)
            )
            seminars = cursor.fetchall()
            
            self.db.close()
            
            return {
                'projects': [dict(p) for p in projects],
                'internships': [dict(i) for i in internships],
                'seminars': [dict(s) for s in seminars]
            }, None
        
        except sqlite3.Error as e:
            self.db.close()
            return None, f"Error viewing submissions: {str(e)}"
    
    def grade_submission(self, submission_type, submission_id, marks):
        """Grade a student submission (project/internship/seminar)"""
        try:
            if marks < 0 or marks > 100:
                return False, "Marks must be between 0 and 100"
            
            conn = self.db.connect()
            cursor = conn.cursor()
            
            table_map = {
                'project': 'projects',
                'internship': 'internships',
                'seminar': 'seminars'
            }
            
            table = table_map.get(submission_type)
            if not table:
                self.db.close()
                return False, "Invalid submission type"
            
            id_field = f"{submission_type}_id"
            
            # Check if submission exists and student is assigned
            cursor.execute(
                f"""SELECT s.student_id FROM {table} s
                    JOIN faculty_assignments fa ON s.student_id = fa.student_id
                    WHERE s.{id_field} = ? AND fa.faculty_id = ?""",
                (submission_id, self.faculty_id)
            )
            
            if not cursor.fetchone():
                self.db.close()
                return False, "Submission not found or student not assigned to you"
            
            # Update marks
            cursor.execute(
                f"UPDATE {table} SET marks = ?, graded_by = ? WHERE {id_field} = ?",
                (marks, self.faculty_id, submission_id)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Marks updated successfully! {marks}/100"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Error grading submission: {str(e)}"
