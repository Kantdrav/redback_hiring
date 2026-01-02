import json
from models import db, MCQQuestion, Assessment, Interview

def grade_mcq(round_id, answers: dict):
    """
    answers: { question_id (int): chosen_index (int), ... }
    Returns: { total_marks, obtained_marks, detail: {qid: {correct, marks_awarded, chosen_answer}} }
    """
    total = 0.0
    obtained = 0.0
    detail = {}
    qids = list(map(int, answers.keys()))
    qs = MCQQuestion.query.filter(MCQQuestion.id.in_(qids)).all()
    qmap = {q.id: q for q in qs}
    for qid_str, chosen in answers.items():
        qid = int(qid_str)
        q = qmap.get(qid)
        if not q:
            continue
        total += q.marks or 0.0
        correct = (int(chosen) == int(q.correct_index))
        awarded = q.marks if correct else 0.0
        obtained += awarded
        detail[qid_str] = {
            "correct": correct, 
            "marks_awarded": awarded, 
            "marks_total": q.marks,
            "chosen_answer": int(chosen),
            "correct_answer": int(q.correct_index)
        }
    return {
        "total_marks": total, 
        "obtained_marks": obtained, 
        "detail": detail,
        "answers": answers  # Store the raw answers as well
    }


