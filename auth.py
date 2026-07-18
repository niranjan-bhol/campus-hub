"""
Authentication module for Campus Hub Portal
Handles user registration and login
"""

import hashlib
import sqlite3
from database import Database


class AuthManager:
    def __init__(self):
        self.db = Database()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, name, username, email, password, role):
        """Register a new user (student or faculty)"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?",
                (username, email)
            )
            if cursor.fetchone():
                self.db.close()
                return False, "Username or email already exists"
            
            # Generate progressive user ID
            user_id = self.db.get_next_user_id(role)
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert user
            cursor.execute(
                """INSERT INTO users (user_id, name, username, email, password, role)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, name, username, email, hashed_password, role)
            )
            
            conn.commit()
            self.db.close()
            return True, f"Registration successful! Your User ID: {user_id}"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Database error: {str(e)}"
    
    def login_user(self, identifier, password, role):
        """Login user with email/username and password"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            # Check if identifier is email or username
            cursor.execute(
                """SELECT * FROM users 
                   WHERE (username = ? OR email = ?) 
                   AND password = ? 
                   AND role = ?""",
                (identifier, identifier, hashed_password, role)
            )
            
            user = cursor.fetchone()
            self.db.close()
            
            if user:
                return True, {
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            else:
                return False, "Invalid credentials or role mismatch"
        
        except sqlite3.Error as e:
            self.db.close()
            return False, f"Database error: {str(e)}"
    
    def get_user_by_id(self, user_id):
        """Get user information by user ID"""
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            self.db.close()
            
            if user:
                return {
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            return None
        
        except sqlite3.Error as e:
            self.db.close()
            return None
