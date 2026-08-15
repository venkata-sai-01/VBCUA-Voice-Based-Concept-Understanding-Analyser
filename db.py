from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import get_settings

class Base(DeclarativeBase):
    pass

def make_engine():
    url = get_settings().database_url
    if url.startswith("sqlite:///"):
        Path(url.replace("sqlite:///", "", 1)).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, connect_args={"check_same_thread": False})

engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    from .models import ReferenceConcept, Evaluation
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(ReferenceConcept).count() == 0:
            db.add_all([
                ReferenceConcept(
                    title="Machine Learning",
                    category="Artificial Intelligence",
                    reference_text="Machine learning is a subset of artificial intelligence where algorithms learn patterns from data and use those patterns to make predictions or decisions without being explicitly programmed for every case."
                ),
                ReferenceConcept(
                    title="Data Mining",
                    category="Data Science",
                    reference_text="Data mining is the process of discovering useful patterns, relationships and knowledge from large datasets using statistical, database and machine learning techniques."
                ),
                ReferenceConcept(
                    title="Cloud Computing",
                    category="Cloud",
                    reference_text="Cloud computing provides on-demand access to computing resources such as servers, storage and databases over a network, usually with flexible scaling and pay-as-you-go pricing."
                )
            ])
            db.commit()
    finally:
        db.close()
