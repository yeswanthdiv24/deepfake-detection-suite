# 🎬 DeepFake Detection Suite - Complete Setup Guide

## 📋 What You Have

Your complete deepfake detection system includes:

### ✅ Core Components
- **Face Detection Module** - Uses MediaPipe for robust face localization
- **DeepFake CNN Model** - Custom convolutional neural network
- **Image Analyzer** - Analyzes single images
- **Video Analyzer** - Processes videos frame-by-frame
- **Web UI** - Gradio-based web interface
- **Logging System** - Comprehensive logging throughout

### ✅ Supporting Files
- Configuration management (`config.py`)
- Examples and usage documentation (`examples.py`)
- Unit tests (`tests.py`)
- Verification script (`verify.py`)
- Complete README and documentation

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- macOS, Linux, or Windows
- ~4GB RAM minimum
- CUDA 11.8+ (optional, for GPU acceleration)

### Installation Steps

#### 1. Navigate to Project
```bash
cd ~/Downloads/DeepFake\ Detection
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

**Installation Time**: ~5-10 minutes depending on internet speed

#### 5. Verify Installation
```bash
python verify.py
```

Expected output:
```
✅ Python 3.9+
✅ Project Structure
✅ Required Imports
✅ CUDA available (GPU)
✅ All checks passed!
```

---

## 🌐 Starting the Application

### Option 1: Start Web Server
```bash
python main.py
```

Then open: **http://localhost:7860**

### Option 2: Run Verification First
```bash
python verify.py  # Check everything is installed
python main.py    # Start server
```

### Expected Console Output
```
2024-XX-XX XX:XX:XX - main - INFO - Starting DeepFake Detection Suite...
2024-XX-XX XX:XX:XX - app - INFO - Initializing models...
2024-XX-XX XX:XX:XX - face_detector - INFO - FaceDetector initialized
2024-XX-XX XX:XX:XX - deepfake_detector - INFO - DeepFakeDetector initialized on cuda
Running on local URL:  http://0.0.0.0:7860
```

---

## 🖥️ Using the Web Interface

### Image Analysis
1. Click **📸 Image Analysis** tab
2. Click upload area or drag image
3. Supported formats: JPG, PNG, BMP
4. Click **🔍 Analyze Image**
5. View results and visualization

### Video Analysis
1. Click **🎥 Video Analysis** tab
2. Click upload area or drag video
3. Supported formats: MP4, AVI, MOV
4. Click **🔍 Analyze Video**
5. Wait for frame-by-frame processing
6. View results summary

### Understanding Results

#### Image Analysis Results
```
DEEPFAKE DETECTION RESULTS
===========================
Average Fake Score: 0.7543

Per-Face Results:
Face 1: DEEPFAKE ⚠️ (Score: 0.7543)
Face 2: AUTHENTIC ✓ (Score: 0.2891)

VERDICT
=======
Status: LIKELY DEEPFAKE
```

- **Score 0.0-0.5**: Likely authentic
- **Score 0.5-0.7**: Uncertain
- **Score 0.7-1.0**: Likely deepfake

#### Video Analysis Results
```
DEEPFAKE FRAMES: 245 / 1000
Percentage Deepfake: 24.50%

VERDICT
Status: LIKELY DEEPFAKE ⚠️
Confidence: High
```

- **Percentage < 10%**: Likely authentic
- **Percentage 10-30%**: Moderately suspicious
- **Percentage > 30%**: Likely deepfake

---

## 💻 Python API Usage

### Basic Image Analysis
```python
import cv2
from models.image_analyzer import ImageAnalyzer
from models.face_detector import FaceDetector
from models.deepfake_detector import DeepFakeDetector

# Initialize
face_detector = FaceDetector()
deepfake_detector = DeepFakeDetector()
analyzer = ImageAnalyzer(face_detector, deepfake_detector)

# Load image
image = cv2.imread('path/to/image.jpg')

# Analyze
result = analyzer.analyze_image(image_array=image)

# Results
print(f"Deepfake: {result['is_likely_deepfake']}")
print(f"Confidence: {result['average_fake_score']:.4f}")
print(analyzer.get_summary(result))
```

### Video Analysis
```python
from models.video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer(face_detector, deepfake_detector)

def progress(current, total):
    print(f"Frame {current}/{total}")

result = analyzer.analyze_video(
    'path/to/video.mp4',
    progress_callback=progress
)

print(analyzer.get_summary(result))
```

### Batch Processing
```python
from pathlib import Path

image_dir = Path('images')
results = []

for img_path in image_dir.glob('*.jpg'):
    result = analyzer.analyze_image(image_path=str(img_path))
    results.append(result)
    print(f"{img_path.name}: {result['average_fake_score']:.4f}")
```

### Webcam Real-time
```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    faces = face_detector.detect_faces(frame)
    
    for bbox in faces:
        face = face_detector.extract_face(frame, bbox)
        result = deepfake_detector.detect(face)
        
        x, y, w, h = bbox
        color = (0, 0, 255) if result['is_deepfake'] else (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    
    cv2.imshow('Deepfake Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# Detection thresholds
FACE_DETECTION_CONFIDENCE = 0.5      # MediaPipe threshold
DEEPFAKE_THRESHOLD = 0.5             # Binary classification threshold

# Image processing
IMAGE_SIZE = 256                      # Input size for CNN
BATCH_SIZE = 4                        # Batch processing size

# Video processing
MAX_VIDEO_FRAMES = 1000               # Max frames to process
VIDEO_FRAME_SAMPLE_RATE = 1           # Process every nth frame

# UI
UI_PORT = 7860                        # Web server port
UI_HOST = "0.0.0.0"                   # Bind to all interfaces

# GPU/CPU
DEVICE = "cuda"                       # "cuda" or "cpu"
```

---

## 📊 Performance Optimization

### For Speed
```python
# In config.py
BATCH_SIZE = 8              # Increase batch size
VIDEO_FRAME_SAMPLE_RATE = 2 # Skip frames
IMAGE_SIZE = 224            # Reduce input size
DEVICE = "cuda"             # Use GPU
```

### For Accuracy
```python
# In config.py
BATCH_SIZE = 1              # Process one at a time
VIDEO_FRAME_SAMPLE_RATE = 1 # Process every frame
IMAGE_SIZE = 512            # Larger input (requires GPU)
DEVICE = "cuda"             # Use GPU
```

### For Lower Memory
```python
# In config.py
BATCH_SIZE = 1
MAX_VIDEO_FRAMES = 100
IMAGE_SIZE = 224
```

---

## 🧪 Testing & Verification

### Run Tests
```bash
python tests.py
```

Tests verify:
- ✅ Face detector functionality
- ✅ CNN model architecture
- ✅ Model forward passes
- ✅ Output format validation
- ✅ Preprocessing correctness

### Verify Installation
```bash
python verify.py
```

Checks:
- ✅ Python version
- ✅ All required files
- ✅ All imports available
- ✅ GPU/CUDA support

### Run Examples
```bash
python examples.py
# Then uncomment desired example functions
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Solution 1: Use different port
# Edit main.py, change 7860 to another port

# Solution 2: Find process using port
lsof -i :7860
kill -9 <PID>
```

### Out of Memory
```python
# In config.py, reduce batch size
BATCH_SIZE = 1

# Or reduce max video frames
MAX_VIDEO_FRAMES = 100
```

### GPU Not Detected
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.cuda.get_device_name(0))"

# Force CPU
# Edit config.py: DEVICE = "cpu"
```

### Slow Performance
- Use GPU instead of CPU
- Reduce IMAGE_SIZE
- Increase VIDEO_FRAME_SAMPLE_RATE
- Reduce MAX_VIDEO_FRAMES

### Model Loading Issues
```python
# Models download on first use
# Ensure you have ~500MB free space
# For models directory: MODELS_DIR
```

---

## 📚 File Reference

### Entry Points
- **main.py** - Start web server
- **verify.py** - Verify installation
- **examples.py** - Code examples
- **tests.py** - Unit tests

### Core Modules
- **models/face_detector.py** - Face detection
- **models/deepfake_detector.py** - CNN model
- **models/image_analyzer.py** - Single image analysis
- **models/video_analyzer.py** - Video analysis

### UI & Utils
- **ui/app.py** - Gradio web interface
- **utils/logger.py** - Logging utilities
- **config.py** - Configuration

### Documentation
- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start
- **BUILD_SUMMARY.md** - Build summary
- **SETUP.md** - This file

---

## 🎓 Model Details

### DeepFakeCNN Architecture
```
Input: 256×256 RGB Image
  ↓
Convolution(32) → ReLU → MaxPool(2)
  ↓
Convolution(64) → ReLU → MaxPool(2)
  ↓
Convolution(128) → ReLU → MaxPool(2)
  ↓
Convolution(256) → ReLU → MaxPool(2)
  ↓
Flatten
  ↓
Dense(512) → ReLU
  ↓
Dense(128) → ReLU
  ↓
Dense(2) → Softmax
  ↓
Output: [fake_prob, real_prob]
```

### Training Data
- FaceForensics++ dataset
- DFDC (Deepfake Detection Challenge)
- Celeb-DF dataset

### Limitations
1. Adversarial deepfakes may bypass detection
2. Trained on specific deepfake types
3. Accuracy varies by video quality
4. May have demographic bias
5. Requires clear, frontal faces

---

## 🔐 Security & Privacy Notes

1. **No Data Storage**: Input files are not saved
2. **Local Processing**: Everything runs locally
3. **No External Calls**: No internet required after setup
4. **Model Offline**: Models download once, then offline
5. **Delete Models**: Remove models/pretrained/ to free space

---

## 📞 Support & Resources

### If Something Goes Wrong
1. Run `python verify.py`
2. Check the logs in `logs/` directory
3. Try `python tests.py`
4. Review `examples.py` for correct usage
5. Check configuration in `config.py`

### Learning Resources
- **PyTorch**: https://pytorch.org/tutorials
- **MediaPipe**: https://mediapipe.dev/solutions
- **Gradio**: https://www.gradio.app/docs
- **OpenCV**: https://docs.opencv.org/

### Additional Links
- FaceForensics++: http://c23.cs.washington.edu
- Deepfake Detection Challenge: https://www.deepfakedetectionchallenge.org
- MediaPipe Face Detection: https://mediapipe.dev/solutions/face_detection

---

## ✅ Final Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Verification passed (`python verify.py`)
- [ ] Port 7860 is available
- [ ] ~2GB free memory

After starting:
- [ ] Web UI opens at http://localhost:7860
- [ ] Can upload images
- [ ] Can upload videos
- [ ] Analyzes and returns results

---

## 🎉 You're Ready!

```bash
# Activate environment
source venv/bin/activate

# Start application
python main.py

# Open in browser
# http://localhost:7860
```

**Enjoy detecting deepfakes!** 🎬🔍

---

*Last Updated: April 2026*
*System Version: 1.0*
