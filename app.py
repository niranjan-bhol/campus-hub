"""
Flask Web Application for Campus Hub Portal
REST API backend with session management
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import os
from database import init_db, Database
from auth import AuthManager
from student_operations import StudentOperations
from faculty_operations import FacultyOperations

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))  # Use env var in production

# Initialize database on startup
init_db()

# Session decorator for authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session or session['user']['role'] != role:
                return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Landing page with role selection"""
    if 'user' in session:
        if session['user']['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for('faculty_dashboard'))
    return render_template('index.html')

@app.route('/login/<role>')
def login_page(role):
    """Login page for student/faculty"""
    if role not in ['student', 'faculty']:
        return redirect(url_for('index'))
    return render_template('login.html', role=role)

@app.route('/register/<role>')
def register_page(role):
    """Registration page for student/faculty"""
    if role not in ['student', 'faculty']:
        return redirect(url_for('index'))
    return render_template('register.html', role=role)

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    """Student dashboard"""
    return render_template('student_dashboard.html', user=session['user'])

@app.route('/faculty/dashboard')
@login_required
@role_required('faculty')
def faculty_dashboard():
    """Faculty dashboard"""
    return render_template('faculty_dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user', None)
    return redirect(url_for('index'))


# ==================== API ENDPOINTS ====================

@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user"""
    data = request.get_json()
    
    required_fields = ['name', 'username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    if data['role'] not in ['student', 'faculty']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400
    
    auth = AuthManager()
    success, message = auth.register_user(
        data['name'], 
        data['username'], 
        data['email'], 
        data['password'], 
        data['role']
    )
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/login', methods=['POST'])
def api_login():
    """Login user"""
    data = request.get_json()
    
    if not all(field in data for field in ['identifier', 'password', 'role']):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    auth = AuthManager()
    success, result = auth.login_user(data['identifier'], data['password'], data['role'])
    
    if success:
        session['user'] = result
        return jsonify({'success': True, 'user': result})
    else:
        return jsonify({'success': False, 'message': result}), 401

@app.route('/api/student/submit-project', methods=['POST'])
@login_required
@role_required('student')
def api_submit_project():
    """Submit a project"""
    data = request.get_json()
    
    student_ops = StudentOperations(session['user']['user_id'])
    success, message = student_ops.submit_project(
        data.get('title', ''),
        data.get('description', ''),
        data.get('start_date', ''),
        data.get('end_date', ''),
        data.get('status', 'In Progress'),
        data.get('github_link', ''),
        data.get('live_link', '')
    )
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/student/apply-internship', methods=['POST'])
@login_required
@role_required('student')
def api_apply_internship():
    """Apply for internship"""
    data = request.get_json()
    
    student_ops = StudentOperations(session['user']['user_id'])
    success, message = student_ops.apply_internship(
        data.get('company_name', ''),
        data.get('position', ''),
        data.get('start_date', ''),
        data.get('end_date', ''),
        data.get('status', 'Applied')
    )
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/student/present-seminar', methods=['POST'])
@login_required
@role_required('student')
def api_present_seminar():
    """Register seminar"""
    data = request.get_json()
    
    student_ops = StudentOperations(session['user']['user_id'])
    success, message = student_ops.present_seminar(
        data.get('topic', ''),
        data.get('description', ''),
        data.get('seminar_date', ''),
        data.get('venue', '')
    )
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/student/submissions', methods=['GET'])
@login_required
@role_required('student')
def api_get_my_submissions():
    """Get student's submissions"""
    student_ops = StudentOperations(session['user']['user_id'])
    submissions = student_ops.view_my_submissions()
    
    if submissions:
        return jsonify({'success': True, 'submissions': submissions})
    else:
        return jsonify({'success': False, 'message': 'Error fetching submissions'}), 500

@app.route('/api/faculty/students', methods=['GET'])
@login_required
@role_required('faculty')
def api_get_all_students():
    """Get all students"""
    faculty_ops = FacultyOperations(session['user']['user_id'])
    students = faculty_ops.list_all_students()
    
    return jsonify({'success': True, 'students': students})

@app.route('/api/faculty/my-students', methods=['GET'])
@login_required
@role_required('faculty')
def api_get_my_students():
    """Get assigned students"""
    faculty_ops = FacultyOperations(session['user']['user_id'])
    students = faculty_ops.list_my_students()
    
    return jsonify({'success': True, 'students': students})

@app.route('/api/faculty/assign-student', methods=['POST'])
@login_required
@role_required('faculty')
def api_assign_student():
    """Assign student to faculty"""
    data = request.get_json()
    
    if 'student_id' not in data:
        return jsonify({'success': False, 'message': 'Student ID required'}), 400
    
    faculty_ops = FacultyOperations(session['user']['user_id'])
    success, message = faculty_ops.assign_student(data['student_id'])
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/faculty/student-submissions/<student_id>', methods=['GET'])
@login_required
@role_required('faculty')
def api_get_student_submissions(student_id):
    """Get specific student's submissions"""
    faculty_ops = FacultyOperations(session['user']['user_id'])
    result, error = faculty_ops.view_student_submissions(student_id)
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({'success': True, 'submissions': result})

@app.route('/api/faculty/grade', methods=['POST'])
@login_required
@role_required('faculty')
def api_grade_submission():
    """Grade a submission"""
    data = request.get_json()
    
    required_fields = ['submission_type', 'submission_id', 'marks']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    faculty_ops = FacultyOperations(session['user']['user_id'])
    success, message = faculty_ops.grade_submission(
        data['submission_type'],
        data['submission_id'],
        int(data['marks'])
    )
    
    return jsonify({'success': success, 'message': message})


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or use 5000
    port = int(os.environ.get('PORT', 5000))
    # Debug mode only in development
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
