# PHASE 3 – Resume-RAG System (FAISS + Embeddings + LLM + Reports)

## Overview
The Resume-RAG (Retrieval-Augmented Generation) system enables intelligent resume analysis, semantic search, and job matching using embeddings and FAISS vector search.

## Components Implemented

### 1. **PDF Text Extraction (`utils_pdf.py`)**
- **Enhanced extraction**: Better formatting preservation, line cleaning
- **Section extraction**: Automatically identifies resume sections:
  - Summary/Objective
  - Professional Experience
  - Education
  - Technical Skills
  - Projects
  - Certifications
- **Error handling**: Graceful handling of malformed PDFs

### 2. **Smart Text Chunking (`rag_resume.py`)**
- **Sentence-aware chunking**: Respects sentence boundaries (no mid-sentence splits)
- **Configurable overlap**: 300-word chunks with 100-word overlap for context
- **Quality filtering**: Removes tiny/meaningless chunks

### 3. **Embedding & FAISS Indexing**
- **Model**: `all-MiniLM-L6-v2` (sentence-transformers)
  - 384-dimensional embeddings
  - Fast inference, suitable for RAG
- **Index type**: `IndexFlatIP` (inner product for normalized cosine similarity)
- **Persistence**: Index and metadata saved to `faiss_index/` directory
- **Per-candidate tracking**: Metadata includes:
  - `candidate_id`: Links chunks to candidate
  - `section`: Resume section (skills, experience, etc.)
  - `indexed_at`: Timestamp

### 4. **Semantic Search Function**
```python
semantic_search(query, candidate_id=None, top_k=10)
```
- Searches FAISS index for relevant resume chunks
- Optional filtering by candidate
- Returns top-k results with similarity scores and section info
- Used for job-resume matching

### 5. **Intelligent Report Generation**

#### A. Skills Extraction
- Detects 50+ technical keywords (Python, AWS, Docker, etc.)
- Case-insensitive matching across resume text
- Returns as badges in UI

#### B. Experience Calculation
- Regex pattern matching for year ranges (2020-2023, etc.)
- Computes years from earliest to latest year mentioned
- Flags early-career candidates

#### C. Match Scoring (0-100)
- **Base score**: 50 points
- **Dynamic scoring**:
  - Semantic matching against job description (+10 per relevant chunk)
  - Skill overlap analysis
  - Capped at 100%

#### D. Recommended Interview Questions
- Generated based on detected skills
- Role-specific questions for senior positions
- Examples:
  - "Describe a complex Python project..."
  - "Walk us through your cloud architecture..."
  - "How have you used Kubernetes in production?"

#### E. Flags & Notes
- Early-career detection
- Skill gaps relative to job
- Missing key technical keywords
- Experience verification prompts

### 6. **Resume Report Template (`templates/resumes/view_report.html`)**
Comprehensive visualization with:
- **Candidate Info**: Name, email, phone, applied position
- **Match Score**: Visual progress bar with percentage
- **Summary**: First resume section excerpt
- **Skills**: Badges showing all detected technical skills
- **Experience**: Years of experience calculation
- **Interview Questions**: Role-appropriate questions
- **Flags & Notes**: HR review items
- **Resume Snippets**: Expandable accordion of indexed chunks

## Workflow

```
User uploads PDF resume
         ↓
Extract text + parse sections
         ↓
Create intelligent chunks (300 words, 100-word overlap)
         ↓
Generate embeddings (all-MiniLM-L6-v2)
         ↓
Add to FAISS index + save metadata
         ↓
Extract skills, experience, years
         ↓
Semantic search against job description (if provided)
         ↓
Calculate match score & generate questions
         ↓
Create flags/notes
         ↓
Display comprehensive report
```

## Key Features

### ✅ **Job-Resume Matching**
- Resume semantic search against job description
- Match score reflects relevance
- Skill gap identification
- Role-appropriate interview questions

### ✅ **Error Handling**
- PDF extraction failures caught and reported
- Indexing errors don't break upload flow
- User-friendly error messages

### ✅ **Scalability**
- FAISS handles thousands of resume chunks efficiently
- Metadata JSON allows offline analysis
- Per-candidate indexing enables multi-tenant scenarios

### ✅ **Privacy**
- All processing done locally (no API calls)
- FAISS index persisted locally
- No external LLM dependencies

## Configuration

**File paths:**
```
/faiss_index/
  ├── faiss.index          # FAISS vector index
  └── metadata.json        # Chunk metadata
/uploads/resumes/          # Uploaded PDF files
```

**Hyperparameters:**
```python
CHUNK_SIZE = 300           # words per chunk
CHUNK_OVERLAP = 100        # word overlap between chunks
TOP_K_SEARCH = 10          # search results
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

## Future Enhancements

1. **LLM Integration**: Hook to OpenAI/Claude for more sophisticated analysis
2. **Async Indexing**: Background task queue for large-scale resume processing
3. **Resume Scoring**: ML model for predicting interview success
4. **Multi-language Support**: Handle resumes in multiple languages
5. **Resume Parsing**: Extract structured data (work history, education)
6. **Batch Analysis**: Process multiple resumes with comparison views

## Testing the System

1. **Login**: Use admin token or regular account
2. **Upload Resume**: Go to `/rag/upload_resume`
3. **Fill in Details**: Name, email, phone (optional), job selection
4. **Select Job** (optional): For job-specific matching
5. **View Report**: Automatic redirect to analysis
6. **Review Results**: Skills, experience, match score, questions

## Example Report Output

```json
{
  "summary": "Senior software engineer with experience in...",
  "skills": ["Python", "AWS", "Docker", "Kubernetes", "PostgreSQL"],
  "experience_years": 7,
  "match_score": 85,
  "recommended_questions": [
    "Describe your experience with Kubernetes...",
    "How do you approach system design..."
  ],
  "flags": [],
  "snippets": ["Full resume section previews..."]
}
```

---

**Status**: ✅ Phase 3 Complete
**Version**: 1.0
**Last Updated**: December 12, 2025
