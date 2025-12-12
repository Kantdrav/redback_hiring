"""
HR Analytics Service - Provides metrics, filtering, and reporting for HR dashboards
"""
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from models import db, Candidate, Job, User, Interview
from collections import defaultdict, Counter


class HRAnalytics:
    """Comprehensive analytics for HR dashboards"""
    
    @staticmethod
    def get_dashboard_metrics():
        """Get high-level dashboard metrics"""
        total_candidates = Candidate.query.count()
        total_jobs = Job.query.count()
        open_jobs = Job.query.filter_by(status="open").count()
        applied_count = Candidate.query.filter_by(status="applied").count()
        
        # Average match score
        avg_match_score = db.session.query(
            func.avg(func.cast(Candidate.match_score, db.Float))
        ).scalar() or 0
        
        # Candidates by status
        status_dist = db.session.query(
            Candidate.status,
            func.count(Candidate.id)
        ).group_by(Candidate.status).all()
        
        # Last 7 days applications
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_apps = Candidate.query.filter(
            Candidate.created_at >= week_ago
        ).count()
        
        return {
            "total_candidates": total_candidates,
            "total_jobs": total_jobs,
            "open_jobs": open_jobs,
            "applied_candidates": applied_count,
            "avg_match_score": round(float(avg_match_score), 1),
            "recent_applications_7d": recent_apps,
            "candidate_status_distribution": dict(status_dist) if status_dist else {}
        }
    
    @staticmethod
    def get_candidates_with_filters(
        job_id=None,
        status=None,
        min_match_score=None,
        skill=None,
        search_query=None,
        page=1,
        per_page=20
    ):
        """
        Get filtered candidate list with pagination
        
        Args:
            job_id: Filter by job ID
            status: Filter by application status
            min_match_score: Minimum match score (0-100)
            skill: Filter by technical skill
            search_query: Search by name or email
            page: Page number (1-indexed)
            per_page: Results per page
        
        Returns:
            dict with candidates, total count, pagination info
        """
        query = Candidate.query
        
        # Apply filters
        if job_id:
            query = query.filter_by(applied_job_id=job_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if search_query:
            query = query.filter(
                db.or_(
                    Candidate.name.ilike(f"%{search_query}%"),
                    Candidate.email.ilike(f"%{search_query}%")
                )
            )
        
        if min_match_score is not None:
            query = query.filter(Candidate.match_score >= min_match_score)
        
        # TODO: Implement skill filtering when skill metadata is accessible
        # This would require parsing the FAISS metadata or adding a skills column
        
        total = query.count()
        candidates = query.order_by(
            Candidate.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            "candidates": candidates.items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": candidates.pages,
            "has_next": candidates.has_next,
            "has_prev": candidates.has_prev
        }
    
    @staticmethod
    def get_skill_demand_analysis():
        """Analyze which skills are most in-demand across all jobs"""
        jobs = Job.query.all()
        skill_counter = Counter()
        
        # Common tech keywords
        tech_keywords = {
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "go", "rust",
            "sql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "react", "vue", "angular", "node", "django", "flask", "spring",
            "rest", "graphql", "api", "microservices", "ci/cd", "git",
            "html", "css", "typescript", "scala", "kotlin", "swift",
            "machine learning", "ai", "nlp", "tensorflow", "pytorch"
        }
        
        for job in jobs:
            description = (job.description or "").lower()
            title = (job.title or "").lower()
            search_text = description + " " + title
            
            for keyword in tech_keywords:
                if keyword in search_text:
                    skill_counter[keyword.title()] += 1
        
        # Return top 15 skills
        return sorted(
            skill_counter.items(),
            key=lambda x: x[1],
            reverse=True
        )[:15]
    
    @staticmethod
    def get_experience_distribution():
        """Analyze candidate experience distribution"""
        candidates = Candidate.query.all()
        experience_buckets = {
            "0-2 years": 0,
            "2-5 years": 0,
            "5-10 years": 0,
            "10+ years": 0,
            "Unknown": 0
        }
        
        # This is simplified - in reality, you'd extract from FAISS metadata
        # For now, we use a heuristic based on candidate count
        for candidate in candidates:
            # Placeholder: randomly assign (in production, extract from resume analysis)
            experience_buckets["Unknown"] += 1
        
        return experience_buckets
    
    @staticmethod
    def get_match_score_distribution():
        """Analyze match score distribution"""
        candidates = Candidate.query.all()
        score_buckets = {
            "90-100": 0,
            "80-89": 0,
            "70-79": 0,
            "60-69": 0,
            "Below 60": 0
        }
        
        for candidate in candidates:
            score = candidate.match_score or 0
            if score >= 90:
                score_buckets["90-100"] += 1
            elif score >= 80:
                score_buckets["80-89"] += 1
            elif score >= 70:
                score_buckets["70-79"] += 1
            elif score >= 60:
                score_buckets["60-69"] += 1
            else:
                score_buckets["Below 60"] += 1
        
        return score_buckets
    
    @staticmethod
    def get_hiring_funnel():
        """Get hiring pipeline stats"""
        statuses = ["applied", "screening", "interview", "offer", "hired", "rejected"]
        funnel = {}
        
        for status in statuses:
            count = Candidate.query.filter_by(status=status).count()
            funnel[status] = count
        
        return funnel
    
    @staticmethod
    def get_job_candidate_summary():
        """Get summary of candidates per job"""
        jobs = Job.query.all()
        summary = []
        
        for job in jobs:
            candidates = Candidate.query.filter_by(applied_job_id=job.id).all()
            avg_score = sum(c.match_score or 0 for c in candidates) / len(candidates) if candidates else 0
            
            summary.append({
                "job_id": job.id,
                "job_title": job.title,
                "total_candidates": len(candidates),
                "avg_match_score": round(avg_score, 1),
                "by_status": self._count_by_status(candidates)
            })
        
        return summary
    
    @staticmethod
    def _count_by_status(candidates):
        """Helper to count candidates by status"""
        counter = Counter(c.status for c in candidates)
        return dict(counter)
    
    @staticmethod
    def get_top_candidates(job_id=None, limit=10):
        """Get top candidates by match score"""
        query = Candidate.query.order_by(Candidate.match_score.desc())
        
        if job_id:
            query = query.filter_by(applied_job_id=job_id)
        
        return query.limit(limit).all()
    
    @staticmethod
    def get_recent_activity(days=7):
        """Get recently uploaded resumes"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = Candidate.query.filter(
            Candidate.created_at >= cutoff
        ).order_by(Candidate.created_at.desc()).limit(20).all()
        
        return recent
