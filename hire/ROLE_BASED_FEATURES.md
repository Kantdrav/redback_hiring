# Redback - Role-Based Features Documentation

## Overview

Redback is a comprehensive interview and assessment management platform with role-based access control. Each user role has specific capabilities, dashboards, and workflows.

---

## 1. ADMIN ROLE

### Capabilities
- Manage all users and assign roles (Admin, HR, Interviewer, Candidate)
- Configure scoring policies and set passing scores
- Manage round types and interview templates
- Manage technical FAQ/question banks per programming language
- Set question count, time limits, shuffle behavior for each language
- Set passing scores per language/round
- View comprehensive reports and audit logs
- System-wide configuration and monitoring

### Admin Dashboard Features

#### 1.1 User Management
- **Route**: `/admin/users`
- **Features**:
  - List all users with role badges
  - Create new users (any role)
  - Edit user details and roles
  - Disable/delete users
  - Assign permissions

#### 1.2 Programming Languages
- **Route**: `/admin/languages`
- **Features**:
  - Add/edit programming languages
  - Enable/disable languages
  - Track question banks per language
  - Support for: Python, Java, JavaScript, C++, Go, Rust, etc.

#### 1.3 Question Banks
- **Route**: `/admin/question-banks`
- **Features**:
  - Create question banks per programming language
  - Upload/add questions with:
    - **Question Types**: MCQ, Coding, Essay
    - **Difficulty Levels**: Easy, Medium, Hard
    - **Time Limits**: Configurable per question
    - **Enable/Disable**: Control which questions are active
  - Organize questions by:
    - Programming language
    - Difficulty
    - Question type
  - Shuffle options for randomization
  - Version control for question updates

#### 1.4 Scoring Policies
- **Route**: `/admin/scoring-policies`
- **Features**:
  - Define scoring policies with:
    - **Passing Score**: Global and per-round thresholds
    - **Weights**: Assign importance to different round types
      - Technical rounds: 40%
      - Coding rounds: 30%
      - HR screening: 30%
  - Create multiple policies for different job types
  - Enable/disable policies
  - Policy templates for reuse

#### 1.5 Round Templates
- **Route**: `/admin/round-templates`
- **Features**:
  - Create pre-configured round types:
    - HR (Screening/Communication)
    - Technical (Knowledge & Problem-solving)
    - MCQ (Auto-graded assessments)
    - Coding (Programming tasks)
    - Live (Real-time interviews)
  - Configure template settings:
    - Duration
    - Question count
    - Shuffle behavior
    - Pass/fail criteria

#### 1.6 Audit Logs
- **Route**: `/admin/audit-logs`
- **Features**:
  - Track all admin actions:
    - User creation/modification
    - Question bank changes
    - Policy updates
    - Template modifications
  - Log details include:
    - Action type
    - Entity modified
    - Timestamp
    - Payload (what changed)
  - Compliance and audit trail

---

## 2. HR ROLE (Human Resources)

### Capabilities
- Create job openings with descriptions
- Design interview plans with multiple rounds
- Invite candidates to interviews
- Schedule interviews
- Recommend pass/fail candidates
- Track candidate progress through interview stages
- Manage screening rounds (HR interviews)
- Generate candidate reports

### HR Dashboard Features

#### 2.1 Job Management
- **Route**: `/hr/jobs`
- **Features**:
  - Create job openings with:
    - Job title
    - Department
    - Location
    - Full description
  - Update job status (open/closed)
  - View applicants for each job
  - Manage job lifecycle

#### 2.2 Interview Planning
- **Route**: `/hr/interview-plans`
- **Features**:
  - Create interview plans linked to specific jobs
  - Configure multi-round interview process:
    1. HR Screening Round
    2. Technical Assessment (MCQ/Coding)
    3. Technical Interview (Live/Manual)
    4. Final Decision Round
  - Assign:
    - Round types (from admin templates)
    - Question banks per round
    - Time limits
    - Passing scores
    - Programming languages for technical rounds
  - Reuse templates across jobs

#### 2.3 Candidate Management
- **Route**: `/hr/candidates`
- **Features**:
  - View all candidates in system
  - Filter by status:
    - Applied
    - Shortlisted
    - In Interview
    - Offered
    - Rejected
  - Search candidates by name/email

#### 2.4 Interview Scheduling
- **Route**: `/hr/interview-schedules`
- **Features**:
  - Invite candidates to specific interview plans
  - Create interview schedules
  - Prevent duplicate invitations
  - Track interview status:
    - **invited**: Candidate hasn't responded
    - **in_progress**: Candidate accepted and taking test
    - **completed**: All rounds finished
    - **rejected**: Candidate declined or failed

#### 2.5 Candidate Recommendations
- **Route**: `/hr/interview-schedules/<id>/recommend`
- **Features**:
  - Recommend PASS or FAIL after all rounds
  - Add HR notes/comments
  - Track recommendation timestamp
  - Review all candidate feedback

#### 2.6 Reporting
- Generate candidate performance reports
- Track interview pipeline metrics
- View completion rates by stage

---

## 3. INTERVIEWER ROLE (Technical)

### Capabilities
- View assigned interviews only
- Grade manual technical tasks
- Review auto-graded MCQ/Coding results
- Access candidate coding submissions
- Provide feedback and scoring
- Rate candidate performance
- No access to question banks or scoring policies

### Interviewer Dashboard Features

#### 3.1 Assigned Interviews
- **Route**: `/interviewer/interviews`
- **Features**:
  - View only interviews assigned to them
  - Filter by status:
    - Scheduled
    - In Progress
    - Completed
  - View interview details:
    - Candidate name
    - Interview round
    - Scheduled time
    - Status

#### 3.2 Manual Grading
- **Route**: `/interviewer/interviews/<id>/grade`
- **Features**:
  - Score interviews on 0-100 scale
  - Add detailed feedback
  - Mark interview as completed
  - Submit grades to system
  - Audit trail of grading

#### 3.3 Test Result Review
- **Route**: `/interviewer/test-results`
- **Features**:
  - Review auto-graded test results:
    - MCQ responses and scores
    - Coding output verification
  - Add reviewer comments
  - Change result status:
    - **accepted**: Score is final
    - **needs_discussion**: Questionable answer
    - **rejected**: Score should be overridden
  - Flag issues for HR follow-up

#### 3.4 Coding Submissions
- **Route**: `/interviewer/coding-submissions`
- **Features**:
  - View submitted code
  - Review code quality
  - Check test case passes/fails
  - Add code review comments
  - Verify test output

#### 3.5 Dashboard Stats
- Total interviews assigned
- Pending reviews
- Completed evaluations
- Recent interview list

---

## 4. CANDIDATE ROLE

### Capabilities
- View open job positions
- Apply for jobs
- Accept/decline interview invitations
- Take online assessments and coding tests
- View test results and feedback
- Track interview status and outcomes
- Improve on feedback and reapply

### Candidate Dashboard Features

#### 4.1 Job Board
- **Route**: `/candidate/job-board`
- **Features**:
  - Browse all open job positions
  - Search and filter jobs by:
    - Job title
    - Department
    - Location
    - Keywords
  - View job details and requirements
  - One-click application

#### 4.2 My Applications
- **Route**: `/candidate/my-applications`
- **Features**:
  - Track all job applications
  - View application status
  - See application date
  - Know next steps

#### 4.3 Interview Invitations
- **Route**: `/candidate/interviews`
- **Features**:
  - Receive interview invitations
  - View interview details:
    - Invited date
    - Interview plan/rounds
    - Job position
    - Next steps
  - Accept interview invitation
  - Decline with optional reason
  - Track interview progress

#### 4.4 Take Tests
- **Route**: `/candidate/test/<schedule_id>`
- **Features**:
  - Access interview assessments when scheduled
  - Test types:
    - **MCQ Assessment**: Multiple choice questions
      - Auto-graded
      - Timer-based
      - Immediate feedback option
    - **Coding Challenge**: Write code in browser
      - Support for multiple languages
      - Built-in compiler
      - Test cases provided
      - Time-limited
    - **Technical Interview**: Questions from interviewer
  - Features during test:
    - Timer/countdown
    - Question navigation
    - Code editor syntax highlighting
    - Submit responses
  - Move through rounds sequentially
  - Submit each round before advancing

#### 4.5 View Results & Feedback
- **Route**: `/candidate/interview/<schedule_id>/outcome`
- **Features**:
  - View overall interview outcome
  - See round-by-round results:
    - Score received
    - Feedback from interviewer
    - Pass/fail status
  - Access detailed feedback only when released by HR
  - View areas for improvement
  - Understand next steps

#### 4.6 Profile Management
- Update profile information
- Manage interview preferences
- Review interview history

---

## Database Models

### User Model (Extended)
```python
class User:
  - id, email, password_hash
  - name, role, phone
  - is_active
  - permissions_json (granular permissions)
  - created_at, updated_at
```

### Admin Models
- **ProgrammingLanguage**: Language + enabled flag
- **QuestionBank**: Questions per language with metadata
- **QuestionBankItem**: Individual question with type/difficulty
- **ScoringPolicy**: Scoring rules and weights
- **RoundTemplate**: Pre-configured round types

### HR Models
- **Job**: Job openings
- **InterviewPlan**: Multi-round interview process
- **InterviewSchedule**: Candidate-specific interview instance

### Interview/Assessment Models
- **Interview**: Interviewer assignment for specific round
- **Assessment**: Manual grading results
- **CandidateTestResult**: Auto-graded test results

### Audit Model
- **AuditLog**: Track all actions with timestamps

---

## Authentication & Authorization

### Role-Based Access Control (RBAC)
```python
Admin:      All permissions
HR:         Job and interview management
Interviewer: View assigned interviews, grade, review tests
Candidate:  View jobs, apply, take tests
```

### Login Flow
1. Select role from dropdown (Admin, HR, Interviewer, Candidate)
2. Enter email and password
3. If Admin: Also enter security token
4. Validate credentials and role match
5. Redirect to role-specific dashboard

### Audit Trail
- Every action logged to AuditLog table
- Timestamp, user, action, entity, payload
- Compliance and security tracking

---

## Key Features by Role

| Feature | Admin | HR | Interviewer | Candidate |
|---------|-------|----|----|-----------|
| Manage Users | ✅ | ❌ | ❌ | ❌ |
| Question Banks | ✅ | ❌ | ❌ | ❌ |
| Scoring Policies | ✅ | ❌ | ❌ | ❌ |
| Create Jobs | ❌ | ✅ | ❌ | ❌ |
| Interview Plans | ❌ | ✅ | ❌ | ❌ |
| Invite Candidates | ❌ | ✅ | ❌ | ❌ |
| Grade Interviews | ❌ | ❌ | ✅ | ❌ |
| Review Tests | ❌ | ❌ | ✅ | ❌ |
| Apply for Jobs | ❌ | ❌ | ❌ | ✅ |
| Take Tests | ❌ | ❌ | ❌ | ✅ |
| View Results | ❌ | ❌ | ✅ | ✅ |
| Audit Logs | ✅ | ❌ | ❌ | ❌ |

---

## Default Admin Credentials

```
Email: admin@redback.local
Password: Admin@2025
Token: admin-access-token-2025
```

**To reset admin credentials:**
```bash
python create_admin.py
```

---

## API Routes Summary

### Admin Routes
```
GET/POST  /admin/dashboard              - Admin dashboard
GET/POST  /admin/languages              - List/manage languages
GET/POST  /admin/question-banks         - Manage question banks
GET/POST  /admin/scoring-policies       - Manage scoring policies
GET/POST  /admin/round-templates        - Manage round templates
GET       /admin/audit-logs             - View audit logs
GET/POST  /admin/users                  - User management
```

### HR Routes
```
GET       /hr/dashboard                 - HR dashboard
GET/POST  /hr/jobs                      - Job management
GET/POST  /hr/interview-plans           - Interview planning
GET       /hr/candidates                - Candidate list
GET/POST  /hr/interview-schedules       - Interview scheduling
POST      /hr/interview-schedules/<id>/recommend - Recommend candidate
```

### Interviewer Routes
```
GET       /interviewer/dashboard        - Interviewer dashboard
GET       /interviewer/interviews       - Assigned interviews
GET/POST  /interviewer/interviews/<id>/grade - Grade interview
GET       /interviewer/test-results     - Review test results
GET       /interviewer/coding-submissions - Review code
```

### Candidate Routes
```
GET       /candidate/dashboard          - Candidate dashboard
GET       /candidate/job-board          - Browse jobs
GET       /candidate/my-applications    - My job applications
GET/POST  /candidate/interviews         - Interview invitations
GET/POST  /candidate/test/<id>          - Take test
GET       /candidate/interview/<id>/outcome - View results
```

---

## Workflow Examples

### Complete Interview Process

#### 1. Admin Setup
```
1. Create programming languages (Python, Java, JavaScript)
2. Upload question banks per language
3. Create scoring policies (technical: 40%, coding: 30%, hr: 30%)
4. Create round templates (HR, Technical, Coding)
```

#### 2. HR Process
```
1. Create job opening ("Senior Python Developer")
2. Create interview plan (HR → Technical → Coding)
3. Configure each round:
   - Round 1: HR (screening)
   - Round 2: Technical MCQ (Python questions)
   - Round 3: Coding Challenge
4. Invite candidates to plan
5. Monitor interview progress
6. Make pass/fail recommendations
```

#### 3. Candidate Process
```
1. Browse job board
2. Apply for "Senior Python Developer"
3. Receive interview invitation
4. Accept interview
5. Take HR screening round
6. Take technical MCQ assessment
7. Take coding challenge
8. View results and feedback
9. If passed: receive offer
10. If improvement needed: reapply later
```

#### 4. Interviewer Process
```
1. See assigned interviews in dashboard
2. For manual rounds: grade and provide feedback
3. For auto-graded rounds: review results
4. For coding: review submitted code
5. Mark interview as completed
```

---

## Next Steps

- [ ] Create HTML templates for each role dashboard
- [ ] Implement test-taking interface
- [ ] Add email notification system
- [ ] Create candidate feedback system
- [ ] Implement video interview integration
- [ ] Add analytics and reporting dashboard
- [ ] Create API for third-party integrations
- [ ] Add candidate profile with resume
- [ ] Implement interview scheduling calendar
- [ ] Create offer letter generation

---

## Security Considerations

1. **Admin Token**: Only for admin login, change in production
2. **Password**: Hashed using Werkzeug security
3. **RBAC**: Enforced at route level with `@role_required` decorator
4. **Audit Trail**: All actions logged for compliance
5. **Data Privacy**: Candidates see only their own results
6. **Access Control**: Users can only access their own data/assignments

