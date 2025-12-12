# PHASE 4 – HR Dashboards, Reports, Analytics, CSV Exports

## Overview
Complete HR management suite with interactive dashboards, advanced analytics, filtering, and CSV export capabilities for data-driven recruitment decisions.

## Components Implemented

### 1. **HR Analytics Service** (`services/hr_analytics.py`)

#### Key Metrics
- Total candidates and jobs
- Open positions
- Average match scores
- Recent applications (7-day window)
- Candidate status distribution

#### Filtering & Search
- Filter by job position
- Filter by application status (applied, screening, interview, offer, hired, rejected)
- Filter by minimum match score
- Full-text search by name or email
- Paginated results (20 per page)

#### Analytics Functions
- **Skill Demand**: Top 15 in-demand technical skills across jobs
- **Experience Distribution**: Candidate experience buckets
- **Match Score Distribution**: Score breakdown (90-100, 80-89, etc.)
- **Hiring Funnel**: Pipeline breakdown by stage
- **Job Summary**: Candidates per job with average match scores
- **Top Candidates**: Highest-scoring candidates overall or per-job
- **Recent Activity**: Last 20 uploaded resumes

### 2. **CSV Export Service** (`services/csv_exporter.py`)

#### Export Options
1. **Candidates Export**
   - Name, Email, Phone
   - Applied Position, Status
   - Match Score, Resume Path
   - Application Date

2. **Detailed Candidates Export**
   - All of above plus
   - Experience Years, Skills
   - Notes/Flags

3. **Jobs Export**
   - Title, Department, Location
   - Status, Created Date
   - Candidate Count
   - Average Match Score

4. **Analytics Export**
   - Key metrics summary
   - Dashboard snapshot

5. **Skill Demand Export**
   - Skill name and job posting count
   - Top 15 skills ranked

6. **Hiring Funnel Export**
   - Stage breakdown
   - Counts and percentages

#### Features
- Timestamped filenames
- UTF-8 encoding with proper escaping
- Professional formatting

### 3. **HR Dashboard Routes** (`routes/hr_dashboard.py`)

#### Main Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/dashboard/` | GET | Main HR dashboard |
| `/dashboard/candidates` | GET | Candidates list with filters |
| `/dashboard/analytics` | GET | Analytics and reports |
| `/dashboard/reports` | GET | Reports and exports hub |
| `/dashboard/export/candidates` | GET | Download candidates CSV |
| `/dashboard/export/jobs` | GET | Download jobs CSV |
| `/dashboard/export/analytics` | GET | Download analytics CSV |
| `/dashboard/export/skills` | GET | Download skill demand CSV |
| `/dashboard/export/funnel` | GET | Download hiring funnel CSV |
| `/dashboard/candidate/<id>/update-status` | POST | Update candidate status |
| `/dashboard/api/metrics` | GET | JSON metrics API |
| `/dashboard/api/funnel` | GET | JSON funnel API |
| `/dashboard/api/skills` | GET | JSON skills API |

#### Access Control
- Requires `login_required`
- Role-based: `admin` or `hr`
- Using `@role_required` decorator

### 4. **Dashboard Templates**

#### `dashboard/index.html` (Main Dashboard)
- **Key Metrics Cards**
  - Total Candidates
  - Open Jobs
  - Average Match Score
  - Recent Applications (7d)
  
- **Recent Activity**
  - Last 10 uploaded resumes
  - Name, Email, Status, Date
  
- **Top Candidates**
  - Top 5 by match score
  - Name, Email, Score badge
  
- **Status Distribution**
  - Breakdown by application status
  
- **Quick Actions**
  - View All Candidates
  - Analytics & Reports
  - Generate Report
  - Manage Jobs

#### `dashboard/candidates.html` (Filtered Candidates List)
- **Advanced Filters**
  - Search by name/email
  - Filter by job
  - Filter by status
  - Filter by min match score
  
- **Candidates Table**
  - Name, Email, Phone
  - Applied Position, Status badge
  - Match Score progress bar
  - Applied Date
  - Actions (View Report, Update Status)
  
- **Pagination**
  - 20 results per page
  - Previous/Next navigation
  - Direct page navigation
  
- **Status Update Modal**
  - Change candidate status inline
  - 6 status options

#### `dashboard/analytics.html` (Analytics & Insights)
- **Key Metrics Cards**
  - Total Candidates
  - Total Jobs
  - Average Match Score
  - Recent Applications
  
- **Hiring Funnel**
  - 6-stage pipeline visualization
  - Count and percentage per stage
  
- **Match Score Distribution**
  - 5 score ranges
  - Progress bars
  - Candidate counts
  
- **Top In-Demand Skills**
  - Top 15 technical skills
  - Job posting count per skill
  
- **Job Summary Table**
  - Job titles
  - Total candidates per job
  - Average match score per job
  - Breakdown by status

#### `dashboard/reports.html` (Reports & Exports Hub)
- **Report Sections**
  - Candidate Reports
  - Analytics Reports
  - Job Reports
  - Dashboard Navigation
  
- **Each Section**
  - Description of export
  - What data is included
  - Direct download link
  
- **Current Metrics**
  - Summary stats display

### 5. **Enhanced Navigation** (`base.html`)
- **Bootstrap 5 Navbar**
- **Responsive Design**
- **Dashboard Dropdown** (for HR/Admin)
  - Overview
  - Candidates
  - Analytics
  - Reports
  
- **Flash Message Display**
  - Bootstrap alert styling
  - Dismissible alerts

## Database Schema Updates

### Candidate Model
```python
class Candidate(db.Model):
    # ... existing fields ...
    match_score = db.Column(db.Integer, default=0)  # 0-100
    
    # Relationships
    job = db.relationship("Job", backref="candidates")
    user = db.relationship("User", backref="candidates")
```

## Key Features

### ✅ **Comprehensive Filtering**
- Multi-field search
- Combined filters
- Status-based filtering
- Match score threshold
- Pagination support

### ✅ **Advanced Analytics**
- Hiring funnel visualization
- Match score distribution
- Skill demand analysis
- Experience metrics
- Job-specific summaries

### ✅ **Data Export**
- Multiple export formats
- Timestamped files
- Professional CSV formatting
- One-click downloads

### ✅ **Role-Based Access**
- HR and Admin only
- Protected routes
- Secure API endpoints

### ✅ **Responsive UI**
- Bootstrap 5 framework
- Mobile-friendly tables
- Collapsible sections
- Accessible forms

### ✅ **Real-Time Updates**
- Status changes persist
- Match scores saved
- Metadata synchronized

## Workflow Examples

### Admin Creates Report
```
Dashboard → Reports → Select Export Type → Download CSV
```

### HR Reviews Candidates
```
Candidates List → Filter by Job → Sort by Match Score → View Top Candidates
```

### Analyze Hiring Pipeline
```
Analytics → View Funnel → Review Stage Breakdown → Export Funnel Data
```

## API Endpoints for Integration

### Get Metrics (JSON)
```
GET /dashboard/api/metrics
Response: {
  "total_candidates": 45,
  "total_jobs": 12,
  "open_jobs": 5,
  "avg_match_score": 72.3,
  "recent_applications_7d": 8,
  ...
}
```

### Get Hiring Funnel (JSON)
```
GET /dashboard/api/funnel
Response: {
  "applied": 45,
  "screening": 20,
  "interview": 8,
  "offer": 2,
  "hired": 1,
  "rejected": 14
}
```

### Get Skill Demand (JSON)
```
GET /dashboard/api/skills
Response: {
  "skills": [
    {"skill": "Python", "count": 12},
    {"skill": "AWS", "count": 10},
    ...
  ]
}
```

## Security Considerations

1. **Authentication**: All routes require `@login_required`
2. **Authorization**: Role-based access with `@role_required("admin", "hr")`
3. **Data Privacy**: Only shows candidates accessible to authenticated user
4. **SQL Injection**: Using SQLAlchemy ORM with parameterized queries
5. **CSRF Protection**: Forms include CSRF token handling

## Performance Optimizations

1. **Pagination**: Limits database queries to 20 results per page
2. **Lazy Loading**: Relationships loaded on-demand
3. **CSV Generation**: Streamed response (no in-memory file)
4. **Caching Ready**: API endpoints can be easily cached

## Future Enhancements

1. **Advanced Charts**: Plotly/Chart.js integration for visualizations
2. **Scheduled Reports**: Email reports on a schedule
3. **Custom Metrics**: User-defined KPIs
4. **Bulk Actions**: Update multiple candidates at once
5. **Interview Calendar**: Calendar view of scheduled interviews
6. **Offer Management**: Track and manage offers
7. **Analytics Dashboard**: Real-time metrics dashboard
8. **Audit Logs**: Track all HR actions

## Testing the System

1. **Login as HR/Admin**
   - Use admin bypass token: `admin-access-token-2025`

2. **Create Sample Data**
   - Create jobs: `/jobs/create`
   - Upload resumes: `/rag/upload_resume`
   - System auto-calculates match scores

3. **Test Filtering**
   - Dashboard → Candidates
   - Apply various filters
   - Verify results update

4. **Test Exports**
   - Dashboard → Reports
   - Click export buttons
   - Verify CSV downloads

5. **Test Analytics**
   - Dashboard → Analytics
   - Review all visualizations
   - Check funnel breakdown

---

**Status**: ✅ Phase 4 Complete
**Version**: 1.0
**Last Updated**: December 12, 2025
