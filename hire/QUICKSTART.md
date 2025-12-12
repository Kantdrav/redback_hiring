# Redback Platform - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Activate Environment
```bash
cd /home/kantdravi/Desktop/redback_it_sol/hire
source .venv/bin/activate
```

### Step 2: Start Application
```bash
python app.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

### Step 4: Login with Admin
```
Email:    admin@redback.local
Password: Admin@2025
Token:    admin-access-token-2025
Role:     Admin
```

---

## 📋 Quick Reference

### Admin Tasks
```
1. /admin/languages          → Add Python, Java, JavaScript
2. /admin/question-banks     → Create banks per language
3. /admin/question-banks/create → Add sample questions
4. /admin/scoring-policies   → Set weights and passing scores
5. /admin/round-templates    → Create interview templates
```

### HR Tasks
```
1. /hr/jobs/create           → Create job opening
2. /hr/interview-plans/create → Design interview process
3. /hr/interview-schedules   → Invite candidates
4. /hr/interview-schedules/<id>/recommend → Pass/Fail decision
```

### Interviewer Tasks
```
1. /interviewer/interviews   → View assigned interviews
2. /interviewer/interviews/<id>/grade → Grade interview
3. /interviewer/test-results → Review auto-graded tests
```

### Candidate Tasks
```
1. /candidate/job-board      → Browse jobs
2. /candidate/apply/1        → Apply for job
3. /candidate/interviews     → View invitations
4. /candidate/test/1         → Take test
5. /candidate/interview/1/outcome → View results
```

---

## 👥 Create Sample Users

### Option 1: Via Admin Panel
1. Go to `/admin/users/create`
2. Fill form with name, email, role, password
3. Click Create

### Option 2: Direct SQL
```python
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    # Create HR user
    hr = User(email='hr@redback.local', name='HR Manager', role='hr')
    hr.set_password('password123')
    
    # Create Interviewer
    interv = User(email='interviewer@redback.local', name='Interviewer', role='interviewer')
    interv.set_password('password123')
    
    # Create Candidate
    cand = User(email='candidate@redback.local', name='Candidate', role='candidate')
    cand.set_password('password123')
    
    db.session.add_all([hr, interv, cand])
    db.session.commit()
    print("Users created!")
```

---

## 🔑 Default Logins

### Admin
```
Email:    admin@redback.local
Password: Admin@2025
Token:    admin-access-token-2025
```

### Reset Admin
```bash
python create_admin.py
```

---

## 📂 Project Structure

```
/hire/
├── app.py                    (Flask app)
├── models.py                 (Database models)
├── auth.py                   (Login/authentication)
├── routes/
│   ├── admin_dashboard.py    (Admin features)
│   ├── hr_jobs.py            (HR features)
│   ├── interviewer.py        (Interviewer features)
│   ├── candidate.py          (Candidate features)
│   └── (other existing routes)
├── templates/
│   ├── admin/                (Admin templates - NEEDED)
│   ├── hr/                   (HR templates - NEEDED)
│   ├── interviewer/          (Interviewer templates - NEEDED)
│   ├── candidate/            (Candidate templates - NEEDED)
│   └── auth/                 (Login template)
└── (other directories)
```

---

## 📚 Documentation Files

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **README_IMPLEMENTATION.md** | Overview & status | 5 min |
| **ROLE_BASED_FEATURES.md** | Feature details | 15 min |
| **DEVELOPER_GUIDE.md** | Code reference | 10 min |
| **SYSTEM_ARCHITECTURE.md** | System design | 10 min |
| **IMPLEMENTATION_SUMMARY.md** | Technical details | 10 min |
| **COMPLETE_IMPLEMENTATION_REPORT.md** | Full report | 15 min |

---

## 🧪 Test Workflow

### 1. Admin Creates Content (5 min)
```
1. Login as admin
2. Create language "Python"
3. Create question bank "Python Basics"
4. Add 5 sample questions (MCQ type)
5. Create scoring policy "Standard"
6. Create round template "Technical MCQ"
```

### 2. HR Sets Up Interview (5 min)
```
1. Create HR user (if not exists)
2. Login as HR
3. Create job "Python Developer"
4. Create interview plan "Python Interview"
5. Add 2 rounds: HR Screening + Technical MCQ
6. Configure with Python question bank
```

### 3. Candidate Applies (3 min)
```
1. Create candidate user
2. Login as candidate
3. Browse job board
4. Apply for "Python Developer"
5. Check my applications
```

### 4. HR Invites Candidate (2 min)
```
1. Login as HR
2. Go to interview schedules
3. Invite candidate to interview plan
4. Candidate receives invitation
```

### 5. Candidate Takes Test (5 min)
```
1. Login as candidate
2. View interview invitations
3. Accept interview
4. Take technical test
5. Answer 5 MCQ questions
6. Submit and view results
```

### 6. Interviewer Reviews (3 min)
```
1. Create interviewer user
2. Login as interviewer
3. View assigned interviews
4. Review test results
5. Add comments/review
```

---

## 🐛 Common Issues & Solutions

### Issue: "Port 5000 already in use"
```bash
# Kill existing process
lsof -i :5000
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

### Issue: "ImportError: No module named 'models'"
```bash
# Make sure you're in the correct directory
cd /home/kantdravi/Desktop/redback_it_sol/hire

# Activate venv
source .venv/bin/activate
```

### Issue: "Database is locked"
```bash
# SQLite issue with concurrent access
# Stop Flask, restart
pkill -f "python app.py"
python app.py
```

### Issue: "Admin login fails with token"
```bash
# Check token in auth.py line 10
# Should be: admin-access-token-2025
# Make sure to enter it exactly on login form
```

---

## 📊 Database Status

### Check Database Exists
```bash
ls -lh instance/interviewflow.sqlite
```

### Reset Database (⚠️ Deletes all data)
```bash
rm instance/interviewflow.sqlite
python app.py  # Creates fresh database
```

### View Database Content
```python
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"{u.email} - {u.role}")
```

---

## 🔒 Security Reminders

- ✅ Admin token is for development only
- ✅ Change in production (`ADMIN_BYPASS_TOKEN` in auth.py)
- ✅ Use HTTPS in production
- ✅ Don't commit secrets to git
- ✅ Use environment variables for config

---

## 📱 API Testing

### Test with curl
```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -d "email=admin@redback.local&password=Admin@2025&role=admin&admin_token=admin-access-token-2025"

# Get admin dashboard
curl -X GET http://localhost:5000/admin/dashboard
```

### Test with Postman
1. Create login request: POST /auth/login
2. Include form data: email, password, role, admin_token
3. Save session cookie
4. Make subsequent requests with session

---

## 🎯 Next Steps

### Immediate (This Week)
- [ ] Verify all routes work
- [ ] Test CRUD operations
- [ ] Verify role-based access
- [ ] Check audit logs

### Short-term (Next Week)
- [ ] Create HTML templates
- [ ] Style with Bootstrap
- [ ] Test full workflows
- [ ] User acceptance testing

### Medium-term (This Month)
- [ ] Deploy to staging
- [ ] Load testing
- [ ] Security audit
- [ ] Performance optimization

---

## 📞 Need Help?

### Debug Mode (Get detailed errors)
```bash
export FLASK_DEBUG=1
python app.py
```

### Check Logs
```bash
# See Flask startup logs
# Should show "Running on http://127.0.0.1:5000"

# Check database
# instance/interviewflow.sqlite should exist

# Check routes
# Run: python -c "from app import create_app; app = create_app(); print([r for r in app.url_map.iter_rules()])"
```

### Common Routes Reference
```
Home:              http://localhost:5000/
Login:             http://localhost:5000/auth/login
Register:          http://localhost:5000/auth/register

Admin:             http://localhost:5000/admin/dashboard
HR:                http://localhost:5000/hr/dashboard
Interviewer:       http://localhost:5000/interviewer/dashboard
Candidate:         http://localhost:5000/candidate/dashboard
```

---

## 💡 Pro Tips

1. **Use browser DevTools** to inspect requests/responses
2. **Check console logs** for Flask debug messages
3. **Test with multiple roles** to verify RBAC
4. **Verify audit logs** for all actions
5. **Use admin to create test data** quickly
6. **Check email fields** are lowercase (auth.py does .lower())

---

## 📝 Feature Checklist

### Admin Features
- [ ] Login with token
- [ ] Manage languages
- [ ] Create question banks
- [ ] Add questions (MCQ, coding, essay)
- [ ] Create scoring policies
- [ ] Create round templates
- [ ] View audit logs

### HR Features
- [ ] Create job openings
- [ ] Create interview plans
- [ ] Configure interview rounds
- [ ] Invite candidates
- [ ] View interview status
- [ ] Recommend pass/fail

### Interviewer Features
- [ ] View assigned interviews
- [ ] Grade manual interviews
- [ ] Review auto-graded tests
- [ ] Review code submissions
- [ ] Add feedback/comments

### Candidate Features
- [ ] Browse jobs
- [ ] Apply for jobs
- [ ] Receive invitations
- [ ] Accept/decline
- [ ] Take tests
- [ ] View results

---

## 🎓 Learning Path

### Beginner (2 hours)
1. Read README_IMPLEMENTATION.md
2. Login as admin
3. Create a language
4. Create a question bank

### Intermediate (4 hours)
1. Create complete job setup
2. Create interview plan
3. Invite candidate
4. Test candidate journey

### Advanced (8 hours)
1. Read DEVELOPER_GUIDE.md
2. Understand database schema
3. Create custom reports
4. Extend with new features

---

## 🚀 Ready?

```
1. source .venv/bin/activate
2. python app.py
3. Open http://localhost:5000
4. Login with admin credentials
5. Start exploring!
```

**Questions?** Check the documentation files in the `/hire` directory.

**Found a bug?** Check browser console and Flask logs.

**Want to extend?** Read DEVELOPER_GUIDE.md for patterns and examples.

---

**Happy Testing! 🎉**

