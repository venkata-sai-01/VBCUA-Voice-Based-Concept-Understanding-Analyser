import re
from collections import Counter

FILLERS = ["um", "uh", "er", "erm", "hmm", "like", "basically", "actually",
           "literally", "you know", "i mean", "sort of", "kind of"]

def analyze(text: str):
    counts = Counter()
    normalized = text.lower()
    for phrase in FILLERS:
        pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        n = len(re.findall(pattern, normalized))
        if n:
            counts[phrase] = n
    words = re.findall(r"\b[\w']+\b", normalized)
    total = sum(counts.values())
    return total, dict(counts), total / max(1, len(words))
