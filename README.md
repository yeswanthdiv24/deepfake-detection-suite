# 🎬 DeepFake Detection Suite

A comprehensive deep learning system for detecting AI-generated and manipulated facial media (images and videos).

## Features

- 📸 **Image Analysis**: Detect deepfakes in static images
- 🎥 **Video Analysis**: Frame-by-frame deepfake detection with temporal analysis
- 🔬 **Automatic Face Detection**: Uses MediaPipe for robust face localization
- 🤖 **CNN-based Detector**: Custom deep learning model trained on deepfake datasets
- 🎨 **Web Interface**: Gradio-based UI for easy interaction
- 📊 **Detailed Results**: Per-face confidence scores and visualizations

## Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd DeepFake\ Detection

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

This will start a web server at `http://localhost:7860`

## Usage

### Via Web Interface

1. Open `http://localhost:7860` in your browser
2. Select **Image Analysis** or **Video Analysis**
3. Upload your file
4. Click **Analyze**
5. View results with confidence scores

### Via Python API

```python
import cv2
from models.face_detector import FaceDetector
from models.deepfake_detector import DeepFakeDetector
from models.image_analyzer import ImageAnalyzer

# Initialize
face_detector = FaceDetector()
deepfake_detector = DeepFakeDetector()
analyzer = ImageAnalyzer(face_detector, deepfake_detector)

# Analyze image
image = cv2.imread('path/to/image.jpg')
result = analyzer.analyze_image(image_array=image)

print(f"Is Deepfake: {result['is_likely_deepfake']}")
print(f"Confidence: {result['average_fake_score']:.4f}")
```

## Model Architecture

### DeepFakeCNN

- **Input**: 256x256 RGB images
- **Architecture**: 4-layer CNN + 3-layer fully connected
- **Output**: Binary classification (Real/Fake)
- **Training**: Standard cross-entropy loss

```
Input (3, 256, 256)
  ↓
Conv(32) + ReLU + MaxPool + Dropout
  ↓
Conv(64) + ReLU + MaxPool + Dropout
  ↓
Conv(128) + ReLU + MaxPool + Dropout
  ↓
Conv(256) + ReLU + MaxPool + Dropout
  ↓
FC(512) + ReLU + Dropout
  ↓
FC(128) + ReLU + Dropout
  ↓
FC(2) → Softmax
  ↓
Output [fake_score, real_score]
```

## Performance

| Metric | Value |
|--------|-------|
| Accuracy | ~90% |
| Inference Speed (GPU) | 5-10 fps |
| Inference Speed (CPU) | 1-2 fps |
| Minimum Face Size | 64x64 pixels |
| Model Size | ~20 MB |

## File Structure

```
DeepFake Detection/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── models/
│   ├── face_detector.py       # Face detection (MediaPipe)
│   ├── deepfake_detector.py   # CNN deepfake classifier
│   ├── image_analyzer.py      # Image analysis
│   └── video_analyzer.py      # Video analysis
├── ui/
│   └── app.py            # Gradio web interface
└── utils/
    └── logger.py         # Logging utilities
```

## Dependencies

- **PyTorch**: Deep learning framework
- **OpenCV**: Video/image processing
- **MediaPipe**: Face detection
- **Gradio**: Web interface
- **NumPy/SciPy**: Numerical computing

See `requirements.txt` for exact versions.

## Advanced Usage

### Custom Model Training

```python
from models.deepfake_detector import DeepFakeCNN
import torch

# Load custom trained model
model = DeepFakeCNN()
model.load_state_dict(torch.load('path/to/model.pth'))

detector = DeepFakeDetector()
detector.model = model
```

### Batch Processing

```python
from pathlib import Path
from models.image_analyzer import ImageAnalyzer

# Process multiple images
image_dir = Path('images')
results = []

for img_path in image_dir.glob('*.jpg'):
    result = analyzer.analyze_image(image_path=str(img_path))
    results.append(result)
```

### Video Frame Extraction

```python
from models.video_analyzer import VideoAnalyzer

def progress(current, total):
    print(f"Processing frame {current}/{total}")

result = video_analyzer.analyze_video('video.mp4', 
                                      progress_callback=progress)

print(f"Deepfake frames: {result['deepfake_frames']}")
print(f"Percentage: {result['deepfake_percentage']:.2f}%")
```

## Limitations & Disclaimers

1. **Detection Accuracy**: Not 100% accurate; novel deepfakes may bypass detection
2. **Data Bias**: Model trained on limited demographic data; may have bias
3. **Quality Dependent**: Works best with clear faces at reasonable resolution
4. **False Positives**: Heavy compression or artifacts may cause false positives
5. **Not Legal Evidence**: Should not be used as sole evidence in legal proceedings

## Research References

This system is inspired by:
- FaceForensics++ dataset
- Xception-based detection methods
- Face manipulation detection techniques
- Temporal consistency analysis

## Future Improvements

- [ ] Support for audio deepfake detection
- [ ] Face liveness detection
- [ ] Multi-modal analysis (audio + video)
- [ ] Attention visualization
- [ ] Real-time video stream analysis
- [ ] Mobile-optimized models
- [ ] Ensemble methods for higher accuracy

## License

This project is provided for research and educational purposes.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Disclaimer**: This tool is for research and educational purposes. Always verify important media through multiple authoritative sources before making decisions based on detection results.
<img width="1589" height="900" alt="WhatsApp Image 2026-05-07 at 19 38 01 (1)" src="https://github.com/user-attachments/assets/55be30f3-bba0-475a-bded-2ff58d4038cb" />
<img width="1600" height="910" alt="WhatsApp Image 2026-05-07 at 19 38 02" src="https://github.com/user-attachments/assets/8bfb6d20-1b09-4159-ad63-0765d4f6096f" />
<img width="1600" height="775" alt="WhatsApp Image 2026-05-07 at 19 38 02 (1)" src="https://github.com/user-attachments/assets/f1d88eb2-1127-40c5-9d5b-bb44e535c94a" />

