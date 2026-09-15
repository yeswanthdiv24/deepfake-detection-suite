#!/usr/bin/env python3
"""
Verification script for DeepFake Detection Suite
Checks all dependencies and models are ready
"""
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_imports():
    """Check all required imports"""
    imports = [
        ('torch', 'PyTorch'),
        ('torchvision', 'TorchVision'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('gradio', 'Gradio'),
        ('mediapipe', 'MediaPipe'),
        ('PIL', 'Pillow'),
        ('scipy', 'SciPy'),
    ]
    
    all_ok = True
    for module, name in imports:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Check project files exist"""
    files = [
        'main.py',
        'config.py',
        'ui/app.py',
        'models/face_detector.py',
        'models/deepfake_detector.py',
        'models/image_analyzer.py',
        'models/video_analyzer.py',
        'utils/logger.py',
    ]
    
    project_root = Path(__file__).parent
    all_ok = True
    
    for file in files:
        path = project_root / file
        if path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_ok = False
    
    return all_ok

def check_torch_cuda():
    """Check if CUDA is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA available (GPU: {torch.cuda.get_device_name(0)})")
            return True
        else:
            print("⚠️  CUDA not available (will use CPU)")
            return True
    except Exception as e:
        print(f"⚠️  Could not check CUDA: {e}")
        return True

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("🔍 DeepFake Detection Suite - Verification")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", check_project_structure),
        ("Required Imports", check_imports),
        ("GPU Support", check_torch_cuda),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        print("-" * 40)
        passed = check_func()
        all_passed = all_passed and passed
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed! Ready to run.")
        print("\nStart with:")
        print("  python main.py")
    else:
        print("❌ Some checks failed. Install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
