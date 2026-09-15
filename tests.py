"""
Test suite for DeepFake Detection System
"""
import unittest
import numpy as np
import cv2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from models.face_detector import FaceDetector
from models.deepfake_detector import DeepFakeDetector, DeepFakeCNN


class TestFaceDetector(unittest.TestCase):
    """Test face detection module"""
    
    def setUp(self):
        self.detector = FaceDetector()
    
    def test_initialization(self):
        """Test face detector initializes"""
        self.assertIsNotNone(self.detector.detector)
    
    def test_detect_faces_empty_image(self):
        """Test detection on empty image"""
        image = np.zeros((480, 640, 3), dtype=np.uint8)
        faces = self.detector.detect_faces(image)
        self.assertEqual(len(faces), 0)
    
    def test_detect_faces_none_input(self):
        """Test detection with None input"""
        faces = self.detector.detect_faces(None)
        self.assertEqual(len(faces), 0)


class TestDeepFakeCNN(unittest.TestCase):
    """Test deepfake detection model"""
    
    def setUp(self):
        self.model = DeepFakeCNN()
    
    def test_model_initialization(self):
        """Test model initializes"""
        self.assertIsNotNone(self.model)
    
    def test_model_forward_pass(self):
        """Test model forward pass"""
        import torch
        self.model.eval()
        
        # Random input
        x = torch.randn(1, 3, 256, 256)
        
        with torch.no_grad():
            output = self.model(x)
        
        # Check output shape
        self.assertEqual(output.shape, (1, 2))
    
    def test_output_valid(self):
        """Test model output is valid"""
        import torch
        import torch.nn.functional as F
        
        self.model.eval()
        x = torch.randn(1, 3, 256, 256)
        
        with torch.no_grad():
            output = self.model(x)
            probs = F.softmax(output, dim=1)
        
        # Check probabilities sum to 1
        self.assertAlmostEqual(probs.sum().item(), 1.0, places=5)


class TestDeepFakeDetector(unittest.TestCase):
    """Test deepfake detector"""
    
    def setUp(self):
        self.detector = DeepFakeDetector()
    
    def test_detector_initialization(self):
        """Test detector initializes"""
        self.assertIsNotNone(self.detector.model)
        self.assertIsNotNone(self.detector.device)
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        image = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
        tensor = self.detector.preprocess(image)
        
        # Check tensor shape
        self.assertEqual(tensor.shape, (1, 3, 256, 256))
        
        # Check values are normalized
        self.assertLessEqual(tensor.max(), 1.0)
        self.assertGreaterEqual(tensor.min(), 0.0)
    
    def test_detect_returns_dict(self):
        """Test detect returns expected format"""
        image = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
        result = self.detector.detect(image)
        
        # Check required keys
        self.assertIn('is_deepfake', result)
        self.assertIn('confidence', result)
        self.assertIn('fake_score', result)
        self.assertIn('real_score', result)
        
        # Check types
        self.assertIsInstance(result['is_deepfake'], bool)
        self.assertIsInstance(result['confidence'], float)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestFaceDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestDeepFakeCNN))
    suite.addTests(loader.loadTestsFromTestCase(TestDeepFakeDetector))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
