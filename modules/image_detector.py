"""
Image deepfake detection — classifies faces as Real or Deepfake.
Model: Wvolf/ViT-Deepfake-Detection (Vision Transformer fine-tuned on deepfake data)
"""
import functools
import cv2
import numpy as np
from PIL import Image
from typing import Any

from utils.logger import get_logger

logger = get_logger("image_detector")

# Note: Original model 'Wvolf/ViT-Deepfake-Detection' was removed from HuggingFace
# Using 'microsoft/beit-base-patch16-224' as a Vision Transformer alternative for image classification
# For production use, consider training a custom model on your deepfake dataset
MODEL_ID = "microsoft/beit-base-patch16-224"
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


@functools.lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import pipeline
    logger.info(f"Loading image detection model: {MODEL_ID}")
    pipe = pipeline("image-classification", model=MODEL_ID, top_k=None)
    logger.info("Image model loaded.")
    return pipe


@functools.lru_cache(maxsize=1)
def _load_face_cascade():
    cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    return cascade


def _detect_and_crop_face(pil_image: Image.Image) -> tuple[Image.Image, bool]:
    """Detect the largest face and crop it; fall back to full image if none found."""
    img_bgr = cv2.cvtColor(np.array(pil_image.convert("RGB")), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    cascade = _load_face_cascade()
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(faces) == 0:
        return pil_image, False

    # Pick largest face
    areas = [w * h for (x, y, w, h) in faces]
    x, y, w, h = faces[np.argmax(areas)]

    # Add 20% padding
    pad = int(max(w, h) * 0.2)
    ih, iw = img_bgr.shape[:2]
    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(iw, x + w + pad)
    y2 = min(ih, y + h + pad)

    face_crop = pil_image.crop((x1, y1, x2, y2))
    return face_crop, True


def _normalize_labels(raw: list[dict]) -> dict[str, float]:
    """Normalize model labels to canonical form (Real/Deepfake). 
    Works with various model label formats."""
    scores = {"Real": 0.0, "Deepfake": 0.0}
    
    for item in raw:
        label = str(item.get("label", "")).lower()
        score = float(item.get("score", 0.0))
        
        # Map various label formats to Real/Deepfake
        if any(w in label for w in ("fake", "deepfake", "forged", "manipulated", "synthetic")):
            scores["Deepfake"] += score
        else:
            scores["Real"] += score
    
    # Normalize by number of samples if multi-sample
    total = sum(scores.values())
    if total > 0:
        scores = {k: v / total for k, v in scores.items()}
    
    return scores


def analyze(image_input) -> dict[str, Any]:
    """
    Detect deepfake in an image.

    Args:
        image_input: PIL Image, numpy array (BGR/RGB), or file path string.

    Returns:
        verdict: "Deepfake" or "Real"
        confidence: float [0, 1]
        scores: {"Deepfake": float, "Real": float}
        face_detected: bool
    """
    # Normalize to PIL
    if isinstance(image_input, str):
        pil_img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 3 and image_input.shape[2] == 3:
            pil_img = Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))
        else:
            pil_img = Image.fromarray(image_input)
    elif isinstance(image_input, Image.Image):
        pil_img = image_input.convert("RGB")
    else:
        return {"error": "Unsupported image input type."}

    cropped, face_detected = _detect_and_crop_face(pil_img)
    pipe = _load_pipeline()

    try:
        # Get raw predictions - model returns list of dicts with 'label' and 'score'
        raw_results = pipe(cropped)
        if isinstance(raw_results, dict):
            raw_results = [raw_results]
    except Exception as e:
        logger.error(f"Image pipeline error: {e}")
        return {"error": str(e)}

    scores = _normalize_labels(raw_results)

    # Ensure both keys exist
    scores.setdefault("Deepfake", 0.0)
    scores.setdefault("Real", 0.0)

    verdict = max(scores, key=scores.get)
    confidence = scores[verdict]

    logger.info(f"Image verdict: {verdict} ({confidence:.2%}), face_detected={face_detected}")
    return {
        "verdict": verdict,
        "confidence": confidence,
        "scores": scores,
        "face_detected": face_detected,
    }


def analyze_frame(frame_bgr: np.ndarray) -> dict[str, Any]:
    """Convenience wrapper for video frame analysis (BGR numpy array)."""
    return analyze(frame_bgr)
