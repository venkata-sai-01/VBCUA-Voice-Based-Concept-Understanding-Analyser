from functools import lru_cache
import whisper
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from . import audio as audio_service
from .filler import analyze as filler_analyze
from ..config import get_settings

@lru_cache(maxsize=1)
def whisper_model():
    return whisper.load_model(get_settings().whisper_model)

@lru_cache(maxsize=1)
def embedding_model():
    return SentenceTransformer(get_settings().embedding_model)

def transcribe(path: str):
    return whisper_model().transcribe(path, fp16=False).get("text", "").strip()

def similarity(reference: str, response: str):
    model = embedding_model()
    v = model.encode([reference, response], normalize_embeddings=True)
    return float(max(0.0, min(1.0, cosine_similarity([v[0]], [v[1]])[0][0])))

def analyze(path: str, reference: str):
    transcript = transcribe(path)
    semantic = similarity(reference, transcript)
    filler_count, filler_counts, filler_ratio = filler_analyze(transcript)
    af = audio_service.extract(path)
    words = max(1, len(transcript.split()))
    wpm = words / max(af["duration_seconds"] / 60, 1e-6)

    semantic_part = semantic * 70
    filler_quality = max(0, 1 - min(1, filler_ratio / 0.08)) * 10
    pause_quality = max(0, 1 - min(1, max(0, af["pause_ratio"] - 0.25) / 0.50)) * 10
    energy_quality = min(1, max(0, af["rms_energy"] / 0.12)) * 10
    score = round(max(0, min(100, semantic_part + filler_quality + pause_quality + energy_quality)), 2)

    if score >= 85: classification = "Excellent"
    elif score >= 70: classification = "Good"
    elif score >= 50: classification = "Needs Improvement"
    else: classification = "Poor"

    tips = []
    if semantic < .60: tips.append("Review the core definition and include the main concept keywords.")
    elif semantic < .75: tips.append("Add important details or a practical example.")
    else: tips.append("Strong conceptual coverage. Keep the explanation structured.")
    if filler_ratio > .05: tips.append("Reduce filler words by replacing them with short silent pauses.")
    if af["pause_ratio"] > .55: tips.append("Practice smoother transitions and reduce unusually long pauses.")
    if af["rms_energy"] < .015: tips.append("Speak more clearly and consistently for a stronger audio signal.")

    return {
        "transcript": transcript,
        "semantic_similarity": semantic,
        "filler_count": filler_count,
        "filler_counts": filler_counts,
        "filler_ratio": filler_ratio,
        **af,
        "speaking_rate_wpm": wpm,
        "score": score,
        "classification": classification,
        "recommendations": tips
    }
