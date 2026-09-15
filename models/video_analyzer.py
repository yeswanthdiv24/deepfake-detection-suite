"""
Video Analysis Module for deepfake detection
"""
import cv2
import numpy as np
from collections import deque
from utils.logger import get_logger

logger = get_logger("video_analyzer")


class VideoAnalyzer:
    """Analyzes video frames for deepfake detection"""
    
    def __init__(self, face_detector, deepfake_detector):
        self.face_detector = face_detector
        self.deepfake_detector = deepfake_detector
        self.frame_buffer = deque(maxlen=30)
    
    def analyze_video(self, video_path, progress_callback=None):
        """
        Analyze video for deepfakes
        
        Args:
            video_path: path to video file
            progress_callback: function to call with progress (current, total)
        
        Returns:
            dict with analysis results
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Cannot open video: {video_path}")
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        frame_detections = []
        deepfake_frames = []
        
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_idx += 1
            
            # Detect faces
            faces = self.face_detector.detect_faces(frame)
            
            frame_results = {
                'frame_num': frame_idx,
                'timestamp': frame_idx / fps,
                'faces': len(faces),
                'detections': []
            }
            
            # Analyze each face
            for face_bbox in faces:
                face = self.face_detector.extract_face(frame, face_bbox)
                result = self.deepfake_detector.detect(face)
                
                frame_results['detections'].append({
                    'bbox': face_bbox,
                    'is_deepfake': result['is_deepfake'],
                    'fake_score': result['fake_score']
                })
                
                if result['is_deepfake']:
                    deepfake_frames.append(frame_idx)
            
            frame_detections.append(frame_results)
            
            if progress_callback:
                progress_callback(frame_idx, total_frames)
        
        cap.release()
        
        # Calculate overall statistics
        total_deepfake_frames = len(set(deepfake_frames))
        deepfake_percentage = (total_deepfake_frames / total_frames * 100) if total_frames > 0 else 0
        
        return {
            'video_path': video_path,
            'total_frames': total_frames,
            'fps': fps,
            'duration_sec': total_frames / fps if fps > 0 else 0,
            'deepfake_frames': total_deepfake_frames,
            'deepfake_percentage': deepfake_percentage,
            'frame_detections': frame_detections,
            'is_likely_deepfake': deepfake_percentage > 20  # If >20% deepfake, likely manipulated
        }
    
    def get_summary(self, analysis_result):
        """Generate text summary of analysis"""
        if not analysis_result:
            return "Failed to analyze video"
        
        summary = f"""
VIDEO ANALYSIS SUMMARY
======================
File: {analysis_result['video_path']}
Duration: {analysis_result['duration_sec']:.2f} seconds
Total Frames: {analysis_result['total_frames']}
FPS: {analysis_result['fps']:.2f}

DEEPFAKE DETECTION RESULTS
===========================
Frames with Deepfake: {analysis_result['deepfake_frames']} / {analysis_result['total_frames']}
Percentage Deepfake: {analysis_result['deepfake_percentage']:.2f}%

VERDICT
=======
Status: {"LIKELY DEEPFAKE ⚠️" if analysis_result['is_likely_deepfake'] else "LIKELY AUTHENTIC ✓"}
Confidence: {"High" if analysis_result['deepfake_percentage'] > 50 else "Moderate" if analysis_result['deepfake_percentage'] > 20 else "Low"}
        """
        return summary.strip()
