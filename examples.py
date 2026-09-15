"""
Example usage scripts for DeepFake Detection Suite
"""

# Example 1: Analyze a single image
def example_image_analysis():
    """Analyze a single image for deepfakes"""
    import cv2
    from models.face_detector import FaceDetector
    from models.deepfake_detector import DeepFakeDetector
    from models.image_analyzer import ImageAnalyzer
    
    # Initialize
    face_detector = FaceDetector()
    deepfake_detector = DeepFakeDetector()
    analyzer = ImageAnalyzer(face_detector, deepfake_detector)
    
    # Analyze image
    image = cv2.imread('path/to/your/image.jpg')
    result = analyzer.analyze_image(image_array=image)
    
    # Print results
    print(analyzer.get_summary(result))


# Example 2: Analyze a video
def example_video_analysis():
    """Analyze a video for deepfakes"""
    from models.face_detector import FaceDetector
    from models.deepfake_detector import DeepFakeDetector
    from models.video_analyzer import VideoAnalyzer
    
    # Initialize
    face_detector = FaceDetector()
    deepfake_detector = DeepFakeDetector()
    analyzer = VideoAnalyzer(face_detector, deepfake_detector)
    
    # Progress callback
    def show_progress(current, total):
        print(f"Processing frame {current}/{total}")
    
    # Analyze video
    result = analyzer.analyze_video(
        'path/to/your/video.mp4',
        progress_callback=show_progress
    )
    
    # Print results
    print(analyzer.get_summary(result))


# Example 3: Batch process images
def example_batch_processing():
    """Process multiple images"""
    from pathlib import Path
    import cv2
    from models.face_detector import FaceDetector
    from models.deepfake_detector import DeepFakeDetector
    from models.image_analyzer import ImageAnalyzer
    
    # Initialize
    face_detector = FaceDetector()
    deepfake_detector = DeepFakeDetector()
    analyzer = ImageAnalyzer(face_detector, deepfake_detector)
    
    # Process all images in directory
    image_dir = Path('images')
    results = []
    
    for img_path in image_dir.glob('*.jpg'):
        print(f"Processing {img_path.name}...")
        result = analyzer.analyze_image(image_path=str(img_path))
        results.append({
            'file': img_path.name,
            'is_deepfake': result['is_likely_deepfake'],
            'score': result['average_fake_score']
        })
    
    # Print summary
    print("\nBatch Processing Results:")
    print("-" * 50)
    for r in results:
        status = "DEEPFAKE" if r['is_deepfake'] else "AUTHENTIC"
        print(f"{r['file']:30} | {status:10} | Score: {r['score']:.4f}")


# Example 4: Real-time webcam analysis
def example_webcam_analysis():
    """Analyze webcam stream"""
    import cv2
    from models.face_detector import FaceDetector
    from models.deepfake_detector import DeepFakeDetector
    
    face_detector = FaceDetector()
    deepfake_detector = DeepFakeDetector()
    
    cap = cv2.VideoCapture(0)  # 0 = default webcam
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces
        faces = face_detector.detect_faces(frame)
        
        # Analyze each face
        for face_bbox in faces:
            face = face_detector.extract_face(frame, face_bbox)
            result = deepfake_detector.detect(face)
            
            # Draw result
            x, y, w, h = face_bbox
            color = (0, 0, 255) if result['is_deepfake'] else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            label = f"Fake: {result['fake_score']:.2f}" if result['is_deepfake'] else f"Real: {result['fake_score']:.2f}"
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Display
        cv2.imshow('DeepFake Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Run examples
    print("DeepFake Detection Suite - Examples")
    print("====================================\n")
    
    # Uncomment to run:
    # example_image_analysis()
    # example_video_analysis()
    # example_batch_processing()
    # example_webcam_analysis()
