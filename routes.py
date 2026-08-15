import json
import tempfile
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Evaluation
from ..schemas import ConceptCreate, ConceptOut, AnalyzeResponse, EvaluationOut
from ..repositories import concepts
from ..services.ai import analyze
from ..services.audio import waveform
from ..services.report import make_pdf

router = APIRouter(prefix="/api")

def db_dep():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/concepts", response_model=list[ConceptOut])
def list_concepts():
    return concepts.all()

@router.post("/concepts", response_model=ConceptOut)
def add_concept(payload: ConceptCreate):
    return concepts.create(payload.title, payload.category, payload.reference_text)

@router.get("/concepts/{concept_id}", response_model=ConceptOut)
def get_concept(concept_id: int):
    item = concepts.get(concept_id)
    if not item: raise HTTPException(404, "Concept not found")
    return item

@router.post("/analyze", response_model=AnalyzeResponse)
async def run_analysis(concept_id: int = Form(...), audio: UploadFile = File(...),
                       db: Session = Depends(db_dep)):
    concept = concepts.get(concept_id)
    if not concept: raise HTTPException(404, "Concept not found")
    suffix = Path(audio.filename or ".wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await audio.read()
        tmp.write(content)
        path = tmp.name
    try:
        result = analyze(path, concept.reference_text)
        ev = Evaluation(
            concept_id=concept.id,
            concept_title=concept.title,
            transcript=result["transcript"],
            semantic_similarity=result["semantic_similarity"],
            filler_count=result["filler_count"],
            filler_ratio=result["filler_ratio"],
            pause_ratio=result["pause_ratio"],
            rms_energy=result["rms_energy"],
            duration_seconds=result["duration_seconds"],
            speaking_rate_wpm=result["speaking_rate_wpm"],
            score=result["score"],
            classification=result["classification"],
            recommendations_json=json.dumps(result["recommendations"]),
        )
        db.add(ev); db.commit(); db.refresh(ev)
        return {
            **result,
            "id": ev.id,
            "created_at": ev.created_at,
            "concept_id": ev.concept_id,
            "concept_title": ev.concept_title,
            "recommendations": result["recommendations"]
        }
    finally:
        Path(path).unlink(missing_ok=True)

@router.get("/evaluations", response_model=list[EvaluationOut])
def evaluations(limit: int = 50, db: Session = Depends(db_dep)):
    rows = db.query(Evaluation).order_by(Evaluation.created_at.desc()).limit(min(limit, 200)).all()
    return [row_out(x) for x in rows]

@router.get("/evaluations/{evaluation_id}", response_model=EvaluationOut)
def evaluation(evaluation_id: int, db: Session = Depends(db_dep)):
    item = db.get(Evaluation, evaluation_id)
    if not item: raise HTTPException(404, "Evaluation not found")
    return row_out(item)

@router.get("/evaluations/{evaluation_id}/waveform")
def evaluation_waveform(evaluation_id: int):
    # Waveforms are generated during upload sessions in the frontend.
    raise HTTPException(404, "Waveform is session-local; use the uploaded audio for a new visualization.")

@router.get("/reports/{evaluation_id}")
def report(evaluation_id: int, db: Session = Depends(db_dep)):
    item = db.get(Evaluation, evaluation_id)
    if not item: raise HTTPException(404, "Evaluation not found")
    path = make_pdf(item)
    return FileResponse(path, media_type="application/pdf", filename=path.name)

def row_out(x):
    return {
        "id": x.id, "created_at": x.created_at, "concept_id": x.concept_id,
        "concept_title": x.concept_title, "transcript": x.transcript,
        "semantic_similarity": x.semantic_similarity, "filler_count": x.filler_count,
        "filler_ratio": x.filler_ratio, "pause_ratio": x.pause_ratio,
        "rms_energy": x.rms_energy, "duration_seconds": x.duration_seconds,
        "speaking_rate_wpm": x.speaking_rate_wpm, "score": x.score,
        "classification": x.classification,
        "recommendations": json.loads(x.recommendations_json or "[]")
    }
