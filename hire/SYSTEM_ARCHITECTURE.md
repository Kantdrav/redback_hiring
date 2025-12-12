# Redback Platform - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    REDBACK INTERVIEW PLATFORM                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      USER AUTHENTICATION                          │
│  Login (Role Selection) → Email + Password + Admin Token (if)   │
│  Flask-Login Session Management                                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬─────────────────┬────────────────┐
│   ADMIN      │     HR       │   INTERVIEWER   │   CANDIDATE    │
│   ROLE       │     ROLE     │      ROLE       │     ROLE       │
└──────────────┴──────────────┴─────────────────┴────────────────┘
       │              │               │                 │
       ▼              ▼               ▼                 ▼
┌──────────┐  ┌──────────┐   ┌──────────────┐  ┌──────────────┐
│  ADMIN   │  │    HR    │   │ INTERVIEWER  │  │  CANDIDATE   │
│Dashboard │  │Dashboard │   │  Dashboard   │  │  Dashboard   │
│          │  │          │   │              │  │              │
│• Users   │  │• Jobs    │   │• Assigned    │  │• Job Board   │
│• Langs   │  │• Plans   │   │  Interviews  │  │• My Apps     │
│• Q-Banks │  │• Schedules   │• Grading     │  │• Interviews  │
│• Policies│  │• Recommend   │• Test Review │  │• Take Tests  │
│• Audit   │  │             │• Coding Review   │• View Results│
└──────────┘  └──────────────┘   │              │
       │              │           │              │
       └──────────────┴───────────┴──────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │   FLASK BLUEPRINTS   │
            ├──────────────────────┤
            │ /admin/*             │
            │ /hr/*                │
            │ /interviewer/*       │
            │ /candidate/*         │
            └──────────────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │   DATABASE MODELS    │
            ├──────────────────────┤
            │ User                 │
            │ Job                  │
            │ Candidate            │
            │ InterviewPlan        │
            │ InterviewSchedule    │
            │ ProgrammingLanguage  │
            │ QuestionBank         │
            │ QuestionBankItem     │
            │ ScoringPolicy        │
            │ RoundTemplate        │
            │ CandidateTestResult  │
            │ Assessment           │
            │ AuditLog             │
            └──────────────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │   SQLITE DATABASE    │
            │  instance/           │
            │  interviewflow.sqlite│
            └──────────────────────┘
```

---

## Role-Based Access Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER LOGIN FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Select Role (Admin/HR/Interviewer/Candidate)               │
│  2. Enter Email & Password                                      │
│  3. If Admin: Also Enter Security Token                         │
│  4. Validate Credentials in Database                            │
│  5. Validate Role Matches User's Role                           │
│  6. If Admin: Validate Token against ADMIN_BYPASS_TOKEN        │
│  7. Create Session with Flask-Login                             │
│  8. Redirect to Role-Specific Dashboard                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

     ┌─────────────────┬──────────────────┬──────────────────┬─────────────┐
     │                 │                  │                  │             │
     ▼                 ▼                  ▼                  ▼             ▼
   ADMIN            HR              INTERVIEWER          CANDIDATE
   Dashboard        Dashboard       Dashboard            Dashboard
   
   /admin/          /hr/            /interviewer/        /candidate/
   dashboard        dashboard       dashboard            dashboard
```

---

## Admin Feature Workflow

```
┌──────────────────────────────────────────────────┐
│         ADMIN CONFIGURATION WORKFLOW             │
└──────────────────────────────────────────────────┘

1. LANGUAGE SETUP
   ├─ Create Programming Language
   │  (Python, Java, JavaScript, etc.)
   └─ Enable/Disable Language

2. QUESTION BANK SETUP
   ├─ Create Question Bank per Language
   ├─ Add Questions with:
   │  ├─ Question Text
   │  ├─ Type (MCQ/Coding/Essay)
   │  ├─ Difficulty (Easy/Medium/Hard)
   │  ├─ Time Limit (seconds)
   │  └─ Correct Answer
   └─ Enable/Disable Questions

3. POLICY SETUP
   ├─ Create Scoring Policy
   │  ├─ Set Passing Score (0-100)
   │  └─ Set Weights:
   │     ├─ Technical: 40%
   │     ├─ Coding: 30%
   │     └─ HR: 30%
   └─ Enable/Disable Policy

4. TEMPLATE SETUP
   ├─ Create Round Template
   │  ├─ Type (HR/Technical/MCQ/Coding/Live)
   │  ├─ Duration (minutes)
   │  └─ Configuration
   └─ Enable/Disable Template

5. USER MANAGEMENT
   ├─ Create Users (All Roles)
   ├─ Edit User Details
   ├─ Assign Roles
   └─ Deactivate Users

6. AUDIT LOGS
   ├─ View All Actions
   ├─ Filter by User/Entity
   ├─ View Payloads
   └─ Export Reports
```

---

## HR Interview Setup Workflow

```
┌──────────────────────────────────────────────────┐
│     HR INTERVIEW PLANNING WORKFLOW               │
└──────────────────────────────────────────────────┘

1. CREATE JOB OPENING
   ├─ Job Title
   ├─ Department
   ├─ Location
   ├─ Description
   └─ Set Status (Open/Closed)

2. DESIGN INTERVIEW PLAN
   ├─ Plan Name
   ├─ Link to Job
   │
   ├─ ROUND 1: HR SCREENING
   │  ├─ Duration: 30 mins
   │  ├─ Questions: HR Script
   │  └─ Interviewer: Assign HR
   │
   ├─ ROUND 2: TECHNICAL MCQ
   │  ├─ Language: Python
   │  ├─ Question Bank: Python Basics
   │  ├─ Questions: 20
   │  ├─ Time Limit: 60 mins
   │  └─ Passing Score: 60%
   │
   └─ ROUND 3: CODING CHALLENGE
      ├─ Language: Python
      ├─ Question Bank: Coding Problems
      ├─ Questions: 3
      ├─ Time Limit: 120 mins
      └─ Passing Score: 70%

3. INVITE CANDIDATES
   ├─ Select Candidate
   ├─ Select Interview Plan
   ├─ Create Schedule
   └─ Send Invitation

4. MONITOR INTERVIEWS
   ├─ View Status (Invited/In-Progress/Completed)
   ├─ Track Progress by Round
   ├─ View Scores
   └─ Recommend Pass/Fail

5. MAKE RECOMMENDATIONS
   ├─ Review All Round Results
   ├─ Add HR Notes
   ├─ Recommend: PASS or FAIL
   └─ Send Decision to Candidate
```

---

## Candidate Interview Journey

```
┌──────────────────────────────────────────────────┐
│     CANDIDATE INTERVIEW JOURNEY                  │
└──────────────────────────────────────────────────┘

START
  │
  ▼
BROWSE JOB BOARD
  │ (Search, Filter by title/dept)
  ▼
SELECT JOB
  │ (View details, requirements)
  ▼
APPLY FOR JOB
  │ (One-click application)
  ▼
RECEIVE INVITATION
  │ (Email notification)
  ▼
ACCEPT/DECLINE
  │ (Option to decline)
  ├─ DECLINE → Journey Ends
  │
  └─ ACCEPT → Proceed to Interview
      │
      ▼
    ROUND 1: HR SCREENING
      │ (Live or scheduled interview)
      ▼
    ROUND 2: TECHNICAL ASSESSMENT
      │ (20 MCQ questions, 60 minutes)
      │ Questions auto-graded
      ▼
    ROUND 3: CODING CHALLENGE
      │ (3 coding problems, 120 minutes)
      │ Interviewer reviews code
      ▼
    VIEW RESULTS
      │ (Score, Feedback, Pass/Fail)
      ▼
    ┌─────────────┬─────────────┐
    │ PASSED      │ FAILED      │
    │             │             │
    ▼             ▼
  OFFER        FEEDBACK
  LETTER       & REAPPLY
    │           LATER
    ▼           │
  ACCEPT        ▼
  OFFER       (Back to Job Board)
    │
    ▼
  ONBOARDING

```

---

## Interviewer Review Workflow

```
┌──────────────────────────────────────────────────┐
│    INTERVIEWER GRADING WORKFLOW                  │
└──────────────────────────────────────────────────┘

LOGIN AS INTERVIEWER
  │
  ▼
VIEW ASSIGNED INTERVIEWS
  │ (Filter: Scheduled/Completed)
  ▼
SELECT INTERVIEW
  │
  ├─ MANUAL INTERVIEW (Needs Grading)
  │  │
  │  ▼
  │ OPEN GRADING FORM
  │  │
  │  ├─ Score: 0-100
  │  ├─ Feedback: Text
  │  └─ Submit
  │  │
  │  ▼
  │ MARK COMPLETED
  │  │
  │  └─ Score Recorded
  │
  └─ AUTO-GRADED TEST (Review Results)
     │
     ▼
    VIEW TEST RESULT
     │
     ├─ MCQ Results (Auto-graded)
     │  ├─ Score: 85/100
     │  ├─ Questions Answered
     │  └─ Correct/Incorrect
     │
     └─ CODING RESULTS
        ├─ Code Submitted
        ├─ Test Cases: 8/10 Pass
        ├─ Score: 75/100
        └─ Review Code
           │
           ├─ Accept (PASS)
           ├─ Needs Discussion
           └─ Reject (FAIL)
```

---

## Database Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE SCHEMA RELATIONSHIPS                   │
└─────────────────────────────────────────────────────────────────┘

                           USERS
                          /    \
                        /        \
                    ADMIN      ADMIN_RESOURCES
                    │         /    |     \    \
                    │        /     |      \    \
                Languages  Questions  Policies  Templates
                    │         │
                    │         │
            Question      Question
            Banks         Items
                    │
                    │
                    ▼
                HR_RESOURCES
                /    |    \
              /      |      \
           Jobs   Plans    Schedules
                    │        │
                    └────────┼────────────┐
                             │            │
                             ▼            ▼
                        Candidates   Test_Results
                             │            │
                             └────────┬───┘
                                      │
                              Interview_Sessions


CANDIDATE PATH:
User (candidate) 
  └─ Candidate (Profile)
      └─ Applications (Jobs)
           └─ Interview Schedule
                └─ Test Results
                     └─ Assessment


INTERVIEWER PATH:
User (interviewer)
  └─ Interview Assignments
       └─ Test Results (Review)
            └─ Assessment (Grade)


ADMIN PATH:
User (admin)
  └─ Question Banks
  └─ Scoring Policies
  └─ Round Templates
  └─ Languages
  └─ Audit Logs
```

---

## API Request/Response Flow

```
┌────────────────────────────────────────────────────────┐
│    TYPICAL REQUEST-RESPONSE FLOW                       │
└────────────────────────────────────────────────────────┘

CLIENT REQUEST
    │
    ▼
  HTTP Request (POST/GET)
    │ /admin/question-banks/create
    │ POST data: {language_id, title, ...}
    │
    ▼
FLASK ROUTE HANDLER
    │
    ├─ @login_required decorator
    │  └─ Check Flask-Login session
    │
    ├─ @role_required('admin') decorator
    │  └─ Check user.role == 'admin'
    │
    ├─ Extract form data
    │  └─ Validate inputs
    │
    ├─ Create database record
    │  └─ db.session.add(record)
    │  └─ db.session.commit()
    │
    ├─ Log action to audit
    │  └─ log_admin_action(...)
    │
    ├─ Flash message to user
    │  └─ flash("Success!", "success")
    │
    └─ Render or redirect
       └─ return redirect(url_for(...))
           OR
           return render_template(..., data=data)
       │
       ▼
    HTTP Response (200/302/400/403)
       │
       ▼
    CLIENT RECEIVES RESPONSE
       │
       └─ Display page or redirect
```

---

## Security Layers

```
┌──────────────────────────────────────────────────────────────┐
│                   SECURITY ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────┘

LAYER 1: AUTHENTICATION
  ├─ Password Hashing (Werkzeug)
  ├─ Session Management (Flask-Login)
  ├─ Role Selection at Login
  ├─ Admin Token Verification
  └─ Email Verification (Future)

LAYER 2: AUTHORIZATION
  ├─ Role-Based Access Control (RBAC)
  │  └─ @role_required decorator
  ├─ Login Required Check
  │  └─ @login_required decorator
  └─ Resource-Level Authorization
     └─ Check user_id in route handlers

LAYER 3: DATA ISOLATION
  ├─ Candidates see only their data
  ├─ HR sees only their jobs/interviews
  ├─ Interviewers see only assigned interviews
  └─ Admin sees all data

LAYER 4: AUDIT TRAIL
  ├─ Log all admin actions
  ├─ Log all HR actions
  ├─ Log all interviewer actions
  ├─ Log all candidate actions
  └─ Timestamp all actions

LAYER 5: VALIDATION
  ├─ Input validation (required fields)
  ├─ Type validation (integers, emails)
  ├─ Range validation (scores 0-100)
  ├─ Uniqueness validation (email, username)
  └─ Relationship validation (FK integrity)

LAYER 6: ERROR HANDLING
  ├─ 404 for missing resources (.get_or_404)
  ├─ 403 for unauthorized access
  ├─ Flash messages for errors
  ├─ Redirect to appropriate page
  └─ No sensitive data in errors
```

---

## Data Flow: Job Application to Hire

```
┌──────────────────────────────────────────────────────────────┐
│         COMPLETE DATA FLOW: JOB → APPLICATION → HIRE         │
└──────────────────────────────────────────────────────────────┘

1. JOB CREATION
   HR creates job → stores in Job table
   
2. INTERVIEW PLAN
   HR designs plan → stores in InterviewPlan table
   HR links question banks → stores in round_order_json
   
3. CANDIDATE APPLICATION
   Candidate applies → stores in Candidate table
   Application linked to Job
   
4. INVITE CANDIDATE
   HR invites candidate → creates InterviewSchedule
   Status: 'invited'
   
5. CANDIDATE ACCEPTS
   Candidate accepts → InterviewSchedule status: 'in_progress'
   
6. ROUND 1: HR SCREENING
   Interviewer grades → creates Assessment record
   
7. ROUND 2: MCQ TEST
   Candidate takes test → creates CandidateTestResult
   Auto-graded and stored
   
8. ROUND 3: CODING
   Candidate submits code → creates CandidateTestResult
   Interviewer reviews → adds comments
   
9. FINAL SCORE
   Compute overall_score for InterviewSchedule
   Store in interview_schedules.overall_score
   
10. RECOMMENDATION
    HR recommends PASS/FAIL → stored in feedback_json
    
11. OFFER/REJECTION
    If PASS → generate offer letter
    If FAIL → send feedback & allow reapply
    
12. AUDIT LOG
    All steps tracked in audit_logs table
```

---

## Technology Stack

```
┌──────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                            │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  BACKEND FRAMEWORK:                                           │
│  └─ Flask 2.3.3                                              │
│     ├─ Flask-Login 0.6.2 (Sessions)                          │
│     ├─ Flask-SQLAlchemy 2.x (ORM)                            │
│     └─ Werkzeug (Security, Password Hashing)                 │
│                                                                │
│  DATABASE:                                                    │
│  └─ SQLite3 (Development)                                    │
│     └─ PostgreSQL (Production Ready)                         │
│                                                                │
│  FRONTEND:                                                    │
│  ├─ HTML5                                                     │
│  ├─ CSS3 / Bootstrap 5                                       │
│  ├─ JavaScript (ES6+)                                        │
│  └─ Jinja2 (Templates)                                       │
│                                                                │
│  PYTHON VERSION:                                              │
│  └─ Python 3.10+                                             │
│                                                                │
│  OPTIONAL (Future):                                           │
│  ├─ Celery (Async Tasks)                                     │
│  ├─ Redis (Caching)                                          │
│  ├─ PostgreSQL (Scalable DB)                                 │
│  ├─ Docker (Containerization)                                │
│  ├─ Gunicorn (Production Server)                             │
│  └─ Nginx (Reverse Proxy)                                    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Scalability Architecture

```
┌──────────────────────────────────────────────────────────────┐
│        SCALABILITY & DEPLOYMENT ARCHITECTURE                  │
└──────────────────────────────────────────────────────────────┘

DEVELOPMENT:
  Client → Flask Dev Server (5000)

PRODUCTION - SINGLE SERVER:
  Client → Nginx (Reverse Proxy, Port 80)
           → Gunicorn (App Server, 4 workers)
           → Flask App
           → PostgreSQL (DB)

PRODUCTION - SCALED:
  Clients
    ↓
  Load Balancer (Nginx/HAProxy)
    ↓
  ┌─ App Server 1 (Gunicorn)
  ├─ App Server 2 (Gunicorn)
  └─ App Server 3 (Gunicorn)
    ↓
  Session Store (Redis)
    ↓
  Database Cluster (PostgreSQL)
    ├─ Master (Write)
    ├─ Replica 1 (Read)
    └─ Replica 2 (Read)
    ↓
  Object Storage (S3 for uploads)
    ↓
  Cache (Redis)
  
  Async Tasks (Celery)
    ├─ Email Notifications
    ├─ Report Generation
    └─ Data Processing
```

---

**This architecture provides a secure, scalable, and maintainable platform for managing interviews and assessments with clear role-based workflows.**

