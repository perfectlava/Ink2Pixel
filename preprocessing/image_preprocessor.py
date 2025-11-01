import cv2
import numpy as np
from typing import Optional, Tuple
from .utils import load_image, save_image, validate_image


class ImagePreprocessor:
    """Main preprocessing pipeline for handwritten document images."""
    
    def __init__(self):
        self.processed_image = None
        self.original_image = None
    
    def preprocess(self, image_path: str, output_path: str = None) -> Optional[np.ndarray]:
        """Complete preprocessing pipeline."""
        self.original_image = load_image(image_path, color_mode='color')
        if not validate_image(self.original_image):
            return None
        
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        # Main processing chain
        processed = self.enhance_contrast(gray)
        processed = self.reduce_noise(processed, method='bilateral')
        processed = self.apply_threshold(processed, method='adaptive')
        processed = self.clean_binary_image(processed)
        
        self.processed_image = processed
        
        if output_path:
            save_image(processed, output_path)
        
        return processed
    
    def enhance_contrast(self, image: np.ndarray, method: str = 'clahe') -> np.ndarray:
        """Enhance image contrast."""
        if method == 'clahe':
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(image)
        
        elif method == 'histogram_eq':
            return cv2.equalizeHist(image)
        
        elif method == 'gamma':
            gamma = 1.2
            lookup_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            return cv2.LUT(image, lookup_table)
        
        return image
    
    def reduce_noise(self, image: np.ndarray, method: str = 'bilateral') -> np.ndarray:
        """Reduce noise while preserving edges."""
        if method == 'bilateral':
            return cv2.bilateralFilter(image, 9, 75, 75)
        elif method == 'gaussian':
            return cv2.GaussianBlur(image, (5, 5), 0)
        elif method == 'median':
            return cv2.medianBlur(image, 5)
        
        return image
    
    def apply_threshold(self, image: np.ndarray, method: str = 'adaptive') -> np.ndarray:
        """Convert to binary image."""
        if method == 'adaptive':
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == 'otsu':
            _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return binary
        elif method == 'simple':
            _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            return binary
        
        return image
    
    def clean_binary_image(self, image: np.ndarray) -> np.ndarray:
        """Remove noise from binary image."""
        # Remove salt-and-pepper noise
        cleaned = cv2.medianBlur(image, 5)
        
        # Morphological opening to remove small noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Filter out tiny components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned, connectivity=8)
        min_size = 10
        cleaned_image = np.zeros_like(cleaned)
        
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_size:
                cleaned_image[labels == i] = 255
        
        # Smooth text characters
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        cleaned_image = cv2.morphologyEx(cleaned_image, cv2.MORPH_CLOSE, kernel)
        
        return cleaned_image
    
    def normalize_image(self, image: np.ndarray, target_size: Tuple[int, int] = (800, 600)) -> np.ndarray:
        """
        Normalize image size and intensity values.
        
        Args:
            image: Input image
            target_size: (width, height) tuple
            
        Returns:
            Normalized image
        """
        # Resize while maintaining aspect ratio
        height, width = image.shape[:2]
        target_width, target_height = target_size
        
        scale_w = target_width / width
        scale_h = target_height / height
        scale = min(scale_w, scale_h)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Create canvas and center the image
        canvas = np.zeros((target_height, target_width), dtype=np.uint8)
        if len(resized.shape) == 3:
            canvas = np.zeros((target_height, target_width, resized.shape[2]), dtype=np.uint8)
        
        y_offset = (target_height - new_height) // 2
        x_offset = (target_width - new_width) // 2
        
        canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
        
        return canvas
    
    def get_preprocessing_info(self) -> dict:
        """Get information about the last preprocessing operation."""
        if self.original_image is None or self.processed_image is None:
            return {}
        
        orig_height, orig_width = self.original_image.shape[:2]
        proc_height, proc_width = self.processed_image.shape[:2]
        
        return {
            'original_size': (orig_width, orig_height),
            'processed_size': (proc_width, proc_height),
            'original_channels': len(self.original_image.shape),
            'processed_channels': len(self.processed_image.shape)
        }