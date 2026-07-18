# Campus Hub Portal 🎓

A comprehensive web portal for managing student projects, internships, and seminars with faculty grading capabilities.

**✨ Now with modern Web UI + Terminal CLI!**

## Features

### For Students:
- ✅ Register and login with unique progressive IDs (student_1, student_2, ...)
- 📁 Submit projects with details (title, description, dates, GitHub/live links)
- 💼 Apply for internships (company, position, dates, status)
- 🎤 Register seminar presentations (topic, description, date, venue)
- 📊 View all submissions and grades

### For Faculty:
- ✅ Register and login with unique progressive IDs (faculty_1, faculty_2, ...)
- 👥 Assign students for assistance
- 📋 View student submissions (projects, internships, seminars)
- 📝 Grade submissions (marks out of 100)
- 📊 Marks visible to both faculty and students

## Technology Stack

- **Language:** Python 3.x
- **Database:** SQLite
- **Interface:** Terminal-based CLI

## Project Structure

```
campus-hub/
├── main.py                   # Main CLI application
├── database.py               # Database schema and operations
├── auth.py                   # User authentication
├── student_operations.py     # Student functionalities
├── faculty_operations.py     # Faculty functionalities
├── campus_hub.db            # SQLite database (auto-generated)
└── README.md                # This file
```

## Installation & Setup

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses built-in libraries)

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd /Users/niranjanbhol/Desktop/campus-hub
   ```

2. **Run the application:**
   ```bash
   python3 main.py
   ```

3. **First time setup:**
   - The database will be automatically initialized on first run
   - You'll see: "✓ Database initialized successfully!"

## 🌐 Deploy to Internet (Free!)

Want to make your campus hub accessible online? Deploy for free!

### Quick Deploy (5 minutes)

**Recommended: Render.com**
```bash
# 1. Push your code (if not already)
./deploy.sh

# 2. Visit https://render.com
# 3. Sign up with GitHub
# 4. Connect campus-hub repository
# 5. Click Deploy - Done!
```

Your app will be live at: `https://campus-hub-xxxx.onrender.com`

### Deployment Options

| Platform | Free? | Database | Setup Time | Best For |
|----------|-------|----------|------------|----------|
| **Render.com** | ✅ Yes | Resets on redeploy | 5 min | Quick demos |
| **PythonAnywhere** | ✅ Yes | Persists ✅ | 15 min | Real campus use |
| **Railway.app** | $5 credit/mo | Persists ✅ | 10 min | Best performance |

**📖 Detailed Guides:**
- [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Step-by-step Render deployment
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - All hosting options
- [HOSTING_COMPARISON.md](HOSTING_COMPARISON.md) - Which to choose?

## Usage Guide

### Getting Started

1. **Select Role:**
   - Choose between Student (1) or Faculty (2)

2. **Register (First Time):**
   - Enter name, username, email, and password
   - System assigns unique ID automatically
   - Note your User ID for reference

3. **Login (Returning Users):**
   - Enter email or username
   - Enter password

### Student Workflow

```
Login → Dashboard → Choose Action:
├── Submit Project
│   └── Enter: title, description, dates, status, links
├── Apply for Internship
│   └── Enter: company, position, dates, status
├── Present Seminar
│   └── Enter: topic, description, date, venue
└── View My Submissions
    └── See all submissions with grades
```

### Faculty Workflow

```
Login → Dashboard → Choose Action:
├── Assign Student
│   └── Enter student ID to assign
├── View My Students
│   └── See list of assigned students
├── View Student Submissions
│   └── See all submissions by a student
├── Grade Submission
│   └── Enter: type, ID, marks (0-100)
└── List All Students
    └── See all registered students
```

## Database Schema

### Tables:

1. **users** - Stores student and faculty accounts
   - Progressive IDs: student_1, student_2, faculty_1, faculty_2, ...

2. **projects** - Student project submissions
   - Auto-generated IDs: student_1_project_1, student_1_project_2, ...

3. **internships** - Internship applications
   - Auto-generated IDs: student_1_internship_1, ...

4. **seminars** - Seminar presentations
   - Auto-generated IDs: student_1_seminar_1, ...

5. **faculty_assignments** - Faculty-student associations

## Example Workflow

### Student Example:
```
1. Register as student → Get ID: student_1
2. Login with credentials
3. Submit a project:
   - Title: "E-commerce Website"
   - GitHub: https://github.com/user/ecommerce
   - Status: Completed
4. View submissions → See project with ID: student_1_project_1
5. Check marks after faculty grades
```

### Faculty Example:
```
1. Register as faculty → Get ID: faculty_1
2. Login with credentials
3. View all students → Find student_1
4. Assign student_1 to assist
5. View student_1's submissions
6. Grade project: student_1_project_1 → 85/100
```

## Database Location

The SQLite database file (`campus_hub.db`) is created in the same directory as the application.

## Security Features

- Passwords are hashed using SHA-256
- Role-based access control
- Faculty can only grade assigned students
- Input validation on all forms

## Future Enhancements (UI Version)

- Web-based UI with HTML/CSS/JavaScript
- File upload for project documentation
- Email notifications
- Advanced reporting and analytics
- Search and filter capabilities
- Batch grading options

## Troubleshooting

**Issue: Database locked error**
- Solution: Close any other instances of the application

**Issue: Invalid credentials**
- Solution: Ensure you're selecting the correct role and using correct email/username

**Issue: Student not found**
- Solution: Faculty must use exact student_id (e.g., student_1)

## Developer Notes

### Testing the Application:

1. **Create test accounts:**
   ```python
   # Register 2 students and 1 faculty
   Student 1: username=john_doe, email=john@example.com
   Student 2: username=jane_smith, email=jane@example.com
   Faculty 1: username=prof_smith, email=prof@example.com
   ```

2. **Test student flow:**
   - Submit at least one of each: project, internship, seminar
   - View submissions

3. **Test faculty flow:**
   - Assign students
   - View submissions
   - Grade submissions
   - Verify marks visible to students

### Database Inspection:

```bash
# Open database in SQLite CLI
sqlite3 campus_hub.db

# Useful queries:
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM internships;
SELECT * FROM seminars;
SELECT * FROM faculty_assignments;
```

## License

This project is created for educational purposes.

## Contact

For issues or questions, contact your development team.

---

**Version:** 1.0.0  
**Last Updated:** July 2026  
**Status:** Ready for terminal testing
