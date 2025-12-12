import re
from PyPDF2 import PdfReader

def extract_pdf_text(path):
    """Extract text from PDF with better formatting preservation"""
    try:
        reader = PdfReader(path)
        pages = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            # Clean up extra whitespace while preserving structure
            lines = text.split('\n')
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            pages.append('\n'.join(cleaned_lines))
        return "\n\n".join(pages)
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_sections(text):
    """Extract common resume sections"""
    sections = {
        "summary": "",
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "certifications": "",
        "other": ""
    }
    
    # Pattern matching for common section headers
    patterns = {
        "summary": r"(summary|objective|profile|about)",
        "experience": r"(professional experience|experience|work history|employment)",
        "education": r"(education|academic|degree)",
        "skills": r"(skills|technical skills|competencies)",
        "projects": r"(projects|portfolio|work samples)",
        "certifications": r"(certifications?|licenses?|awards?)"
    }
    
    lines = text.split('\n')
    current_section = "other"
    
    for line in lines:
        lower_line = line.lower()
        for section, pattern in patterns.items():
            if re.search(pattern, lower_line):
                current_section = section
                break
        sections[current_section] += line + "\n"
    
    return sections

