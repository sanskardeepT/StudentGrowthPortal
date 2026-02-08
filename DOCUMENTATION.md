# VCET MentorLog - Complete System Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [User Guide](#user-guide)
5. [Administrator Guide](#administrator-guide)
6. [Technical Details](#technical-details)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## System Overview

### Purpose
VCET MentorLog is a digital mentoring and achievement tracking portal for the Computer Science & Engineering (Data Science) program at Vidyavardhini's College of Engineering & Technology.

### Key Objectives
- ✅ Create permanent digital records of student achievements
- ✅ Enable mentors to provide guidance and feedback
- ✅ Support transparent mentor-student communication  
- ✅ Eliminate barriers between students and their assigned mentors
- ✅ Maintain student privacy (mentors see only assigned students)

### Not a Feature
❌ Approval or rejection system
❌ Grading or evaluation platform
❌ Student reputation system
❌ Achievement marketplace

---

## Architecture

### Technology Stack
- **Framework**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: JSON files (no database)
- **Authentication**: Session-based
- **Deployment**: Python WSGI-compatible server

### Data Flow Diagram
```
┌─────────────────┐        ┌──────────────┐
│   Web Browser   │◄──────►│  Flask App   │
│   (Client)      │        │  (Server)    │
└─────────────────┘        └──────┬───────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │   JSON Files     │
                        ├──────────────────┤
                        │ mentors.json     │
                        │ students.json    │
                        │ achievements.json│
                        │ uploads/         │
                        └──────────────────┘
```

### System Components

#### Frontend Components
- **Login Page**: Role selection (Student/Mentor), authentication
- **Registration Page**: New student signup with mentor selection
- **Student Dashboard**: Record upload, achievement management
- **Mentor Dashboard**: Mentee list, profile viewing
- **Student Profile (Mentor View)**: Achievement review, remark addition

#### Backend Components
- **Authentication Module**: Session management, password hashing
- **File Handler**: Upload validation, certificate storage
- **JSON Manager**: CRUD operations on data files
- **Access Control**: Role-based routing, ownership verification

#### Data Components
- **Mentors Database**: Faculty information
- **Students Database**: User accounts with mentor assignments
- **Achievements Database**: Student records with mentor remarks
- **File Storage**: Uploaded certificates in uploads/ folder

---

## Installation

### System Requirements
- Python 3.8 or higher
- 250MB free disk space
- Windows, macOS, or Linux
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step-by-Step Installation

#### Step 1: Prepare Environment
```bash
# Navigate to project directory
cd c:\Users\Sanskardeep\OneDrive\Desktop\mentor\StudentGrowthPortal

# Create Python virtual environment
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- Flask 2.3.3
- Werkzeug 2.3.7

#### Step 3: Verify Data Files
```bash
# Check all files exist
data/
  ├── mentors.json
  ├── students.json
  └── achievements.json
uploads/  (empty folder)
```

#### Step 4: Run Application
```bash
# Start Flask development server
python app.py

# Output should show:
# * Running on http://localhost:5000
# * Debug mode: on
```

#### Step 5: Access Application
Open browser: **http://localhost:5000**

---

## User Guide

### For Students

#### Registration Process
1. Click "Register here" on login page
2. Fill registration form:
   - **Full Name**: Required, 3+ characters
   - **Email**: Must be @vcet.ac.in domain
   - **Mentor**: Select from dropdown (cannot change later)
   - **Password**: Minimum 6 characters, alphanumeric
   - **Confirm Password**: Must match password field

3. Submit registration
4. Success message confirms account creation
5. Redirect to login page

**Important**: Mentor assignment is permanent and cannot be changed. Choose carefully!

#### Login
1. Select "Student" radio button
2. Enter registered email
3. Enter password
4. Click "Login"
5. Redirected to student dashboard

#### Student Dashboard
**Left Sidebar**:
- Student name and email
- Student ID and department
- Assigned mentor information with contact

**Main Content**:
- Achievement upload form
- List of uploaded achievements
- Mentor remarks (if any)
- Download and delete options

#### Uploading Achievement
1. Scroll to "Upload New Achievement" section
2. Fill required fields:
   - **Title**: Descriptive name of achievement (required)
   - **Category**: Select from dropdown (required)
     - Hackathon
     - Workshop
     - Sports
     - Cultural
     - Internship
     - Certification
     - Competition
     - Other
   - **Level**: Select achievement scope (required)
     - College (local event)
     - State (state-level competition)
     - National (national competition)
     - International (international event)
   - **Date**: YYYY-MM-DD format (required)
   - **Description**: Detailed description (required, 10+ words)
   - **Certificate**: Optional file upload

3. Select certificate (if any):
   - Formats: PDF, JPG, PNG only
   - Maximum size: 10MB
   - Clear photos of physical certificates work well

4. Click "Upload Achievement"
5. Success message appears
6. Achievement immediately visible in list

#### Viewing Achievements
- Achievements display in reverse chronological order (newest first)
- Each achievement shows:
  - Title and badges (category, level)
  - Upload date
  - Description
  - Certificate download button (if attached)
  - Mentor remarks section (if mentor added comments)
  - Delete button

#### Mentor Remarks
- Remarks are optional feedback from your assigned mentor
- No grades or scores assigned
- Remarks are guidance and support
- You can see each remark with mentor name and timestamp
- Multiple remarks can be added to one achievement

#### Downloading Certificates
1. Click "📥 Download Certificate" button on achievement
2. File automatically downloads to your Downloads folder
3. Original file name preserved for future reference

#### Deleting Achievement
1. Click "🗑️ Delete" button on achievement card
2. Confirm deletion in popup
3. File removed from system permanently
4. Certificate file also deleted from server

#### Logging Out
1. Click "Logout" button in top-right
2. Session ends
3. Redirected to login page
4. Must log in again to access dashboard

---

### For Mentors

#### Login Process
1. Go to http://localhost:5000/login
2. Select "Mentor (Faculty)" radio button
3. Enter your email (from mentors.json)
4. **Password field auto-hides** (not required for demo)
5. Click "Login"
6. Redirected to mentor dashboard

**Note**: In production, mentor passwords should be implemented.

#### Mentor Dashboard
**Left Sidebar**:
- Your name and email
- Department (CSE-DS)
- Count of assigned students

**Main Content**:
- Grid of student cards
- Each card shows:
  - Student name and email
  - Student ID and department
  - "View Profile & Achievements" button

#### Viewing Student Profile
1. Click student card on dashboard
2. See student information:
   - Name, email, ID, department
   - Back button to return to dashboard

3. See all student achievements:
   - Displayed in chronological order
   - View details and certificates
   - See existing mentor remarks

#### Adding Remarks
1. Navigate to student achievement
2. Scroll to "Mentor Remarks & Guidance" section
3. Find "Add remarks here" text box
4. Type your guidance comment:
   - Constructive feedback
   - Encouragement
   - Suggestions for growth
   - Questions or discussion starters

5. Click "Add Remarks" button
6. Comment appears in remarks section
7. Timestamp automatically recorded

#### Viewing Remarks History
- All remarks appear with:
  - Mentor name
  - Remark text
  - Timestamp (ISO format)
  - Multiple remarks visible in chronological order

#### Access Control
- You see ONLY students who selected you as mentor
- Cannot view other mentors' students
- Cannot access student accounts directly
- View is read-only (cannot edit student info)

#### Logging Out
1. Click "Logout" button
2. Session ends
3. Return to login page

---

## Administrator Guide

### Managing Mentors

#### Add New Mentor
Edit `data/mentors.json`:
```json
{
  "mentor_id": "M006",
  "name": "Dr. New Faculty Name",
  "email": "newfaculty@vcet.edu.in",
  "department": "CSE-DS"
}
```

**Rules**:
- mentor_id must be unique (M###)
- Email must be @vcet.edu.in
- Department must be "CSE-DS"
- Keep JSON format valid

#### Remove Mentor
1. Delete mentor entry from mentors.json
2. Students already assigned to this mentor remain unchanged
3. Mentor cannot login anymore

### Managing Students

#### Create Student (Registration Method - Recommended)
1. Use student registration page
2. New student fills form
3. Automatically added to students.json
4. Faster, less error-prone

#### Manually Add Student
Edit `data/students.json`:
```json
{
  "student_id": "S004",
  "name": "Jane Doe",
  "email": "jane.doe@vcet.ac.in",
  "password": "hashed_password_here",
  "department": "CSE-DS",
  "mentor_id": "M002"
}
```

**Rules**:
- student_id must be unique (S###)
- Email must be @vcet.ac.in
- Password must be hashed (use Python):
  ```python
  from werkzeug.security import generate_password_hash
  hashed = generate_password_hash("StudentPassword123")
  print(hashed)
  ```
- Department always "CSE-DS"
- mentor_id must exist in mentors.json

#### Reset Student Password
1. Extract password hash for new password:
   ```python
   from werkzeug.security import generate_password_hash
   new_hash = generate_password_hash("NewPassword123")
   ```
2. Update `students.json` with new hash
3. Student can login with new password

#### Delete Student
1. Remove entry from students.json
2. Student achievements remain in achievements.json
3. Student cannot login anymore
4. Mentor can still view past records

### Managing Achievements

#### View All Achievements
Open `data/achievements.json` in text editor to see:
- All student records
- Categories, levels, dates
- Attached file names
- Mentor remarks history

#### Clear Old Files
1. Check `uploads/` folder
2. Delete unused certificate files manually
3. But keep filename in achievements.json for records

#### Backup Data
```bash
# Copy entire data folder
Copy-Item -Path "data" -Destination "data_backup_2025-01-15" -Recurse

# Copy uploads folder
Copy-Item -Path "uploads" -Destination "uploads_backup_2025-01-15" -Recurse
```

#### Restore from Backup
```bash
# Remove current data
Remove-Item -Path "data" -Recurse
Remove-Item -Path "uploads" -Recurse

# Restore backup
Copy-Item -Path "data_backup_2025-01-15" -Destination "data" -Recurse
Copy-Item -Path "uploads_backup_2025-01-15" -Destination "uploads" -Recurse
```

---

## Technical Details

### File Structure

#### app.py - Main Application
- **Lines 1-50**: Imports and configuration
- **Lines 51-100**: Utility functions (JSON I/O, validation)
- **Lines 101-150**: Authentication functions
- **Lines 151-200**: Student routes (registration, login)
- **Lines 201-300**: Student dashboard routes
- **Lines 301-400**: Mentor routes
- **Lines 401-500**: File handling and error management

#### HTML Templates
- **register.html**: Form with mentor dropdown, client-side validation
- **login.html**: Radio button toggle for role selection
- **student_dashboard.html**: Main student portal, AJAX file upload
- **mentor_dashboard.html**: Student list grid, quick links
- **mentor_student.html**: Achievement detail view, remark form

#### CSS
- Mobile-responsive grid layout
- Professional color scheme (blue/gray)
- Accessible form styling
- Print-friendly design

#### JSON Data Files
- Human-readable format
- Easy to edit manually
- Portable backup-friendly
- No special encoding required

### Session Management
```python
session['user_id']     # S001 or M001
session['role']        # 'student' or 'mentor'
session['name']        # Display name
session['email']       # Email address
```

Session expires after browser close (default Flask behavior).

### Password Hashing
Students' passwords are hashed using `werkzeug.security`:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing on registration
hash = generate_password_hash("StudentPassword123")

# Verification on login
if check_password_hash(stored_hash, entered_password):
    # Login successful
```

Mentors don't have password hashing (demo mode - should be added in production).

### File Upload Validation
1. **File Type**: Only PDF, JPG, PNG allowed
2. **File Size**: Maximum 10MB per file
3. **Filename**: Sanitized using `secure_filename()`
4. **Storage Path**: `uploads/` folder
5. **Unique Names**: UUID prefix prevents collisions

---

## API Reference

### Authentication Routes

#### POST /register
Student registration
```
Parameters:
  - name: string (required)
  - email: string (required, @vcet.ac.in)
  - password: string (required, min 6 chars)
  - confirm_password: string (required)
  - mentor_id: string (required)

Response:
  - Success: Redirect to /login with message
  - Error: Redirect to /register with error message
```

#### POST /login
Student or mentor login
```
Parameters:
  - email: string (required)
  - password: string (required for students)
  - user_type: string ('student' or 'mentor')

Response:
  - Success (student): Redirect to /student/dashboard
  - Success (mentor): Redirect to /mentor/dashboard
  - Error: Redirect to /login with error message
```

#### GET /logout
Clear session and logout
```
Response:
  - Redirect to /login with logout message
```

### Student Routes

#### GET /student/dashboard
View student dashboard
```
Requirements:
  - User must be logged in as student
  
Response:
  - HTML: Student dashboard with achievements
```

#### POST /student/upload-achievement
Upload new achievement
```
Parameters:
  - title: string (required)
  - category: string (required)
  - level: string (required)
  - date: YYYY-MM-DD (required)
  - description: string (required)
  - certificate: file (optional, PDF/JPG/PNG)

Response:
  - JSON: {success: true, message: "..."}
  - Error: {success: false, message: "..."}
```

#### POST /student/achievement/<id>/delete
Delete achievement record
```
Parameters:
  - achievement_id: string (in URL)

Response:
  - JSON: {success: true, message: "..."}
  - Error: {success: false, message: "..."} 404
```

#### GET /download/<filename>
Download certificate file
```
Parameters:
  - filename: string (in URL)

Response:
  - File: Binary file download
  - Error: Redirect with error message
```

### Mentor Routes

#### GET /mentor/dashboard
View assigned students list
```
Requirements:
  - User must be logged in as mentor

Response:
  - HTML: Mentor dashboard with student cards
```

#### GET /mentor/student/<student_id>
View student profile and achievements
```
Requirements:
  - User must be logged in as mentor
  - Student must be assigned to this mentor

Response:
  - HTML: Student profile page with achievements
  - Error 403: If student not assigned
  - Error 404: If student not found
```

#### POST /mentor/add-remark
Add guidance remark to achievement
```
Parameters:
  - achievement_id: string (required)
  - remark: string (required)

Response:
  - JSON: {success: true, message: "..."}
  - Error: {success: false, message: "..."} 403
```

---

## Troubleshooting

### Common Issues & Solutions

#### Application Won't Start

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt

# Or install manually
pip install Flask==2.3.3 Werkzeug==2.3.7
```

**Issue**: `Address already in use`
```bash
# Solution: Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)

# Or kill process on port 5000 (Windows PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

**Issue**: `IndentationError in app.py`
```bash
# Solution: Re-check file with
python -m py_compile app.py

# If error, recreate app.py from original
```

#### Login Issues

**Issue**: "Invalid email or password"
- Check email matches exactly in students.json
- Verify password is correct (case-sensitive)
- For mentors: just use email, no password needed
- Password hashing: ensure hash correctly generated

**Issue**: "Mentor email not found"
- Check mentor email exists in mentors.json
- Use @vcet.edu.in domain for mentors
- Email is case-sensitive

#### File Upload Issues

**Issue**: "Invalid file type"
- Upload only PDF, JPG, or PNG
- Check file extension: .pdf .jpg .jpeg .png
- Uppercase extensions also work

**Issue**: "File too large"
- Maximum 10MB per file
- Compress image if needed
- Split large PDF into parts

**Issue**: "Upload fails silently"
- Check `uploads/` folder exists and has write permissions
- Check disk space available (need ~100MB free minimum)
- Try different file type

#### Database Issues

**Issue**: Missing data file
- Verify `data/mentors.json` exists
- Verify `data/students.json` exists
- Verify `data/achievements.json` exists
- Check file format is valid JSON

**Issue**: JSON format error
- Open file in text editor
- Use JSON validator online
- Check for missing commas, brackets
- Ensure all strings are in double quotes

**Issue**: Mentor not visible after adding
- Save mentors.json properly
- Restart Flask application
- Clear browser cache

#### Performance Issues

**Issue**: Application slow to load
- Check JSON files not too large (normal if <1000 students)
- Reduce number of files in uploads/
- Consider database migration

**Issue**: File upload slow
- Check file size is reasonable
- Check internet connection
- Try uploading in different browser

#### Data Loss Prevention

**Backup before changes**:
```bash
# Before editing JSON files
cp -r data data_backup_$(date +%Y%m%d)
cp -r uploads uploads_backup_$(date +%Y%m%d)
```

**Restore from backup**:
```bash
# If something goes wrong
rm -r data
cp -r data_backup_YYYYMMDD data
```

---

## Best Practices

### For Students
1. ✅ Upload achievements immediately after completion
2. ✅ Include description with relevant details
3. ✅ Attach proof/certificate whenever possible
4. ✅ Review mentor remarks regularly
5. ✅ Use accurate dates for records

### For Mentors
1. ✅ Check assigned students regularly
2. ✅ Review new achievements within 5 days
3. ✅ Provide constructive feedback
4. ✅ Ask questions to promote deeper learning
5. ✅ Maintain encouraging tone

### For Administrators
1. ✅ Backup data weekly
2. ✅ Monitor file upload folder size
3. ✅ Keep mentor list updated
4. ✅ Archive old records annually
5. ✅ Review system logs regularly

---

## Support & Contact

For technical issues:
1. Check this documentation
2. Review README.md
3. Check QUICKSTART.md
4. View app.py comments for code logic

---

**Document Version**: 1.0
**Last Updated**: February 2025
**Status**: Production Ready ✅
