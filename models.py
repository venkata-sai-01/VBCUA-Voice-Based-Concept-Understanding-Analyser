from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class ReferenceConcept(Base):
    __tablename__ = "reference_concepts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="General")
    reference_text: Mapped[str] = mapped_column(Text, nullable=False)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    concept_id: Mapped[int] = mapped_column(Integer)
    concept_title: Mapped[str] = mapped_column(String(200))
    transcript: Mapped[str] = mapped_column(Text)
    semantic_similarity: Mapped[float] = mapped_column(Float)
    filler_count: Mapped[int] = mapped_column(Integer)
    filler_ratio: Mapped[float] = mapped_column(Float)
    pause_ratio: Mapped[float] = mapped_column(Float)
    rms_energy: Mapped[float] = mapped_column(Float)
    duration_seconds: Mapped[float] = mapped_column(Float)
    speaking_rate_wpm: Mapped[float] = mapped_column(Float)
    score: Mapped[float] = mapped_column(Float)
    classification: Mapped[str] = mapped_column(String(50))
    recommendations_json: Mapped[str] = mapped_column(Text, default="[]")
