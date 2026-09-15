"""
DeepFake Detection Suite
========================
Usage:
    python main.py

Opens a Gradio web UI at http://localhost:7860
Supports deepfake detection in: Image, Video, Audio, and Text.

Note: Uses a custom CNN model. For best accuracy, train on deepfake datasets.
"""
import sys
import os

# Disable HuggingFace online features to prevent model loading errors
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_DATASETS_OFFLINE'] = '1'

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from ui.app import build_app
from utils.logger import get_logger

logger = get_logger("main")


if __name__ == "__main__":
    logger.info("Starting DeepFake Detection Suite...")
    logger.info("Loading models...")
    
    try:
        demo = build_app()
        logger.info("✓ Models loaded successfully")
        
        logger.info("\n" + "="*60)
        logger.info("🎬 DeepFake Detection Suite Ready!")
        logger.info("="*60)
        logger.info("\nOpening web interface at http://localhost:7860")
        logger.info("Press Ctrl+C to stop the server")
        logger.info("="*60 + "\n")
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True,
        )
    
    except Exception as e:
        logger.error(f"✗ Error starting application: {e}")
        logger.error("\nTroubleshooting steps:")
        logger.error("1. Run: python error_recovery.py")
        logger.error("2. Check: python verify.py")
        logger.error("3. Reinstall: pip install -r requirements.txt")
        sys.exit(1)
