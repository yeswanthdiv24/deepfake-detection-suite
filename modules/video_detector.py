"""
Video deepfake detection — samples frames uniformly and aggregates image-level predictions.
Uses image_detector internally.
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Any

from utils.logger import get_logger
from modules import image_detector

logger = get_logger("video_detector")

DEFAULT_NUM_SAMPLES = 16
DEEPFAKE_RATIO_THRESHOLD = 0.4  # If >40% of sampled frames are deepfake → video is deepfake


def analyze(video_path: str, num_samples: int = DEFAULT_NUM_SAMPLES) -> dict[str, Any]:
    """
    Detect deepfake in a video by sampling frames.

    Args:
        video_path: Path to video file.
        num_samples: Number of frames to sample evenly across the video.

    Returns:
        verdict: "Deepfake" or "Real"
        confidence: float [0, 1]
        deepfake_ratio: float — fraction of sampled frames classified as deepfake
        frame_results: list of per-frame dicts with index, verdict, confidence
        fps: float
        duration_sec: float
        total_frames: int
    """
    if not video_path or not Path(video_path).exists():
        return {"error": "Video file not found."}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Could not open video file."}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    duration_sec = total_frames / fps

    logger.info(f"Video: {total_frames} frames, {fps:.1f} fps, {duration_sec:.1f}s")

    if total_frames == 0:
        cap.release()
        return {"error": "Video has no frames or could not be read."}

    num_samples = min(num_samples, total_frames)
    sample_indices = np.linspace(0, total_frames - 1, num_samples, dtype=int)

    frame_results = []

    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret:
            logger.warning(f"Could not read frame {idx}")
            continue

        result = image_detector.analyze_frame(frame)
        if "error" in result:
            logger.warning(f"Frame {idx} analysis failed: {result['error']}")
            continue

        frame_results.append({
            "frame_index": int(idx),
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "deepfake_prob": result["scores"].get("Deepfake", 0.0),
            "face_detected": result.get("face_detected", False),
        })

    cap.release()

    if not frame_results:
        return {"error": "Could not analyze any frames from the video."}

    deepfake_frames = [r for r in frame_results if r["verdict"] == "Deepfake"]
    deepfake_ratio = len(deepfake_frames) / len(frame_results)

    if deepfake_ratio > DEEPFAKE_RATIO_THRESHOLD:
        verdict = "Deepfake"
        confidence = np.mean([r["confidence"] for r in deepfake_frames]) if deepfake_frames else 0.0
    else:
        verdict = "Real"
        real_frames = [r for r in frame_results if r["verdict"] == "Real"]
        confidence = np.mean([r["confidence"] for r in real_frames]) if real_frames else 0.0

    logger.info(f"Video verdict: {verdict} ({confidence:.2%}), deepfake_ratio={deepfake_ratio:.2%}")
    return {
        "verdict": verdict,
        "confidence": float(confidence),
        "deepfake_ratio": deepfake_ratio,
        "frame_results": frame_results,
        "fps": fps,
        "duration_sec": duration_sec,
        "total_frames": total_frames,
        "frames_analyzed": len(frame_results),
    }
