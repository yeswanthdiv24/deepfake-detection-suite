"""
Face Detection Module using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
from utils.logger import get_logger

logger = get_logger("face_detector")


class FaceDetector:
    """Detects faces in images and videos"""
    
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.detector = self.mp_face.FaceDetection(
            model_selection=1,  # 1 for full-range detection
            min_detection_confidence=0.5
        )
        logger.info("FaceDetector initialized")
    
    def detect_faces(self, image):
        """
        Detect faces in an image
        
        Args:
            image: numpy array (BGR format from OpenCV)
        
        Returns:
            List of face regions: [(x, y, w, h), ...]
        """
        if image is None:
            return []
        
        h, w = image.shape[:2]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self.detector.process(rgb_image)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Ensure coordinates are within bounds
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                faces.append((x, y, width, height))
        
        return faces
    
    def extract_face(self, image, face_bbox):
        """
        Extract a face region from an image
        
        Args:
            image: numpy array
            face_bbox: (x, y, w, h)
        
        Returns:
            Face crop (256x256)
        """
        x, y, w, h = face_bbox
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (256, 256))
        return face
    
    def draw_faces(self, image, faces):
        """Draw face bounding boxes on image"""
        image_copy = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image_copy
