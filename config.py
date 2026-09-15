"""
Configuration and constants for DeepFake Detection Suite
"""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Model paths
MODELS_DIR = PROJECT_ROOT / "models" / "pretrained"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Detection thresholds
FACE_DETECTION_CONFIDENCE = 0.5
DEEPFAKE_THRESHOLD = 0.5  # Score above this is considered deepfake

# Image processing
IMAGE_SIZE = 256
BATCH_SIZE = 4

# Video processing
MAX_VIDEO_FRAMES = 1000
VIDEO_FRAME_SAMPLE_RATE = 1  # Process every nth frame

# UI settings
UI_PORT = 7860
UI_HOST = "0.0.0.0"

# Logging
LOG_LEVEL = "INFO"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Device settings
DEVICE = "cuda"  # or "cpu"

# Model settings
MODEL_CHECKPOINT = MODELS_DIR / "deepfake_detector.pth"
