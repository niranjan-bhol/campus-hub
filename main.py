#!/usr/bin/env python3
"""
Campus Hub Portal - Main CLI Application
Terminal-based interface for managing projects, internships, and seminars
"""

import os
import sys
from database import init_db
from auth import AuthManager
from student_operations import StudentOperations
from faculty_operations import FacultyOperations


class CampusHubCLI:
    def __init__(self):
        self.auth = AuthManager()
        self.current_user = None
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_menu(self, options):
        """Print menu options"""
        print()
        for key, value in options.items():
            print(f"  {key}. {value}")
        print()
    
    def get_input(self, prompt):
        """Get user input with prompt"""
        return input(f"➤ {prompt}: ").strip()
    
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_screen()
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 15 + "CAMPUS HUB PORTAL" + " " * 26 + "║")
        print("║" + " " * 10 + "Project | Internship | Seminar Manager" + " " * 10 + "║")
        print("╚" + "═" * 58 + "╝\n")
    
    def role_selection(self):
        """Select role (Student/Faculty)"""
        self.show_welcome()
        self.print_header("SELECT YOUR ROLE")
        self.print_menu({
            "1": "Student",
            "2": "Faculty",
            "3": "Exit"
        })
        
        choice = self.get_input("Enter choice")
        
        if choice == "1":
            return "student"
        elif choice == "2":
            return "faculty"
        elif choice == "3":
            print("\n👋 Thank you for using Campus Hub Portal!")
            sys.exit(0)
        else:
            print("❌ Invalid choice!")
            input("\nPress Enter to continue...")
            return None
    
    def auth_menu(self, role):
        """Authentication menu (Register/Login)"""
        self.clear_screen()
        self.print_header(f"{role.upper()} - AUTHENTICATION")
        self.print_menu({
            "1": "Register",
            "2": "Login",
            "3": "Back to Role Selection"
        })
        
        choice = self.get_input("Enter choice")
        
        if choice == "1":
            self.register(role)
        elif choice == "2":
            self.login(role)
        elif choice == "3":
            return
        else:
            print("❌ Invalid choice!")
            input("\nPress Enter to continue...")
    
    def register(self, role):
        """Handle user registration"""
        self.clear_screen()
        self.print_header(f"{role.upper()} REGISTRATION")
        
        print("\n📝 Enter your details:\n")
        name = self.get_input("Full Name")
        username = self.get_input("Username")
        email = self.get_input("Email")
        password = self.get_input("Password")
        
        if not all([name, username, email, password]):
            print("\n❌ All fields are required!")
            input("\nPress Enter to continue...")
            return
        
        success, message = self.auth.register_user(name, username, email, password, role)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def login(self, role):
        """Handle user login"""
        self.clear_screen()
        self.print_header(f"{role.upper()} LOGIN")
        
        print("\n🔐 Enter your credentials:\n")
        identifier = self.get_input("Email or Username")
        password = self.get_input("Password")
        
        if not all([identifier, password]):
            print("\n❌ All fields are required!")
            input("\nPress Enter to continue...")
            return
        
        success, result = self.auth.login_user(identifier, password, role)
        
        if success:
            self.current_user = result
            print(f"\n✓ Welcome, {result['name']}!")
            input("\nPress Enter to continue...")
            
            if role == "student":
                self.student_dashboard()
            else:
                self.faculty_dashboard()
        else:
            print(f"\n❌ {result}")
            input("\nPress Enter to continue...")
    
    def student_dashboard(self):
        """Student dashboard"""
        student_ops = StudentOperations(self.current_user['user_id'])
        
        while True:
            self.clear_screen()
            self.print_header(f"STUDENT DASHBOARD - {self.current_user['name']}")
            print(f"User ID: {self.current_user['user_id']}")
            
            self.print_menu({
                "1": "Submit Project",
                "2": "Apply for Internship",
                "3": "Present Seminar",
                "4": "View My Submissions",
                "5": "Logout"
            })
            
            choice = self.get_input("Enter choice")
            
            if choice == "1":
                self.submit_project(student_ops)
            elif choice == "2":
                self.apply_internship(student_ops)
            elif choice == "3":
                self.present_seminar(student_ops)
            elif choice == "4":
                self.view_submissions(student_ops)
            elif choice == "5":
                self.current_user = None
                print("\n✓ Logged out successfully!")
                input("\nPress Enter to continue...")
                break
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
    
    def submit_project(self, student_ops):
        """Submit a project"""
        self.clear_screen()
        self.print_header("SUBMIT PROJECT")
        
        print("\n📋 Enter project details:\n")
        title = self.get_input("Project Title")
        description = self.get_input("Description")
        start_date = self.get_input("Start Date (YYYY-MM-DD)")
        end_date = self.get_input("End Date (YYYY-MM-DD)")
        status = self.get_input("Status (e.g., In Progress, Completed)")
        github_link = self.get_input("GitHub Link")
        live_link = self.get_input("Live Project Link")
        
        if not title:
            print("\n❌ Project title is required!")
            input("\nPress Enter to continue...")
            return
        
        success, message = student_ops.submit_project(
            title, description, start_date, end_date, status, github_link, live_link
        )
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def apply_internship(self, student_ops):
        """Apply for internship"""
        self.clear_screen()
        self.print_header("APPLY FOR INTERNSHIP")
        
        print("\n💼 Enter internship details:\n")
        company = self.get_input("Company Name")
        position = self.get_input("Position")
        start_date = self.get_input("Start Date (YYYY-MM-DD)")
        end_date = self.get_input("End Date (YYYY-MM-DD)")
        status = self.get_input("Status (e.g., Applied, Ongoing, Completed)")
        
        if not all([company, position]):
            print("\n❌ Company name and position are required!")
            input("\nPress Enter to continue...")
            return
        
        success, message = student_ops.apply_internship(
            company, position, start_date, end_date, status or "Applied"
        )
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def present_seminar(self, student_ops):
        """Register seminar presentation"""
        self.clear_screen()
        self.print_header("REGISTER SEMINAR PRESENTATION")
        
        print("\n🎤 Enter seminar details:\n")
        topic = self.get_input("Seminar Topic")
        description = self.get_input("Description")
        seminar_date = self.get_input("Seminar Date (YYYY-MM-DD)")
        venue = self.get_input("Venue")
        
        if not topic:
            print("\n❌ Seminar topic is required!")
            input("\nPress Enter to continue...")
            return
        
        success, message = student_ops.present_seminar(
            topic, description, seminar_date, venue
        )
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def view_submissions(self, student_ops):
        """View student's own submissions"""
        self.clear_screen()
        self.print_header("MY SUBMISSIONS")
        
        submissions = student_ops.view_my_submissions()
        
        if not submissions:
            print("\n❌ Error fetching submissions!")
            input("\nPress Enter to continue...")
            return
        
        # Display Projects
        print("\n📁 PROJECTS:")
        if submissions['projects']:
            for proj in submissions['projects']:
                print(f"\n  ID: {proj['project_id']}")
                print(f"  Title: {proj['title']}")
                print(f"  Status: {proj['status']}")
                print(f"  Marks: {proj['marks'] if proj['marks'] else 'Not graded'}")
                if proj['marks']:
                    print(f"  Graded by: {proj['graded_by']}")
                print(f"  GitHub: {proj['github_link']}")
                print("  " + "-" * 50)
        else:
            print("  No projects submitted yet.")
        
        # Display Internships
        print("\n💼 INTERNSHIPS:")
        if submissions['internships']:
            for intern in submissions['internships']:
                print(f"\n  ID: {intern['internship_id']}")
                print(f"  Company: {intern['company_name']}")
                print(f"  Position: {intern['position']}")
                print(f"  Status: {intern['status']}")
                print(f"  Marks: {intern['marks'] if intern['marks'] else 'Not graded'}")
                if intern['marks']:
                    print(f"  Graded by: {intern['graded_by']}")
                print("  " + "-" * 50)
        else:
            print("  No internships applied yet.")
        
        # Display Seminars
        print("\n🎤 SEMINARS:")
        if submissions['seminars']:
            for sem in submissions['seminars']:
                print(f"\n  ID: {sem['seminar_id']}")
                print(f"  Topic: {sem['topic']}")
                print(f"  Date: {sem['seminar_date']}")
                print(f"  Venue: {sem['venue']}")
                print(f"  Marks: {sem['marks'] if sem['marks'] else 'Not graded'}")
                if sem['marks']:
                    print(f"  Graded by: {sem['graded_by']}")
                print("  " + "-" * 50)
        else:
            print("  No seminars registered yet.")
        
        input("\nPress Enter to continue...")
    
    def faculty_dashboard(self):
        """Faculty dashboard"""
        faculty_ops = FacultyOperations(self.current_user['user_id'])
        
        while True:
            self.clear_screen()
            self.print_header(f"FACULTY DASHBOARD - {self.current_user['name']}")
            print(f"User ID: {self.current_user['user_id']}")
            
            self.print_menu({
                "1": "Assign Student",
                "2": "View My Students",
                "3": "View Student Submissions",
                "4": "Grade Submission",
                "5": "List All Students",
                "6": "Logout"
            })
            
            choice = self.get_input("Enter choice")
            
            if choice == "1":
                self.assign_student(faculty_ops)
            elif choice == "2":
                self.view_my_students(faculty_ops)
            elif choice == "3":
                self.view_student_submissions_menu(faculty_ops)
            elif choice == "4":
                self.grade_submission(faculty_ops)
            elif choice == "5":
                self.list_all_students(faculty_ops)
            elif choice == "6":
                self.current_user = None
                print("\n✓ Logged out successfully!")
                input("\nPress Enter to continue...")
                break
            else:
                print("❌ Invalid choice!")
                input("\nPress Enter to continue...")
    
    def assign_student(self, faculty_ops):
        """Assign a student to faculty"""
        self.clear_screen()
        self.print_header("ASSIGN STUDENT")
        
        print("\n👥 Enter student details:\n")
        student_id = self.get_input("Student ID (e.g., student_1)")
        
        if not student_id:
            print("\n❌ Student ID is required!")
            input("\nPress Enter to continue...")
            return
        
        success, message = faculty_ops.assign_student(student_id)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def view_my_students(self, faculty_ops):
        """View students assigned to faculty"""
        self.clear_screen()
        self.print_header("MY ASSIGNED STUDENTS")
        
        students = faculty_ops.list_my_students()
        
        if students:
            print("\n👥 Your assigned students:\n")
            for student in students:
                print(f"  ID: {student['user_id']}")
                print(f"  Name: {student['name']}")
                print(f"  Username: {student['username']}")
                print(f"  Email: {student['email']}")
                print("  " + "-" * 50)
        else:
            print("\n📝 No students assigned yet.")
        
        input("\nPress Enter to continue...")
    
    def list_all_students(self, faculty_ops):
        """List all students in the system"""
        self.clear_screen()
        self.print_header("ALL STUDENTS")
        
        students = faculty_ops.list_all_students()
        
        if students:
            print("\n👥 All registered students:\n")
            for student in students:
                print(f"  ID: {student['user_id']}")
                print(f"  Name: {student['name']}")
                print(f"  Username: {student['username']}")
                print(f"  Email: {student['email']}")
                print("  " + "-" * 50)
        else:
            print("\n📝 No students registered yet.")
        
        input("\nPress Enter to continue...")
    
    def view_student_submissions_menu(self, faculty_ops):
        """View submissions of a specific student"""
        self.clear_screen()
        self.print_header("VIEW STUDENT SUBMISSIONS")
        
        print("\n📋 Enter student details:\n")
        student_id = self.get_input("Student ID")
        
        if not student_id:
            print("\n❌ Student ID is required!")
            input("\nPress Enter to continue...")
            return
        
        result, error = faculty_ops.view_student_submissions(student_id)
        
        if error:
            print(f"\n❌ {error}")
            input("\nPress Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header(f"SUBMISSIONS - {student_id}")
        
        # Display Projects
        print("\n📁 PROJECTS:")
        if result['projects']:
            for proj in result['projects']:
                print(f"\n  ID: {proj['project_id']}")
                print(f"  Title: {proj['title']}")
                print(f"  Description: {proj['description']}")
                print(f"  Status: {proj['status']}")
                print(f"  Start: {proj['start_date']} | End: {proj['end_date']}")
                print(f"  GitHub: {proj['github_link']}")
                print(f"  Live: {proj['live_link']}")
                print(f"  Marks: {proj['marks'] if proj['marks'] else 'Not graded'}")
                print("  " + "-" * 50)
        else:
            print("  No projects submitted.")
        
        # Display Internships
        print("\n💼 INTERNSHIPS:")
        if result['internships']:
            for intern in result['internships']:
                print(f"\n  ID: {intern['internship_id']}")
                print(f"  Company: {intern['company_name']}")
                print(f"  Position: {intern['position']}")
                print(f"  Status: {intern['status']}")
                print(f"  Start: {intern['start_date']} | End: {intern['end_date']}")
                print(f"  Marks: {intern['marks'] if intern['marks'] else 'Not graded'}")
                print("  " + "-" * 50)
        else:
            print("  No internships applied.")
        
        # Display Seminars
        print("\n🎤 SEMINARS:")
        if result['seminars']:
            for sem in result['seminars']:
                print(f"\n  ID: {sem['seminar_id']}")
                print(f"  Topic: {sem['topic']}")
                print(f"  Description: {sem['description']}")
                print(f"  Date: {sem['seminar_date']}")
                print(f"  Venue: {sem['venue']}")
                print(f"  Marks: {sem['marks'] if sem['marks'] else 'Not graded'}")
                print("  " + "-" * 50)
        else:
            print("  No seminars registered.")
        
        input("\nPress Enter to continue...")
    
    def grade_submission(self, faculty_ops):
        """Grade a student submission"""
        self.clear_screen()
        self.print_header("GRADE SUBMISSION")
        
        print("\n📝 Enter grading details:\n")
        print("Submission types: project, internship, seminar\n")
        
        submission_type = self.get_input("Submission Type").lower()
        submission_id = self.get_input("Submission ID")
        marks = self.get_input("Marks (0-100)")
        
        if not all([submission_type, submission_id, marks]):
            print("\n❌ All fields are required!")
            input("\nPress Enter to continue...")
            return
        
        try:
            marks = int(marks)
        except ValueError:
            print("\n❌ Marks must be a number!")
            input("\nPress Enter to continue...")
            return
        
        success, message = faculty_ops.grade_submission(submission_type, submission_id, marks)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        # Initialize database
        init_db()
        
        while True:
            role = self.role_selection()
            if role:
                self.auth_menu(role)


if __name__ == "__main__":
    app = CampusHubCLI()
    app.run()
