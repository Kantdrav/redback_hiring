import os
import json
import re
from flask import Blueprint, request, current_app, jsonify, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from models import db, Candidate, Job
from utils_pdf import extract_pdf_text, extract_sections
from datetime import datetime
from pathlib import Path
from flask_login import login_required, current_user

rag_bp = Blueprint("rag", __name__, template_folder="templates/resumes")

# Global small in-process index for demo. For production, persist index files and metadata.
BASE = Path(__file__).parent
VEC_DIR = BASE / "faiss_index"
VEC_DIR.mkdir(exist_ok=True)
META_FILE = VEC_DIR / "metadata.json"
INDEX_FILE = VEC_DIR / "faiss.index"

# Lazy-load heavy ML models to reduce memory at startup
EMBED_MODEL = None
FAISS_INDEX = None
METADATA = None

def get_embed_model():
    """Lazy-load embedding model on first use"""
    global EMBED_MODEL
    if EMBED_MODEL is None:
        from sentence_transformers import SentenceTransformer
        EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return EMBED_MODEL

def load_metadata():
    """Lazy-load metadata and index on first use"""
    global METADATA, FAISS_INDEX
    if METADATA is None:
        if META_FILE.exists():
            with open(META_FILE, "r", encoding="utf-8") as f:
                METADATA = json.load(f)
        else:
            METADATA = []
    if FAISS_INDEX is None and INDEX_FILE.exists():
        import faiss
        FAISS_INDEX = faiss.read_index(str(INDEX_FILE))
    return METADATA, FAISS_INDEX

def save_index_and_meta():
    if index is not None:
        faiss.write_index(index, str(INDEX_FILE))
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(METADATA, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

@rag_bp.route("/upload_resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    jobs = Job.query.filter_by(status="open").all() if Job else []
    
    if request.method == "POST":
        # candidate fields
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        job_id = request.form.get("job_id", None)

        # Validation
        if not name:
            flash("Name is required", "danger")
            return redirect(request.url)
        if not email:
            flash("Email is required", "danger")
            return redirect(request.url)

        file = request.files.get("resume")
        if not file or file.filename == "":
            flash("No file uploaded", "danger")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Only pdf allowed", "danger")
            return redirect(request.url)

        filename = secure_filename(f"{int(datetime.utcnow().timestamp())}_{file.filename}")
        save_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
        file.save(save_path)

        # store candidate with current user ID
        c = Candidate(user_id=current_user.id, name=name, email=email, phone=phone, resume_path=str(save_path), applied_job_id=job_id if job_id else None)
        db.session.add(c)
        db.session.commit()

        # index resume asynchronously ideally; demo: immediate
        try:
            index_resume_candidate(c.id, str(save_path))
            flash("Resume uploaded & indexed", "success")
        except Exception as e:
            flash(f"Resume uploaded but indexing failed: {str(e)}", "warning")

        return redirect(url_for("rag.view_report", candidate_id=c.id))
    
    return render_template("resumes/upload.html", jobs=jobs)

def chunk_text(text, chunk_size=300, overlap=100):
    """
    Smart text chunking that respects sentence boundaries
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_len = len(sentence.split())
        if current_length + sentence_len > chunk_size and current_chunk:
            # Save current chunk
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)
            # Start new chunk with overlap
            overlap_sentences = []
            sent_count = 0
            for sent in reversed(current_chunk):
                if sent_count * 15 < overlap:  # approximate words
                    overlap_sentences.insert(0, sent)
                    sent_count += len(sent.split())
                else:
                    break
            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s.split()) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_length += sentence_len
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return [c for c in chunks if len(c.strip()) > 20]  # filter out tiny chunks

def index_resume_candidate(candidate_id: int, file_path: str):
    global index, METADATA
    try:
        text = extract_pdf_text(file_path)
        if not text:
            raise ValueError("Could not extract text from PDF")
        
        sections = extract_sections(text)
        chunks = []
        chunk_sections = []
        
        # Chunk each section separately to maintain context
        for section_name, section_text in sections.items():
            if section_text.strip():
                section_chunks = chunk_text(section_text, chunk_size=300, overlap=100)
                chunks.extend(section_chunks)
                chunk_sections.extend([section_name] * len(section_chunks))
        
        if not chunks:
            raise ValueError("Could not create chunks from resume text")
        
        embed_model = get_embed_model()
        embeddings = embed_model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)
        d = embeddings.shape[1]
        if index is None:
            import faiss
            index = faiss.IndexFlatIP(d)
        
        # normalize for cosine similarity
        import faiss
        faiss.normalize_L2(embeddings)
        index.add(embeddings)

        # add metadata entries
        metadata, _ = load_metadata()
        start_idx = len(metadata)
        for i, (chunk, section) in enumerate(zip(chunks, chunk_sections)):
            metadata.append({
                "candidate_id": candidate_id,
                "chunk_id": f"{candidate_id}_{i+start_idx}",
                "text": chunk[:3000],
                "section": section,
                "indexed_at": datetime.utcnow().isoformat()
            })
        save_index_and_meta()
        print(f"✓ Indexed {len(chunks)} chunks for candidate {candidate_id}")
    except Exception as e:
        print(f"Error indexing resume: {e}")
        raise

@rag_bp.route("/resume/<int:candidate_id>/report", methods=["GET"])
@login_required
def view_report(candidate_id):
    cand = Candidate.query.get_or_404(candidate_id)
    job = Job.query.get(cand.applied_job_id) if cand.applied_job_id else None
    report = generate_resume_report(candidate_id, job)
    
    # Save match score to candidate record
    cand.match_score = report.get("match_score", 0)
    db.session.commit()
    
    return render_template("resumes/view_report.html", candidate=cand, job=job, report=report)

@rag_bp.route("/resume/<int:candidate_id>/download", methods=["GET"])
@login_required
def download_resume(candidate_id):
    cand = Candidate.query.get_or_404(candidate_id)
    # Authorization: allow owner candidate or admin/hr roles
    user_role = getattr(current_user, "role", None)
    if not (user_role in ["admin", "hr"] or cand.user_id == current_user.id):
        flash("You don't have permission to download this resume", "danger")
        return redirect(url_for("rag.view_report", candidate_id=candidate_id))

    resume_path = cand.resume_path
    if not resume_path or not os.path.exists(resume_path):
        flash("Resume file not found", "warning")
        return redirect(url_for("rag.view_report", candidate_id=candidate_id))

    return send_file(
        resume_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=os.path.basename(resume_path)
    )

def semantic_search(query, candidate_id=None, top_k=10):
    """
    Search FAISS index for relevant chunks
    Optionally filter by candidate_id
    """
    metadata, faiss_index = load_metadata()
    if faiss_index is None or len(metadata) == 0:
        return []
    
    try:
        embed_model = get_embed_model()
        emb = embed_model.encode([query], convert_to_numpy=True)
        import faiss
        faiss.normalize_L2(emb)
        D, I = faiss_index.search(emb, min(top_k * 2, len(metadata)))  # search more, then filter
        
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(metadata):
                continue
            meta = metadata[idx]
            if candidate_id and meta["candidate_id"] != candidate_id:
                continue
            results.append({
                "score": float(score),
                "text": meta["text"],
                "section": meta.get("section", "unknown"),
                "candidate_id": meta["candidate_id"]
            })
        return results[:top_k]
    except Exception as e:
        print(f"Search error: {e}")
        return []

TECH_KEYWORDS = {
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "go", "rust",
    "sql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "react", "vue", "angular", "node", "django", "flask", "spring",
    "rest", "graphql", "api", "microservices", "ci/cd", "git",
    "html", "css", "typescript", "scala", "kotlin", "swift",
    "machine learning", "ai", "nlp", "tensorflow", "pytorch"
}

def extract_skills_from_text(text):
    """Extract technical skills from resume text"""
    text_lower = text.lower()
    found_skills = set()
    for keyword in TECH_KEYWORDS:
        if keyword in text_lower:
            found_skills.add(keyword.title())
    return sorted(list(found_skills))

def extract_experience_years(text):
    """Extract years of experience from resume text"""
    # Look for patterns like "2020-2023", "2020 – 2023", "2020 - 2023"
    year_pattern = r"(?:19|20)\d{2}"
    years = re.findall(year_pattern, text)
    if years:
        try:
            year_nums = [int(y) for y in years]
            if year_nums:
                return max(year_nums) - min(year_nums)
        except:
            pass
    return 0

def generate_resume_report(candidate_id, job=None):
    """
    Generate comprehensive resume analysis report
    """
    try:
        # Gather all chunks for this candidate
        candidate_chunks = [meta for meta in METADATA if meta["candidate_id"] == candidate_id]
        
        if not candidate_chunks:
            return {
                "summary": "No resume indexed yet.",
                "skills": [],
                "experience_years": 0,
                "match_score": 0,
                "recommended_questions": [],
                "flags": ["Resume has not been indexed yet"],
                "snippets": []
            }
        
        # Combine text from all sections
        full_text = "\n\n".join([meta["text"] for meta in candidate_chunks])
        
        # Extract skills
        found_skills = extract_skills_from_text(full_text)
        
        # Extract experience
        exp_years = extract_experience_years(full_text)
        
        # Calculate match score based on job description
        match_score = 50  # base score
        if job and job.description:
            job_query = job.title + " " + job.description[:500]
            job_results = semantic_search(job_query, candidate_id=candidate_id, top_k=5)
            match_score = min(100, int(50 + len(job_results) * 10))
        
        # Find recommended interview questions
        recommended_questions = []
        if "python" in [s.lower() for s in found_skills]:
            recommended_questions.append("Describe a complex Python project you've built. What were the key technical challenges?")
        if "aws" in [s.lower() for s in found_skills] or "azure" in [s.lower() for s in found_skills]:
            recommended_questions.append("Walk us through your experience with cloud architecture and deployment pipelines.")
        if "kubernetes" in [s.lower() for s in found_skills]:
            recommended_questions.append("How have you used Kubernetes in production? What scaling challenges did you face?")
        if job and "senior" in job.title.lower() and exp_years < 5:
            recommended_questions.append(f"You're applying for a senior role. Can you elaborate on your leadership and mentoring experience?")
        
        # Flag potential issues
        flags = []
        if exp_years == 0:
            flags.append("Could not determine years of experience from resume.")
        elif exp_years < 2:
            flags.append(f"Candidate appears to have ~{exp_years} years of experience (early career).")
        
        if len(found_skills) < 3:
            flags.append("Resume has minimal technical skills listed. Request more details.")
        
        if job:
            job_skills = extract_skills_from_text(job.description or "")
            missing_skills = set(job_skills) - set([s.lower() for s in found_skills])
            if missing_skills:
                flags.append(f"Missing skills for this role: {', '.join(list(missing_skills)[:3])}")
        
        # Get summary from first chunk
        summary_chunk = candidate_chunks[0]["text"] if candidate_chunks else ""
        summary = (summary_chunk[:300] + "...") if summary_chunk else "Resume indexed successfully."
        
        return {
            "summary": summary,
            "skills": found_skills,
            "experience_years": exp_years,
            "match_score": match_score,
            "recommended_questions": recommended_questions[:5],
            "flags": flags[:5],
            "snippets": [meta["text"][:500] for meta in candidate_chunks[:3]]
        }
    except Exception as e:
        print(f"Error generating report: {e}")
        return {
            "summary": f"Error generating report: {str(e)}",
            "skills": [],
            "experience_years": 0,
            "match_score": 0,
            "recommended_questions": [],
            "flags": [str(e)],
            "snippets": []
        }

