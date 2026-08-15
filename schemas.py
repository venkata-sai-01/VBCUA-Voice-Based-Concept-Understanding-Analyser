from datetime import datetime
from pydantic import BaseModel, Field

class ConceptCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    category: str = Field(default="General", max_length=100)
    reference_text: str = Field(min_length=10)

class ConceptOut(ConceptCreate):
    id: int
    class Config:
        from_attributes = True

class EvaluationOut(BaseModel):
    id: int
    created_at: datetime
    concept_id: int
    concept_title: str
    transcript: str
    semantic_similarity: float
    filler_count: int
    filler_ratio: float
    pause_ratio: float
    rms_energy: float
    duration_seconds: float
    speaking_rate_wpm: float
    score: float
    classification: str
    recommendations: list[str]

class AnalyzeResponse(EvaluationOut):
    filler_counts: dict[str, int]
