"""
DeepFake Detection Model
Uses a CNN-based approach to detect manipulated facial regions
"""
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np
from utils.logger import get_logger

logger = get_logger("deepfake_detector")


class DeepFakeCNN(nn.Module):
    """CNN model for deepfake detection"""
    
    def __init__(self):
        super(DeepFakeCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        
        # After 4 pooling layers: 256x256 -> 16x16
        self.fc1 = nn.Linear(256 * 16 * 16, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)  # Binary classification
        
    def forward(self, x):
        # Block 1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)
        x = self.dropout(x)
        
        # Block 2
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool(x)
        x = self.dropout(x)
        
        # Block 3
        x = self.conv3(x)
        x = F.relu(x)
        x = self.pool(x)
        x = self.dropout(x)
        
        # Block 4
        x = self.conv4(x)
        x = F.relu(x)
        x = self.pool(x)
        x = self.dropout(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # Dense layers
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.fc2(x)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.fc3(x)
        
        return x


class DeepFakeDetector:
    """DeepFake Detection using CNN"""
    
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DeepFakeCNN().to(self.device)
        
        # Try to load model if path provided
        if model_path:
            try:
                if os.path.exists(model_path):
                    self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                    logger.info(f"Loaded model from {model_path}")
            except Exception as e:
                logger.warning(f"Could not load model from {model_path}: {e}")
                logger.info("Using untrained model - this will give random predictions")
        else:
            logger.info("No model path provided - using untrained model")
            logger.info("Note: For accurate predictions, train the model on deepfake data")
        
        self.model.eval()
        logger.info(f"DeepFakeDetector initialized on {self.device}")
    
    def preprocess(self, face_image):
        """
        Preprocess face image for model input
        
        Args:
            face_image: numpy array (BGR)
        
        Returns:
            torch tensor (B, C, H, W)
        """
        # Resize to 256x256
        face = cv2.resize(face_image, (256, 256))
        
        # Convert BGR to RGB
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        face = face.astype(np.float32) / 255.0
        
        # Convert to tensor and add batch dimension
        face = torch.from_numpy(face).permute(2, 0, 1).unsqueeze(0)
        
        return face.to(self.device)
    
    def detect(self, face_image):
        """
        Detect if face is deepfake
        
        Args:
            face_image: numpy array (BGR)
        
        Returns:
            dict with keys: 'is_deepfake', 'confidence', 'fake_score', 'real_score'
        """
        with torch.no_grad():
            face_tensor = self.preprocess(face_image)
            output = self.model(face_tensor)
            probs = F.softmax(output, dim=1)
            
            fake_score = probs[0, 0].item()  # Deepfake probability
            real_score = probs[0, 1].item()  # Real probability
            
            is_deepfake = fake_score > 0.5
            confidence = max(fake_score, real_score)
        
        return {
            'is_deepfake': is_deepfake,
            'confidence': confidence,
            'fake_score': fake_score,
            'real_score': real_score
        }


import os
