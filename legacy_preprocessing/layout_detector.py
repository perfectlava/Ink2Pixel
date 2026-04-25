import cv2
import numpy as np
from typing import List, Dict
from .utils import validate_image


class LayoutDetector:
    """Detect basic layout and text regions in handwritten documents."""
    
    def __init__(self):
        self.text_regions = []
    
    def find_text_regions(self, image: np.ndarray) -> List[Dict]:
        """
        Find text regions/blocks in the image.
        
        Args:
            image: Preprocessed binary image
            
        Returns:
            List of text region dictionaries
        """
        if not validate_image(image):
            return []
        
        processed = image.copy()
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.dilate(processed, kernel, iterations=1)
        
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        min_area = 200  
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            
            aspect_ratio = w / h
            if aspect_ratio > 15 or aspect_ratio < 0.1:
                continue
            
            text_regions.append({
                'bbox': (x, y, w, h),
                'area': area
            })
        
        text_regions.sort(key=lambda region: region['bbox'][1])
        self.text_regions = text_regions
        
        return text_regions
    
    def get_text_area_roi(self, image: np.ndarray, padding: int = 20) -> np.ndarray:
        """
        Extract the main text area ROI with minimal padding.
        
        Args:
            image: Input image
            padding: Padding around text area
            
        Returns:
            Cropped image with text area only
        """
        if not validate_image(image):
            return image
        
        if not self.text_regions:
            return image
        
        height, width = image.shape[:2]
        
        min_x = min(region['bbox'][0] for region in self.text_regions)
        min_y = min(region['bbox'][1] for region in self.text_regions)
        max_x = max(region['bbox'][0] + region['bbox'][2] for region in self.text_regions)
        max_y = max(region['bbox'][1] + region['bbox'][3] for region in self.text_regions)
        
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(width, max_x + padding)
        max_y = min(height, max_y + padding)
        
        return image[min_y:max_y, min_x:max_x]