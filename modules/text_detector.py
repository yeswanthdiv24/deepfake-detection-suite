"""
Text deepfake detection — identifies AI-generated text vs human-written text.
Model: Hello-SimpleAI/chatgpt-detector-roberta (RoBERTa fine-tuned)
"""
import functools
from typing import Any

from utils.logger import get_logger

logger = get_logger("text_detector")

MODEL_ID = "Hello-SimpleAI/chatgpt-detector-roberta"
MAX_TOKENS = 512
CHUNK_OVERLAP = 50


@functools.lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import pipeline
    logger.info(f"Loading text detection model: {MODEL_ID}")
    pipe = pipeline(
        "text-classification",
        model=MODEL_ID,
        top_k=None,
        truncation=True,
        max_length=MAX_TOKENS,
    )
    logger.info("Text model loaded.")
    return pipe


def _chunk_text(text: str, chunk_size: int = 400, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping word-level chunks."""
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def analyze(text: str) -> dict[str, Any]:
    """
    Detect whether text is AI-generated or human-written.

    Returns:
        verdict: "AI-Generated" or "Human-Written"
        confidence: float [0, 1]
        scores: {"AI-Generated": float, "Human-Written": float}
        chunk_results: list of per-chunk verdicts (for long text)
    """
    if not text or not text.strip():
        return {"error": "No text provided."}

    pipe = _load_pipeline()
    words = text.split()

    if len(words) <= 400:
        chunks = [text.strip()]
    else:
        chunks = _chunk_text(text)

    logger.info(f"Analyzing {len(chunks)} chunk(s) of text.")

    # Accumulate scores across chunks
    agg_scores: dict[str, float] = {}
    chunk_results = []

    for i, chunk in enumerate(chunks):
        try:
            raw = pipe(chunk)[0]  # list of {"label": ..., "score": ...}
        except Exception as e:
            logger.warning(f"Chunk {i} failed: {e}")
            continue

        chunk_scores = {}
        for item in raw:
            label = item["label"]
            score = item["score"]
            # Normalize label names
            if label.lower() in ("fake", "chatgpt", "ai", "machine"):
                label = "AI-Generated"
            elif label.lower() in ("real", "human", "humans"):
                label = "Human-Written"
            chunk_scores[label] = score

        for label, score in chunk_scores.items():
            agg_scores[label] = agg_scores.get(label, 0.0) + score

        chunk_verdict = max(chunk_scores, key=chunk_scores.get)
        chunk_results.append({
            "chunk": i + 1,
            "verdict": chunk_verdict,
            "confidence": chunk_scores.get(chunk_verdict, 0.0),
        })

    if not agg_scores:
        return {"error": "Analysis failed on all chunks."}

    # Average across chunks
    n = len(chunk_results)
    avg_scores = {k: v / n for k, v in agg_scores.items()}

    verdict = max(avg_scores, key=avg_scores.get)
    confidence = avg_scores[verdict]

    logger.info(f"Text verdict: {verdict} ({confidence:.2%})")
    return {
        "verdict": verdict,
        "confidence": confidence,
        "scores": avg_scores,
        "chunk_results": chunk_results,
        "num_words": len(words),
    }
