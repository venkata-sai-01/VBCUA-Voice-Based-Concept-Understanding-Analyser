import numpy as np
import librosa

def extract(path: str):
    y, sr = librosa.load(path, sr=None, mono=True)
    if len(y) == 0:
        return {"duration_seconds": 0.0, "pause_ratio": 0.0, "rms_energy": 0.0}
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    threshold = max(1e-5, float(np.percentile(rms, 25)) * 0.60)
    return {
        "duration_seconds": float(len(y) / sr),
        "pause_ratio": float(np.mean(rms < threshold)),
        "rms_energy": float(np.mean(rms)),
    }

def waveform(path: str, max_points=2500):
    y, sr = librosa.load(path, sr=None, mono=True)
    if not len(y):
        return [], []
    step = max(1, len(y) // max_points)
    yy = y[::step]
    tt = np.arange(len(yy)) * step / sr
    return tt.tolist(), yy.tolist()
