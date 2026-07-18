# Campus Hub Portal - Quick Reference Guide

## 🚀 Starting the Application

### Option 1: Using the start script (recommended)
```bash
./start.sh
```

### Option 2: Direct Python execution
```bash
python3 main.py
```

### Option 3: Initialize database separately
```bash
python3 database.py
python3 main.py
```

---

## 📋 Quick Command Reference

### Database Operations

**View all tables:**
```bash
sqlite3 campus_hub.db ".tables"
```

**View table schema:**
```bash
sqlite3 campus_hub.db ".schema users"
sqlite3 campus_hub.db ".schema projects"
```

**Query users:**
```bash
sqlite3 campus_hub.db "SELECT user_id, name, role FROM users;"
```

**Query projects with marks:**
```bash
sqlite3 campus_hub.db "SELECT project_id, title, marks, graded_by FROM projects;"
```

**View all students:**
```bash
sqlite3 campus_hub.db "SELECT user_id, name, email FROM users WHERE role='student';"
```

**View all faculty:**
```bash
sqlite3 campus_hub.db "SELECT user_id, name, email FROM users WHERE role='faculty';"
```

**Check faculty-student assignments:**
```bash
sqlite3 campus_hub.db "SELECT * FROM faculty_assignments;"
```

**View graded submissions:**
```bash
sqlite3 campus_hub.db "SELECT 'Project' as type, project_id as id, marks FROM projects WHERE marks IS NOT NULL
UNION ALL
SELECT 'Internship', internship_id, marks FROM internships WHERE marks IS NOT NULL
UNION ALL
SELECT 'Seminar', seminar_id, marks FROM seminars WHERE marks IS NOT NULL;"
```

---

## 🔑 Common User Flows

### First Time User (Student)
1. Run application: `python3 main.py`
2. Select: `1` (Student)
3. Choose: `1` (Register)
4. Fill in: name, username, email, password
5. Note your assigned ID (e.g., student_1)
6. Login with your credentials

### First Time User (Faculty)
1. Run application: `python3 main.py`
2. Select: `2` (Faculty)
3. Choose: `1` (Register)
4. Fill in: name, username, email, password
5. Note your assigned ID (e.g., faculty_1)
6. Login with your credentials

### Student - Submit a Project
1. Login as student
2. Choose: `1` (Submit Project)
3. Enter project details
4. Note the project ID (e.g., student_1_project_1)

### Faculty - Grade a Submission
1. Login as faculty
2. Assign student: Choose `1` → Enter student_id
3. View submissions: Choose `3` → Enter student_id
4. Grade submission: Choose `4`
   - Type: `project`, `internship`, or `seminar`
   - ID: e.g., `student_1_project_1`
   - Marks: 0-100

---

## 🗃️ Database Backup & Restore

### Backup database
```bash
cp campus_hub.db campus_hub_backup_$(date +%Y%m%d).db
```

### Restore from backup
```bash
cp campus_hub_backup_20260718.db campus_hub.db
```

### Export to SQL
```bash
sqlite3 campus_hub.db .dump > campus_hub_dump.sql
```

### Import from SQL
```bash
sqlite3 campus_hub.db < campus_hub_dump.sql
```

---

## 🧪 Testing Scenarios

### Complete Test Flow

**1. Create test users:**
```
Student 1:
  Name: John Doe
  Username: john_doe
  Email: john@test.com
  Password: test123

Student 2:
  Name: Jane Smith
  Username: jane_smith
  Email: jane@test.com
  Password: test123

Faculty 1:
  Name: Prof. Johnson
  Username: prof_johnson
  Email: prof@test.com
  Password: test123
```

**2. Student 1 submissions:**
- Project: "AI Chatbot"
- Internship: Google, Software Engineer
- Seminar: "Machine Learning Basics"

**3. Faculty workflow:**
- Assign student_1 and student_2
- View student_1 submissions
- Grade all submissions with different marks

**4. Verification:**
- Login as student_1
- View submissions to see marks

---

## 🛠️ Troubleshooting Commands

### Check if database is locked
```bash
lsof campus_hub.db
```

### Reset database (CAUTION: Deletes all data)
```bash
rm campus_hub.db
python3 database.py
```

### Check Python version
```bash
python3 --version
```

### Verify all files exist
```bash
ls -la *.py
```

---

## 📊 Useful SQL Queries

### Get submission statistics per student
```sql
sqlite3 campus_hub.db "
SELECT 
    u.user_id,
    u.name,
    COUNT(DISTINCT p.project_id) as projects,
    COUNT(DISTINCT i.internship_id) as internships,
    COUNT(DISTINCT s.seminar_id) as seminars
FROM users u
LEFT JOIN projects p ON u.user_id = p.student_id
LEFT JOIN internships i ON u.user_id = i.student_id
LEFT JOIN seminars s ON u.user_id = s.student_id
WHERE u.role = 'student'
GROUP BY u.user_id;
"
```

### Get average marks by student
```sql
sqlite3 campus_hub.db "
SELECT 
    u.user_id,
    u.name,
    ROUND(AVG(COALESCE(p.marks, i.marks, s.marks)), 2) as avg_marks
FROM users u
LEFT JOIN projects p ON u.user_id = p.student_id
LEFT JOIN internships i ON u.user_id = i.student_id
LEFT JOIN seminars s ON u.user_id = s.student_id
WHERE u.role = 'student' AND (p.marks IS NOT NULL OR i.marks IS NOT NULL OR s.marks IS NOT NULL)
GROUP BY u.user_id;
"
```

### Faculty workload
```sql
sqlite3 campus_hub.db "
SELECT 
    f.user_id,
    f.name,
    COUNT(DISTINCT fa.student_id) as students_assigned,
    (SELECT COUNT(*) FROM projects WHERE graded_by = f.user_id) +
    (SELECT COUNT(*) FROM internships WHERE graded_by = f.user_id) +
    (SELECT COUNT(*) FROM seminars WHERE graded_by = f.user_id) as total_graded
FROM users f
LEFT JOIN faculty_assignments fa ON f.user_id = fa.faculty_id
WHERE f.role = 'faculty'
GROUP BY f.user_id;
"
```

---

## 🎯 Pro Tips

1. **Always note your User ID** after registration - you'll need it for reference
2. **Faculty must assign students** before they can view submissions or grade
3. **Use descriptive titles** for projects to make them easy to identify
4. **Backup database regularly** if you're testing heavily
5. **Check marks** - Students can see marks immediately after faculty grades

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Review database schema: `sqlite3 campus_hub.db ".schema"`
- Test with sample data first before real usage
- Keep backups before making bulk changes

---

**Last Updated:** July 2026  
**For:** Campus Hub Portal v1.0.0
