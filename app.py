import os
import json
import uuid
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_file, flash

app = Flask(__name__)
app.secret_key = 'VCET_MentorLog_SecureKey_2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7  # 7 days
app.config['SESSION_COOKIE_SECURE'] = False  # Allow HTTP for development
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

# Data file paths
DATA_DIR = 'data'
MENTORS_FILE = os.path.join(DATA_DIR, 'mentors.json')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
ACHIEVEMENTS_FILE = os.path.join(DATA_DIR, 'achievements.json')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

# Ensure session stays alive
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = 604800  # 7 days

# Utility functions
def load_json(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(filepath, data):
    """Save JSON data to file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Create uploads folder if it doesn't exist"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def login_required(role=None):
    """Decorator to check if user is logged in and has correct role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first', 'warning')
                return redirect(url_for('login'))
            
            if role and session.get('role') != role:
                current_role = session.get('role', 'unknown')
                required_role = role
                flash(f'Access Denied: You are logged in as {current_role}, but this page requires {required_role} role.', 'danger')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_student_by_id(student_id):
    """Get student details by ID"""
    students = load_json(STUDENTS_FILE)
    for student in students:
        if student['student_id'] == student_id:
            return student
    return None

def get_mentor_by_id(mentor_id):
    """Get mentor details by ID"""
    mentors = load_json(MENTORS_FILE)
    for mentor in mentors:
        if mentor['mentor_id'] == mentor_id:
            return mentor
    return None

def get_student_by_email(email):
    """Get student by email"""
    students = load_json(STUDENTS_FILE)
    for student in students:
        if student['email'] == email:
            return student
    return None

def get_student_by_id_or_email(student_id, email=None):
    """Get student by ID, fallback to email lookup if ID not found"""
    student = get_student_by_id(student_id)
    if student is None and email:
        student = get_student_by_email(email)
    return student

def get_mentor_by_email(email):
    """Get mentor by email"""
    mentors = load_json(MENTORS_FILE)
    for mentor in mentors:
        if mentor['email'] == email:
            return mentor
    return None

def get_student_achievements(student_id):
    """Get all achievements for a student"""
    achievements = load_json(ACHIEVEMENTS_FILE)
    return [a for a in achievements if a['student_id'] == student_id]

def is_student_assigned_to_mentor(student_id, mentor_id):
    """Check if student is assigned to mentor"""
    student = get_student_by_id(student_id)
    if student is None:
        return False
    return student['mentor_id'] == mentor_id

# Routes

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        if session.get('role') == 'student':
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for('mentor_dashboard'))
    return redirect(url_for('login'))


@app.route('/session-status')
def session_status():
    """Debug endpoint to check current session state"""
    return jsonify({
        'logged_in': 'user_id' in session,
        'user_id': session.get('user_id', 'N/A'),
        'name': session.get('name', 'N/A'),
        'role': session.get('role', 'N/A'),
        'email': session.get('email', 'N/A')
    })

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        mentor_id = request.form.get('mentor_id', '')
        mobile = request.form.get('mobile', '').strip()
        profile_pic = request.files.get('profile_pic')

        # Validation
        if not all([name, email, password, confirm_password, mentor_id, mobile]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return redirect(url_for('register'))

        # Check if email already registered
        if get_student_by_email(email):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Check if mentor exists
        if not get_mentor_by_id(mentor_id):
            flash('Invalid mentor selected', 'danger')
            return redirect(url_for('register'))

        # Create new student
        students = load_json(STUDENTS_FILE)
        # Handle profile picture upload
        profile_pic_filename = ''
        if profile_pic and profile_pic.filename:
            if allowed_file(profile_pic.filename):
                filename = f"{uuid.uuid4()}_{secure_filename(profile_pic.filename)}"
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic_filename = filename
            else:
                flash('Profile picture must be JPG, JPEG, PNG, or GIF', 'danger')
                return redirect(url_for('register'))

        new_student = {
            'student_id': f"S{str(len(students) + 1).zfill(3)}",
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'department': 'CSE-DS',
            'mentor_id': mentor_id,
            'mobile': mobile,
            'profile_pic': profile_pic_filename,
            'university': 'University of Mumbai',
            'college_name': "Vidyavardhini's College of Engineering & Technology",
            'branch': 'Computer Science & Engineering',
            'semester': '5',
            'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
            'academic_details': []
        }
        students.append(new_student)
        save_json(STUDENTS_FILE, students)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    # Load mentors for dropdown
    mentors = load_json(MENTORS_FILE)
    return render_template('register.html', mentors=mentors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for both students and mentors"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user_type = request.form.get('user_type', 'student')

        if not email:
            flash('Email is required', 'danger')
            return redirect(url_for('login'))

        # Password only required for students, not mentors
        if user_type == 'student' and not password:
            flash('Password is required', 'danger')
            return redirect(url_for('login'))

        if user_type == 'student':
            student = get_student_by_email(email)
            if student and check_password_hash(student['password'], password):
                session.clear()  # Clear any previous session
                session['user_id'] = student['student_id']
                session['email'] = student['email']
                session['name'] = student['name']
                session['role'] = 'student'
                session.permanent = True
                flash(f'Welcome back, {student["name"]}!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        else:
            mentor = get_mentor_by_email(email)
            if mentor:
                # For mentors, password is not stored (this is a mock authentication)
                # In production, mentors should have passwords too
                session.clear()  # Clear any previous session
                session['user_id'] = mentor['mentor_id']
                session['email'] = mentor['email']
                session['name'] = mentor['name']
                session['role'] = 'mentor'
                session.permanent = True
                flash(f'Welcome, {mentor["name"]}!', 'success')
                return redirect(url_for('mentor_dashboard'))
            else:
                flash('Mentor email not found', 'danger')

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

# Student Routes

@app.route('/student/dashboard')
@login_required(role='student')
def student_dashboard():
    """Student dashboard"""
    student_id = session['user_id']
    email = session.get('email')
    student = get_student_by_id_or_email(student_id, email)
    
    # If student is found by email but had old ID, update session
    if student and student['student_id'] != student_id:
        session['user_id'] = student['student_id']
        student_id = student['student_id']
    
    if student is None:
        flash('Student not found. Please log in again.', 'danger')
        return redirect(url_for('logout'))
    
    achievements = get_student_achievements(student_id)
    mentor = get_mentor_by_id(student['mentor_id'])

    return render_template('student_dashboard.html', 
                         student=student, 
                         achievements=achievements, 
                         mentor=mentor)

@app.route('/student/upload-achievement', methods=['POST'])
@login_required(role='student')
def upload_achievement():
    """Upload new achievement"""
    student_id = session['user_id']
    
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '')
    level = request.form.get('level', '')
    date = request.form.get('date', '')
    description = request.form.get('description', '').strip()
    certificate = request.files.get('certificate')

    # Validation
    if not all([title, category, level, date, description]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    certificate_file = ''
    if certificate:
        if not allowed_file(certificate.filename):
            return jsonify({'success': False, 'message': 'Invalid file type. Only PDF, JPG, PNG allowed'}), 400

        create_upload_folder()
        filename = f"{uuid.uuid4()}_{secure_filename(certificate.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        certificate.save(filepath)
        certificate_file = filename

    # Add achievement
    achievements = load_json(ACHIEVEMENTS_FILE)
    new_achievement = {
        'achievement_id': f"A{str(len(achievements) + 1).zfill(4)}",
        'student_id': student_id,
        'title': title,
        'category': category,
        'level': level,
        'date': date,
        'description': description,
        'certificate_file': certificate_file
    }
    achievements.append(new_achievement)
    save_json(ACHIEVEMENTS_FILE, achievements)

    return jsonify({'success': True, 'message': 'Achievement uploaded successfully'})

@app.route('/student/achievement/<achievement_id>/delete', methods=['POST'])
@login_required(role='student')
def delete_achievement(achievement_id):
    """Delete achievement"""
    student_id = session['user_id']
    achievements = load_json(ACHIEVEMENTS_FILE)

    for achievement in achievements:
        if achievement['achievement_id'] == achievement_id and achievement['student_id'] == student_id:
            # Delete certificate file if exists
            if achievement.get('certificate_file'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], achievement['certificate_file'])
                if os.path.exists(filepath):
                    os.remove(filepath)

            achievements.remove(achievement)
            save_json(ACHIEVEMENTS_FILE, achievements)
            return jsonify({'success': True, 'message': 'Achievement deleted'})

    return jsonify({'success': False, 'message': 'Achievement not found'}), 404

@app.route('/download/<filename>')
@login_required()
def download_file(filename):
    """Download certificate"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if not os.path.exists(filepath):
        flash('File not found', 'danger')
        return redirect(url_for('index'))
    
    return send_file(filepath, as_attachment=True)

# Mentor Routes

@app.route('/mentor/dashboard')
@login_required(role='mentor')
def mentor_dashboard():
    """Mentor dashboard - view assigned students"""
    mentor_id = session['user_id']
    mentor = get_mentor_by_id(mentor_id)
    
    # Get all students assigned to this mentor
    students = load_json(STUDENTS_FILE)
    assigned_students = [s for s in students if s['mentor_id'] == mentor_id]

    return render_template('mentor_dashboard.html', 
                         mentor=mentor, 
                         students=assigned_students)

@app.route('/mentor/student/<student_id>')
@login_required(role='mentor')
def mentor_view_student(student_id):
    """View specific student's profile and achievements"""
    mentor_id = session['user_id']
    
    # Verify that this student is assigned to this mentor
    if not is_student_assigned_to_mentor(student_id, mentor_id):
        flash(f'Student {student_id} is not assigned to you. You can only view your assigned students.', 'danger')
        return redirect(url_for('mentor_dashboard'))

    student = get_student_by_id(student_id)
    achievements = get_student_achievements(student_id)
    mentor = get_mentor_by_id(student['mentor_id'])

    return render_template('mentor_student.html', 
                         student=student, 
                         achievements=achievements, 
                         mentor=mentor)

@app.route('/mentor/add-remark', methods=['POST'])
@login_required(role='mentor')
def add_mentor_remark():
    """Add mentor remark to achievement (optional guidance)"""
    mentor_id = session['user_id']
    achievement_id = request.form.get('achievement_id', '')
    remark = request.form.get('remark', '').strip()

    if not achievement_id or not remark:
        return jsonify({'success': False, 'message': 'Achievement ID and remark are required'}), 400

    achievements = load_json(ACHIEVEMENTS_FILE)
    for achievement in achievements:
        if achievement['achievement_id'] == achievement_id:
            # Verify mentor can access this achievement
            student = get_student_by_id(achievement['student_id'])
            if student['mentor_id'] != mentor_id:
                return jsonify({'success': False, 'message': 'Unauthorized'}), 403

            # Add mentor remark if not exists
            if 'mentor_remarks' not in achievement:
                achievement['mentor_remarks'] = []

            achievement['mentor_remarks'].append({
                'mentor_id': mentor_id,
                'mentor_name': session['name'],
                'remark': remark,
                'timestamp': datetime.now().isoformat()
            })

            save_json(ACHIEVEMENTS_FILE, achievements)
            return jsonify({'success': True, 'message': 'Remark added successfully'})

    return jsonify({'success': False, 'message': 'Achievement not found'}), 404

@app.route('/student/profile/update', methods=['POST'])
@login_required(role='student')
def update_profile():
    """Update student profile information"""
    student_id = session['user_id']
    mobile = request.form.get('mobile', '').strip()
    profile_pic = request.files.get('profile_pic')

    students = load_json(STUDENTS_FILE)
    for student in students:
        if student['student_id'] == student_id:
            # Update mobile if provided
            if mobile:
                student['mobile'] = mobile

            # Handle profile picture upload
            if profile_pic and profile_pic.filename:
                if allowed_file(profile_pic.filename):
                    # Delete old profile picture if exists
                    if student.get('profile_pic'):
                        old_file = os.path.join(app.config['UPLOAD_FOLDER'], student['profile_pic'])
                        if os.path.exists(old_file):
                            os.remove(old_file)
                    
                    # Save new profile picture
                    filename = f"{uuid.uuid4()}_{secure_filename(profile_pic.filename)}"
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    student['profile_pic'] = filename
                else:
                    return jsonify({'success': False, 'message': 'Profile picture must be JPG, JPEG, PNG, or GIF'}), 400

            save_json(STUDENTS_FILE, students)
            return jsonify({'success': True, 'message': 'Profile updated successfully'})

    return jsonify({'success': False, 'message': 'Student not found'}), 404

@app.route('/student/academic-details/update', methods=['POST'])
@login_required(role='student')
def update_academic_details():
    """Update student academic details"""
    student_id = session['user_id']
    data = request.get_json()
    academic_details = data.get('academic_details', [])

    students = load_json(STUDENTS_FILE)
    for student in students:
        if student['student_id'] == student_id:
            student['academic_details'] = academic_details
            save_json(STUDENTS_FILE, students)
            return jsonify({'success': True, 'message': 'Academic details updated successfully'})

    return jsonify({'success': False, 'message': 'Student not found'}), 404


# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    flash('An error occurred. Please try again', 'danger')
    return redirect(url_for('index'))

# Initialize on startup
create_upload_folder()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
