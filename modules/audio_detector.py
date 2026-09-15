"""
Audio deepfake detection — detects synthetic/spoofed speech vs genuine speech.
Model: mo-thecreator/deepfake-audio-detection (Wav2Vec2 fine-tuned)
"""
import functools
import numpy as np
from pathlib import Path
from typing import Any

from utils.logger import get_logger

logger = get_logger("audio_detector")

MODEL_ID = "mo-thecreator/deepfake-audio-detection"
TARGET_SR = 16000
CHUNK_SEC = 30  # Process in 30-second windows for long audio


@functools.lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import pipeline
    logger.info(f"Loading audio detection model: {MODEL_ID}")
    pipe = pipeline(
        "audio-classification",
        model=MODEL_ID,
        top_k=None,
        sampling_rate=TARGET_SR,
    )
    logger.info("Audio model loaded.")
    return pipe


def _load_audio(path: str) -> tuple[np.ndarray, int]:
    """Load audio file, return (mono float32 array at TARGET_SR, sample_rate)."""
    try:
        import torchaudio
        import torchaudio.transforms as T
        waveform, sr = torchaudio.load(path)
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        if sr != TARGET_SR:
            resampler = T.Resample(orig_freq=sr, new_freq=TARGET_SR)
            waveform = resampler(waveform)
        return waveform.squeeze().numpy(), TARGET_SR
    except Exception as e:
        logger.warning(f"torchaudio failed ({e}), trying librosa.")

    import librosa
    audio, _ = librosa.load(path, sr=TARGET_SR, mono=True)
    return audio, TARGET_SR


def _normalize_labels(raw: list[dict]) -> dict[str, float]:
    scores = {}
    for item in raw:
        label = item["label"]
        score = item["score"]
        low = label.lower()
        if any(w in low for w in ("fake", "spoof", "synthetic", "deepfake", "generated", "bonafide_spoof")):
            scores["Deepfake"] = scores.get("Deepfake", 0.0) + score
        elif any(w in low for w in ("real", "genuine", "human", "bonafide", "authentic")):
            scores["Genuine"] = scores.get("Genuine", 0.0) + score
        else:
            # Fallback: label 0 = genuine, label 1 = spoof (common convention)
            if label in ("LABEL_0", "0"):
                scores["Genuine"] = scores.get("Genuine", 0.0) + score
            else:
                scores["Deepfake"] = scores.get("Deepfake", 0.0) + score
    return scores


def analyze(audio_path: str) -> dict[str, Any]:
    """
    Detect whether audio is genuine or deepfake/synthesized.

    Args:
        audio_path: Path to audio file (.wav, .mp3, .ogg, .flac, .m4a)

    Returns:
        verdict: "Deepfake" or "Genuine"
        confidence: float [0, 1]
        scores: {"Deepfake": float, "Genuine": float}
        duration_sec: float
        num_chunks: int
    """
    if not audio_path or not Path(audio_path).exists():
        return {"error": "Audio file not found."}

    try:
        audio, sr = _load_audio(audio_path)
    except Exception as e:
        logger.error(f"Failed to load audio: {e}")
        return {"error": f"Could not load audio file: {e}"}

    duration_sec = len(audio) / sr
    logger.info(f"Audio duration: {duration_sec:.1f}s, sr={sr}")

    pipe = _load_pipeline()
    chunk_samples = CHUNK_SEC * sr
    chunks = [audio[i : i + chunk_samples] for i in range(0, len(audio), chunk_samples) if len(audio[i:i+chunk_samples]) > sr // 4]

    agg_scores: dict[str, float] = {}
    successful = 0

    for i, chunk in enumerate(chunks):
        try:
            raw = pipe({"sampling_rate": sr, "raw": chunk})[0]
            chunk_scores = _normalize_labels(raw)
            for label, score in chunk_scores.items():
                agg_scores[label] = agg_scores.get(label, 0.0) + score
            successful += 1
        except Exception as e:
            logger.warning(f"Chunk {i} failed: {e}")

    if not agg_scores or successful == 0:
        return {"error": "Analysis failed on all audio chunks."}

    avg_scores = {k: v / successful for k, v in agg_scores.items()}
    avg_scores.setdefault("Deepfake", 0.0)
    avg_scores.setdefault("Genuine", 0.0)

    verdict = max(avg_scores, key=avg_scores.get)
    confidence = avg_scores[verdict]

    logger.info(f"Audio verdict: {verdict} ({confidence:.2%})")
    return {
        "verdict": verdict,
        "confidence": confidence,
        "scores": avg_scores,
        "duration_sec": duration_sec,
        "num_chunks": successful,
    }
