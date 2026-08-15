from ..db import SessionLocal
from ..models import ReferenceConcept

def all():
    db = SessionLocal()
    try: return db.query(ReferenceConcept).order_by(ReferenceConcept.title).all()
    finally: db.close()

def get(cid):
    db = SessionLocal()
    try: return db.get(ReferenceConcept, cid)
    finally: db.close()

def create(title, category, reference_text):
    db = SessionLocal()
    try:
        item = ReferenceConcept(title=title, category=category, reference_text=reference_text)
        db.add(item); db.commit(); db.refresh(item)
        return item
    finally: db.close()
