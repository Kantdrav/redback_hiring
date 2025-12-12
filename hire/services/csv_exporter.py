"""
CSV Export Service - Export candidate data, reports, and analytics
"""
import csv
import io
from datetime import datetime
from models import Candidate, Job, User


class CSVExporter:
    """Handle CSV exports for HR reports"""
    
    @staticmethod
    def export_candidates_csv(candidates=None, job_id=None):
        """
        Export candidates to CSV
        
        Args:
            candidates: List of Candidate objects (if None, export all)
            job_id: Filter by job ID
        
        Returns:
            CSV string
        """
        if candidates is None:
            query = Candidate.query
            if job_id:
                query = query.filter_by(applied_job_id=job_id)
            candidates = query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "ID",
            "Name",
            "Email",
            "Phone",
            "Applied Job",
            "Status",
            "Match Score",
            "Resume Path",
            "Applied Date",
            "User ID"
        ])
        
        # Data rows
        for candidate in candidates:
            job_title = ""
            if candidate.applied_job_id:
                job = Job.query.get(candidate.applied_job_id)
                job_title = job.title if job else ""
            
            writer.writerow([
                candidate.id,
                candidate.name,
                candidate.email,
                candidate.phone or "",
                job_title,
                candidate.status,
                candidate.match_score or "",
                candidate.resume_path or "",
                candidate.created_at.isoformat() if candidate.created_at else "",
                candidate.user_id or ""
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_candidates_detailed_csv(candidates=None):
        """
        Export detailed candidate info (requires FAISS metadata)
        """
        if candidates is None:
            candidates = Candidate.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header with more details
        writer.writerow([
            "ID",
            "Name",
            "Email",
            "Phone",
            "Applied Job",
            "Status",
            "Match Score",
            "Experience Years",
            "Skills",
            "Applied Date",
            "Notes"
        ])
        
        # Data rows (simplified - would need FAISS metadata for full details)
        for candidate in candidates:
            job_title = ""
            if candidate.applied_job_id:
                job = Job.query.get(candidate.applied_job_id)
                job_title = job.title if job else ""
            
            writer.writerow([
                candidate.id,
                candidate.name,
                candidate.email,
                candidate.phone or "",
                job_title,
                candidate.status,
                candidate.match_score or "",
                "",  # Experience years would come from analysis
                "",  # Skills would come from analysis
                candidate.created_at.isoformat() if candidate.created_at else "",
                ""   # Notes/flags
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_jobs_csv():
        """Export all jobs to CSV"""
        from models import Job
        
        jobs = Job.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "ID",
            "Title",
            "Department",
            "Location",
            "Status",
            "Created Date",
            "Candidate Count",
            "Avg Match Score"
        ])
        
        # Data rows
        for job in jobs:
            candidates = Candidate.query.filter_by(applied_job_id=job.id).all()
            avg_score = sum(c.match_score or 0 for c in candidates) / len(candidates) if candidates else 0
            
            writer.writerow([
                job.id,
                job.title,
                job.dept or "",
                job.location or "",
                job.status,
                job.created_at.isoformat() if job.created_at else "",
                len(candidates),
                round(avg_score, 1)
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_analytics_csv(metrics):
        """
        Export analytics summary to CSV
        
        Args:
            metrics: Dict from HRAnalytics.get_dashboard_metrics()
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Metric", "Value"])
        
        # Data
        for key, value in metrics.items():
            if isinstance(value, dict):
                writer.writerow([key, ""])
                for sub_key, sub_value in value.items():
                    writer.writerow([f"  {sub_key}", sub_value])
            else:
                writer.writerow([key, value])
        
        return output.getvalue()
    
    @staticmethod
    def export_skill_demand_csv(skill_data):
        """
        Export skill demand analysis
        
        Args:
            skill_data: List of (skill, count) tuples
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Skill", "Job Postings"])
        
        # Data
        for skill, count in skill_data:
            writer.writerow([skill, count])
        
        return output.getvalue()
    
    @staticmethod
    def export_hiring_funnel_csv(funnel):
        """
        Export hiring funnel data
        
        Args:
            funnel: Dict with status -> count
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Stage", "Count", "Percentage"])
        
        # Calculate total
        total = sum(funnel.values())
        
        # Data
        for stage, count in funnel.items():
            percentage = (count / total * 100) if total > 0 else 0
            writer.writerow([stage.title(), count, f"{percentage:.1f}%"])
        
        return output.getvalue()
    
    @staticmethod
    def generate_filename(report_type):
        """Generate timestamped filename"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{report_type}_{timestamp}.csv"
