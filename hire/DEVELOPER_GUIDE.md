# Redback - Developer Quick Reference

## Project Structure

```
/hire/
├── app.py                          # Flask app factory & blueprints
├── models.py                       # SQLAlchemy models (extended)
├── auth.py                         # Authentication & login
├── config.py                       # Configuration
├── utils/
│   └── rbac.py                     # Role-based access control decorator
├── routes/
│   ├── admin_dashboard.py          # Admin management routes
│   ├── admin_users.py              # User management routes
│   ├── hr_jobs.py                  # HR job/interview routes
│   ├── interviewer.py              # Interviewer grading routes
│   ├── candidate.py                # Candidate job/interview routes
│   ├── interviews.py               # Legacy interview routes
│   └── hr_dashboard.py             # Legacy HR routes
├── templates/
│   ├── admin/                      # Admin templates (needed)
│   ├── hr/                         # HR templates (needed)
│   ├── interviewer/                # Interviewer templates (needed)
│   ├── candidate/                  # Candidate templates (needed)
│   ├── auth/                       # Authentication templates
│   └── base.html                   # Base template
├── services/
│   └── interview_engine.py         # Interview logic
├── instance/
│   └── interviewflow.sqlite        # SQLite database
└── ROLE_BASED_FEATURES.md          # Feature documentation
```

---

## Key Models Quick Reference

### User Extended
```python
User(
    email='user@example.com',
    password_hash='hashed...',
    name='Full Name',
    role='admin|hr|interviewer|candidate',
    is_active=True,
    permissions_json='{}'
)
```

### Admin Models
```python
# Programming Language
ProgrammingLanguage(name='Python', enabled=True)

# Question Bank
QuestionBank(
    language_id=1,
    title='Python Basics',
    enabled=True,
    created_by=admin_user_id
)

# Question Bank Item
QuestionBankItem(
    bank_id=1,
    question_text='What is...',
    question_type='mcq|coding|essay',
    difficulty='easy|medium|hard',
    enabled=True,
    time_limit_seconds=300
)

# Scoring Policy
ScoringPolicy(
    name='Standard Policy',
    policy_json='{"passing_score":60,"weights":{...}}',
    created_by=admin_user_id
)

# Round Template
RoundTemplate(
    name='Technical Round',
    type='technical|hr|mcq|coding|live',
    duration_minutes=60,
    created_by=admin_user_id
)
```

### HR Models
```python
# Interview Plan
InterviewPlan(
    job_id=1,
    name='Interview Plan v1',
    round_order_json='[...]',
    status='draft|active|archived',
    created_by=hr_user_id
)

# Interview Schedule
InterviewSchedule(
    candidate_id=1,
    interview_plan_id=1,
    current_round_index=0,
    status='invited|in_progress|completed|rejected'
)

# Candidate Test Result
CandidateTestResult(
    interview_schedule_id=1,
    round_index=0,
    round_type='mcq',
    language_tested='Python',
    score=85.5,
    max_score=100,
    test_data_json='{...}'
)
```

---

## Routes Quick Reference

### Admin Routes `/admin`
```
GET/POST   /dashboard
GET/POST   /languages
GET/POST   /languages/add
GET/POST   /languages/<id>/edit
GET/POST   /question-banks
GET/POST   /question-banks/create
GET/POST   /question-banks/<id>/edit
GET/POST   /question-banks/<id>/questions/add
GET/POST   /scoring-policies
GET/POST   /scoring-policies/create
GET/POST   /scoring-policies/<id>/edit
GET/POST   /round-templates
GET/POST   /round-templates/create
GET/POST   /round-templates/<id>/edit
GET        /audit-logs
```

### HR Routes `/hr`
```
GET        /dashboard
GET/POST   /jobs
GET/POST   /jobs/create
GET/POST   /jobs/<id>/edit
GET/POST   /interview-plans
GET/POST   /interview-plans/create
GET/POST   /interview-plans/<id>/edit
GET        /candidates
GET/POST   /interview-schedules
GET/POST   /interview-schedules/create
POST       /interview-schedules/<id>/recommend
```

### Interviewer Routes `/interviewer`
```
GET        /dashboard
GET        /interviews
GET        /interviews/<id>
GET/POST   /interviews/<id>/grade
GET        /test-results
GET        /test-results/<id>
POST       /test-results/<id>/review
GET        /coding-submissions
GET        /coding-submissions/<id>
```

### Candidate Routes `/candidate`
```
GET        /dashboard
GET        /job-board
POST       /apply/<job_id>
GET        /my-applications
GET        /interviews
POST       /interviews/<id>/accept
POST       /interviews/<id>/decline
GET        /test/<id>
POST       /test/<id>/submit
GET        /interview/<id>/outcome
```

---

## Authentication

### Login Endpoint
```
POST /auth/login
```

### Form Data
```python
email = 'user@example.com'
password = 'password123'
role = 'admin|hr|interviewer|candidate'
admin_token = 'admin-access-token-2025'  # Only for admin role
```

### Create User
```python
from models import User, db

user = User(
    email='newuser@example.com',
    name='New User',
    role='interviewer'
)
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

---

## Using RBAC Decorator

### In Route Handler
```python
from utils.rbac import role_required
from flask import Blueprint
from flask_login import login_required

@blueprint.route('/admin-only')
@login_required
@role_required('admin')
def admin_only():
    return "Admin access only"
```

### Multiple Roles
```python
@route_handler
@login_required
@role_required('admin', 'hr')  # Both admin and HR can access
def mixed_access():
    return "Admin or HR"
```

---

## Common Patterns

### Get Current User
```python
from flask_login import current_user

if current_user.role == 'admin':
    # Admin-specific logic
    pass
```

### Check Authorization
```python
user = User.query.get_or_404(user_id)
if user.created_by != current_user.id and current_user.role != 'admin':
    flash("Unauthorized", "danger")
    return redirect(url_for('some_route'))
```

### Log Action
```python
from models import AuditLog
import json

log = AuditLog(
    action='update',
    entity_type='question_bank',
    entity_id=bank_id,
    user_id=current_user.id,
    payload_json=json.dumps({'title': 'New Title'})
)
db.session.add(log)
db.session.commit()
```

### Parse JSON Fields
```python
# In model
policy = ScoringPolicy.query.get(1)
config = policy.get_policy()  # Parses JSON
print(config['passing_score'])

# Update JSON
config['passing_score'] = 75
policy.policy_json = json.dumps(config)
db.session.commit()
```

---

## Database Operations

### Create Record
```python
from models import db, QuestionBank

bank = QuestionBank(
    language_id=1,
    title='New Bank',
    created_by=current_user.id
)
db.session.add(bank)
db.session.commit()
```

### Update Record
```python
bank = QuestionBank.query.get(1)
bank.title = "Updated Title"
bank.enabled = False
db.session.commit()
```

### Delete Record
```python
bank = QuestionBank.query.get(1)
db.session.delete(bank)
db.session.commit()
```

### Query Examples
```python
# Get one
user = User.query.filter_by(email='admin@redback.local').first()

# Get all
admins = User.query.filter_by(role='admin').all()

# Filter and order
jobs = Job.query.filter_by(status='open').order_by(Job.created_at.desc()).all()

# Paginate
page = request.args.get('page', 1, type=int)
results = User.query.paginate(page=page, per_page=20)

# Count
count = User.query.filter_by(role='candidate').count()
```

---

## Flask Patterns

### Redirect After Form
```python
if request.method == "POST":
    # Process form
    db.session.commit()
    flash("Success!", "success")
    return redirect(url_for('some_view'))

return render_template('form.html')
```

### Handle 404
```python
record = Model.query.get_or_404(record_id)

# OR custom
record = Model.query.get(record_id)
if not record:
    flash("Not found", "danger")
    return redirect(url_for('list_view'))
```

### Filter Query Parameter
```python
status = request.args.get('status', 'all')
if status != 'all':
    query = query.filter_by(status=status)
```

---

## Template Patterns

### Include Base Template
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container">
    <!-- Content here -->
</div>
{% endblock %}
```

### Flash Messages
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### Loop with Pagination
```html
{% for item in items %}
    <tr>
        <td>{{ item.name }}</td>
    </tr>
{% endfor %}

<!-- Pagination -->
{% if items.has_prev %}<a href="?page=1">First</a>{% endif %}
{% for page_num in items.iter_pages() %}
    {% if page_num %}
        {% if page_num == items.page %}
            <strong>{{ page_num }}</strong>
        {% else %}
            <a href="?page={{ page_num }}">{{ page_num }}</a>
        {% endif %}
    {% endif %}
{% endfor %}
{% if items.has_next %}<a href="?page={{ items.pages }}">Last</a>{% endif %}
```

### Form Elements
```html
<form method="POST" action="{{ url_for('route_name') }}">
    <input type="text" name="field_name" required>
    <select name="role">
        <option value="admin">Admin</option>
        <option value="hr">HR</option>
    </select>
    <textarea name="description"></textarea>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---

## Troubleshooting

### Blueprint Registration Issues
```python
# In app.py - Make sure blueprint is registered
app.register_blueprint(admin_dashboard_bp, url_prefix="/admin")
```

### RBAC Decorator Not Working
```python
# Make sure rbac.py exists in utils/
from utils.rbac import role_required

# Decorator must be below @login_required
@route
@login_required
@role_required('admin')
def view():
    pass
```

### Database Model Not Creating
```python
# In app.py - make sure to run create_all()
with app.app_context():
    db.create_all()
```

### JSON Parse Errors
```python
# Always use try/except for JSON parsing
def get_policy(self):
    try:
        return json.loads(self.policy_json or "{}")
    except Exception:
        return {}
```

---

## Admin Credentials

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

## Testing Workflows

### Admin Test
1. Login: admin@redback.local / Admin@2025 / token
2. Go to `/admin/languages`
3. Add language "Python"
4. Go to `/admin/question-banks`
5. Create bank for Python

### HR Test
1. Create HR user via admin
2. Login as HR
3. Go to `/hr/jobs`
4. Create job opening
5. Go to `/hr/interview-plans`
6. Create plan and add rounds

### Interviewer Test
1. Create interviewer via admin
2. Admin assigns interview to interviewer
3. Login as interviewer
4. Go to `/interviewer/interviews`
5. Grade interview

### Candidate Test
1. Self-register as candidate
2. Go to `/candidate/job-board`
3. Apply for job
4. Get invited to interview
5. Accept and take test
6. View results

---

## Performance Tips

- Use `.limit()` for large queries
- Use `.paginate()` for listing views
- Use `.first()` instead of `.all()[0]`
- Use `eager loading` for relationships:
  ```python
  from sqlalchemy.orm import joinedload
  User.query.options(joinedload(User.permissions)).all()
  ```

---

## Security Notes

- Always use `@role_required` for authorization
- Validate user permissions in route handlers
- Use `.get_or_404()` to prevent ID enumeration
- Hash passwords with `user.set_password()`
- Log all admin actions to audit trail
- Never expose passwords in logs
- Use HTTPS in production
- Validate form inputs
- Prevent SQL injection with ORM

---

## Useful Commands

```bash
# Activate env
source .venv/bin/activate

# Run server
python app.py

# Reset database (delete and recreate)
rm instance/interviewflow.sqlite
python app.py  # Creates on startup

# Create admin
python create_admin.py

# Check Python version
python --version

# Install package
pip install package_name

# List packages
pip list

# View logs
tail -f logs/app.log
```

---

## Documentation Files

- `ROLE_BASED_FEATURES.md` - Comprehensive feature documentation
- `IMPLEMENTATION_SUMMARY.md` - Implementation overview
- `ADMIN_LOGIN_SYSTEM.md` - Admin authentication details
- `README.md` - Project overview

---

**Happy Coding! 🚀**

