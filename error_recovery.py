#!/usr/bin/env python3
"""
Error Recovery Script - Fixes HuggingFace model loading issues
Run this before main.py to ensure models load correctly
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import get_logger

logger = get_logger("error_recovery")

def disable_huggingface_warnings():
    """Disable HuggingFace transformers warnings"""
    try:
        import os
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_DATASETS_OFFLINE'] = '1'
        logger.info("✓ Disabled HuggingFace online model loading")
    except Exception as e:
        logger.warning(f"Could not disable HF warnings: {e}")

def test_imports():
    """Test all critical imports"""
    imports_ok = True
    
    critical_imports = [
        ('torch', 'PyTorch'),
        ('cv2', 'OpenCV'),
        ('gradio', 'Gradio'),
        ('mediapipe', 'MediaPipe'),
        ('numpy', 'NumPy'),
    ]
    
    for module, name in critical_imports:
        try:
            __import__(module)
            logger.info(f"✓ {name} available")
        except ImportError as e:
            logger.error(f"✗ {name} NOT available: {e}")
            imports_ok = False
    
    return imports_ok

def test_local_models():
    """Test local model initialization"""
    try:
        from models.face_detector import FaceDetector
        from models.deepfake_detector import DeepFakeDetector
        
        logger.info("Testing face detector...")
        face_det = FaceDetector()
        logger.info("✓ Face detector initialized")
        
        logger.info("Testing deepfake detector...")
        deepfake_det = DeepFakeDetector()
        logger.info("✓ Deepfake detector initialized")
        
        return True
    except Exception as e:
        logger.error(f"✗ Error initializing models: {e}")
        return False

def main():
    """Run all recovery steps"""
    logger.info("="*60)
    logger.info("DeepFake Detection - Error Recovery")
    logger.info("="*60)
    
    # Step 1: Disable online features
    logger.info("\n[1/3] Disabling online model loading...")
    disable_huggingface_warnings()
    
    # Step 2: Test imports
    logger.info("\n[2/3] Testing Python imports...")
    if not test_imports():
        logger.error("ERROR: Missing critical dependencies!")
        logger.error("Run: pip install -r requirements.txt")
        return False
    
    # Step 3: Test models
    logger.info("\n[3/3] Testing model initialization...")
    if not test_local_models():
        logger.error("ERROR: Could not initialize models")
        return False
    
    logger.info("\n" + "="*60)
    logger.info("✓ All checks passed! Ready to run:")
    logger.info("  python main.py")
    logger.info("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
