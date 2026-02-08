# VCET MentorLog - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.8+ installed
- Windows/Mac/Linux OS
- ~100MB free disk space

### Installation Steps

#### 1️⃣ Open Command Prompt / Terminal
```bash
# Navigate to the project folder
cd C:\Users\Sanskardeep\OneDrive\Desktop\mentor\StudentGrowthPortal
```

#### 2️⃣ Create Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Flask
```bash
pip install -r requirements.txt
```

#### 4️⃣ Run Application
```bash
python app.py
```

Expected output:
```
 * Running on http://localhost:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

#### 5️⃣ Open in Browser
```
http://localhost:5000
```

---

## 🧪 Quick Test Flow (2 minutes)

### Test 1: Student Registration & Login
1. **Visit**: http://localhost:5000/register
2. **Fill**:
   - Name: Test Student
   - Email: teststudent@vcet.ac.in
   - Password: TestPass123
   - Confirm: TestPass123
   - Mentor: Dr. Rajesh Kumar
3. **Click**: Register
4. **Login Page** → Email: teststudent@vcet.ac.in | Password: TestPass123
5. ✅ See student dashboard

### Test 2: Upload Achievement
1. On **Student Dashboard**, fill:
   - Title: My First Achievement
   - Category: Workshop
   - Level: College
   - Date: 2025-12-15
   - Description: Completed data science workshop
2. **Skip** certificate file (optional)
3. **Click**: Upload Achievement
4. ✅ Achievement appears in list

### Test 3: Mentor Login & View
1. **New Tab**: http://localhost:5000/login
2. **Select**: Mentor (Faculty)
3. **Email**: rajesh.kumar@vcet.edu.in
4. **No Password** (faculty login is automatic)
5. **Click**: Login
6. ✅ See list of assigned students
7. **Click**: View Profile → Student's achievements displayed
8. **Add Remark**: "Great progress on data science fundamentals!"
9. ✅ Remark appears in student's achievement

### Test 4: Student Sees Mentor Remarks
1. **Go back to** student account
2. **View achievement** → Mentor remarks visible below
3. ✅ Feedback loop complete

---

## 📊 Sample Credentials (Pre-created)

### Students
```
Email:    amit.tiwari@vcet.ac.in
Password: Welcome@123
Mentor:   Dr. Rajesh Kumar

Email:    neha.gupta@vcet.ac.in
Password: Welcome@123
Mentor:   Dr. Priya Sharma
```

### Mentors
```
Email: rajesh.kumar@vcet.edu.in
Email: priya.sharma@vcet.edu.in
Email: arjun.patel@vcet.edu.in
Email: sneha.verma@vcet.edu.in
Email: vikram.singh@vcet.edu.in

(No password required for mentor login)
```

---

## 🎯 What to Test

| Feature | Step | Expected Result |
|---------|------|-----------------|
| **Register** | Fill form + Select Mentor | Student account created |
| **Login** | Email + Password | Redirected to dashboard |
| **Upload** | Fill achievement form | Record appears in list |
| **Download** | Click cert button | File downloads |
| **Mentor View** | Faculty login + click student | Achievements visible |
| **Add Remark** | Fill remark field | Comment appears |
| **Student View** | Login as student | Remarks visible |
| **Delete** | Click delete button | Achievement removed |
| **Logout** | Click logout | Redirected to login |

---

## 📁 File Locations

```
StudentGrowthPortal/
├── app.py                    ← Main application
├── requirements.txt          ← Python packages
├── data/
│   ├── mentors.json         ← Faculty list
│   ├── students.json        ← Student accounts
│   └── achievements.json    ← Records
├── uploads/                 ← Student files
├── templates/               ← HTML pages
└── static/
    └── style.css           ← Styling
```

---

## 🔧 Troubleshooting

### ❌ "Port 5000 already in use"
Edit line in `app.py`:
```python
# Change from:
app.run(debug=True, host='0.0.0.0', port=5000)
# To:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### ❌ "Module not found: flask"
```bash
pip install -r requirements.txt
```

### ❌ "Java not found" (Windows)
Some Windows versions show Java errors - these are harmless. Flask will still run.

### ❌ Page formatting looks wrong
- Press **Ctrl+F5** (hard refresh) to clear browser cache
- Check internet connection for CDN resources

### ❌ Can't upload files
- File must be PDF, JPG, or PNG
- File size must be under 10MB
- Check write permissions on `uploads/` folder

---

## 🛑 How to Stop Application

**In Terminal**: Press **CTRL + C**

```
^C
```

---

## 📱 Access URL

```
http://localhost:5000
```

### Pages Reference
- `/register` → Student registration
- `/login` → Login page
- `/student/dashboard` → Student portal
- `/mentor/dashboard` → Mentor portal
- `/logout` → Logout (from any page)

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Virtual environment activated (shows "venv" in terminal)
- [ ] Flask installed (no errors from `pip install`)
- [ ] App running on http://localhost:5000
- [ ] Can access login page
- [ ] Can register student account
- [ ] Can login as student
- [ ] Can see student dashboard
- [ ] Can login as mentor
- [ ] Can see mentor dashboard
- [ ] Can upload achievement
- [ ] Can add mentor remark
- [ ] All files in correct folders

---

## 🎓 Next Steps for Production

1. **Add Real Mentors** → Edit `data/mentors.json`
2. **Secure Passwords** → Use environment variables for secret key
3. **Deploy** → Use Heroku, AWS, or college server
4. **Email Notifications** → Add email alerts for achievements
5. **Database Switch** → Replace JSON with PostgreSQL
6. **Backup System** → Automated data backup

---

## 📞 Need Help?

1. Check **README.md** for full documentation
2. Review app.py comments for code logic
3. Check browser console (F12) for JavaScript errors
4. Verify JSON files are not corrupted

---

**Status**: ✅ Ready to Run

Try it now! Execute: `python app.py`
