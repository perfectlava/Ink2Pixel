import cv2
import numpy as np
from typing import List, Dict, Tuple
from .utils import validate_image


class ContourAnalyzer:
    """Analyze contours for text line and character detection."""
    
    def __init__(self):
        self.text_lines = []
        self.characters = []
    
    def find_text_lines(self, image: np.ndarray) -> List[Dict]:
        """
        Find individual text lines using horizontal projection.
        
        Args:
            image: Binary image
            
        Returns:
            List of text line dictionaries
        """
        if not validate_image(image):
            return []
        
        height, width = image.shape
        
        # Calculate horizontal projection (sum of white pixels per row)
        horizontal_projection = np.sum(image == 255, axis=1)
        
        # Find line boundaries
        lines = []
        in_line = False
        line_start = 0
        
        # Threshold for detecting text presence
        threshold = width * 0.02  # At least 2% of row width should have text
        
        for i, pixel_count in enumerate(horizontal_projection):
            if pixel_count > threshold and not in_line:
                # Start of a line
                line_start = i
                in_line = True
            elif pixel_count <= threshold and in_line:
                # End of a line
                line_end = i
                in_line = False
                
                # Add line if substantial enough
                if line_end - line_start > 5:
                    lines.append({
                        'bbox': (0, line_start, width, line_end - line_start),
                        'y_start': line_start,
                        'y_end': line_end,
                        'height': line_end - line_start
                    })
        
        # Handle case where line extends to bottom
        if in_line:
            lines.append({
                'bbox': (0, line_start, width, height - line_start),
                'y_start': line_start,
                'y_end': height,
                'height': height - line_start
            })
        
        self.text_lines = lines
        return lines
    
    def find_character_contours(self, image: np.ndarray) -> List[Dict]:
        """
        Find individual character contours.
        
        Args:
            image: Binary image
            
        Returns:
            List of character contour dictionaries
        """
        if not validate_image(image):
            return []
        
        # Find all contours
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        characters = []
        min_area = 20  # Minimum area for a character
        max_area = image.shape[0] * image.shape[1] * 0.1  # Max 10% of image
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < min_area or area > max_area:
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by aspect ratio (characters shouldn't be too wide or narrow)
            aspect_ratio = w / h
            if aspect_ratio > 3 or aspect_ratio < 0.1:
                continue
            
            # Filter by size (reasonable character dimensions)
            if w < 3 or h < 5 or w > 200 or h > 200:
                continue
            
            characters.append({
                'contour': contour,
                'bbox': (x, y, w, h),
                'area': area,
                'center': (x + w//2, y + h//2)
            })
        
        # Sort characters left to right, top to bottom
        characters.sort(key=lambda char: (char['bbox'][1], char['bbox'][0]))
        self.characters = characters
        
        return characters