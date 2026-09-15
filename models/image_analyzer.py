"""
Image Analysis Module for deepfake detection
"""
import cv2
import numpy as np
from utils.logger import get_logger

logger = get_logger("image_analyzer")


class ImageAnalyzer:
    """Analyzes images for deepfake detection"""
    
    def __init__(self, face_detector, deepfake_detector):
        self.face_detector = face_detector
        self.deepfake_detector = deepfake_detector
    
    def analyze_image(self, image_path=None, image_array=None):
        """
        Analyze image for deepfakes
        
        Args:
            image_path: path to image file OR
            image_array: numpy array of image (BGR)
        
        Returns:
            dict with analysis results
        """
        if image_path:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Cannot read image: {image_path}")
                return None
        elif image_array is not None:
            image = image_array
        else:
            logger.error("Must provide either image_path or image_array")
            return None
        
        # Detect faces
        faces = self.face_detector.detect_faces(image)
        
        if not faces:
            logger.warning("No faces detected in image")
            return {
                'image_path': image_path,
                'faces_detected': 0,
                'detections': [],
                'is_likely_deepfake': False,
                'average_fake_score': 0.0,
                'message': 'No faces detected in image'
            }
        
        detections = []
        fake_scores = []
        
        # Analyze each face
        for i, face_bbox in enumerate(faces):
            face = self.face_detector.extract_face(image, face_bbox)
            result = self.deepfake_detector.detect(face)
            
            detections.append({
                'face_id': i,
                'bbox': face_bbox,
                'is_deepfake': result['is_deepfake'],
                'fake_score': result['fake_score'],
                'confidence': result['confidence']
            })
            
            fake_scores.append(result['fake_score'])
        
        average_fake_score = np.mean(fake_scores) if fake_scores else 0.0
        is_likely_deepfake = average_fake_score > 0.5
        
        return {
            'image_path': image_path,
            'faces_detected': len(faces),
            'detections': detections,
            'is_likely_deepfake': is_likely_deepfake,
            'average_fake_score': average_fake_score,
            'message': f"{'LIKELY DEEPFAKE' if is_likely_deepfake else 'LIKELY AUTHENTIC'}"
        }
    
    def get_summary(self, analysis_result):
        """Generate text summary of analysis"""
        if not analysis_result:
            return "Failed to analyze image"
        
        summary = f"""
IMAGE ANALYSIS SUMMARY
======================
Faces Detected: {analysis_result['faces_detected']}

DEEPFAKE DETECTION RESULTS
===========================
Average Fake Score: {analysis_result['average_fake_score']:.4f}

Per-Face Results:
"""
        
        for det in analysis_result['detections']:
            status = "DEEPFAKE ⚠️" if det['is_deepfake'] else "AUTHENTIC ✓"
            summary += f"\nFace {det['face_id']+1}: {status} (Score: {det['fake_score']:.4f})"
        
        summary += f"""

VERDICT
=======
Status: {analysis_result['message']}
        """
        return summary.strip()
