from backend.app.services.filler import analyze

def test_filler():
    total, counts, ratio = analyze("Um this is like a test, you know.")
    assert total == 3
    assert counts["um"] == 1
    assert counts["like"] == 1
    assert counts["you know"] == 1
