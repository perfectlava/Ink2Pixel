import cv2
import numpy as np
from typing import List, Dict
from .utils import validate_image


class ContourAnalyzer:
    def __init__(self):
        self.text_lines = []
        self.characters = []
    
    def find_text_lines_peaks(self, image: np.ndarray) -> List[Dict]:
        if not validate_image(image):
            return []
        
        height, width = image.shape
        horizontal_projection = np.sum(image == 255, axis=1)
        
        # Estimate text size from projection data
        text_rows = np.where(horizontal_projection > 5)[0]
        if len(text_rows) > 0:
            total_text_height = text_rows[-1] - text_rows[0] + 1
            estimated_line_height = total_text_height // 3 * 1.2  # 20% padding
        else:
            estimated_line_height = 60  # fallback
        
        peaks = []
        threshold = np.max(horizontal_projection) * 0.6
        
        for i in range(10, len(horizontal_projection) - 10):
            if (horizontal_projection[i] > threshold and
                horizontal_projection[i] > horizontal_projection[i-8] and
                horizontal_projection[i] > horizontal_projection[i+8] and
                horizontal_projection[i] >= horizontal_projection[i-1] and
                horizontal_projection[i] >= horizontal_projection[i+1]):
                peaks.append(i)
        
        filtered_peaks = []
        min_distance = int(estimated_line_height * 0.6)  # Dynamic spacing
        
        for peak in peaks:
            if not filtered_peaks or peak - filtered_peaks[-1] >= min_distance:
                filtered_peaks.append(peak)
        
        lines = []
        
        for i, peak in enumerate(filtered_peaks):
            # Give more space above the line for dots, accents, etc.
            y_start = max(0, int(peak - estimated_line_height * 0.6))  # 60% above
            y_end = min(height, int(peak + estimated_line_height * 0.4))  # 40% below
            
            # For the last line, extend to the bottom to avoid cutoff
            if i == len(filtered_peaks) - 1:
                y_end = height
            
            region = image[y_start:y_end, :]
            rows_with_text = np.where(np.sum(region == 255, axis=1) > 3)[0]
            cols_with_text = np.where(np.sum(region == 255, axis=0) > 3)[0]
            
            if len(rows_with_text) > 0 and len(cols_with_text) > 0:
                min_row = rows_with_text[0]
                max_row = rows_with_text[-1]
                min_col = cols_with_text[0]
                max_col = cols_with_text[-1]
                
                actual_y = y_start + min_row
                actual_height = max_row - min_row + 1
                actual_x = min_col
                actual_width = max_col - min_col + 1
                
                lines.append({
                    'bbox': (actual_x, actual_y, actual_width, actual_height),
                    'y_start': actual_y,
                    'y_end': actual_y + actual_height,
                    'height': actual_height
                })
        
        return lines
    
    def find_character_contours(self, image: np.ndarray) -> List[Dict]:
        if not validate_image(image):
            return []
        
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        characters = []
        min_area = 20
        max_area = image.shape[0] * image.shape[1] * 0.1
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area < min_area or area > max_area:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            if (aspect_ratio > 3 or aspect_ratio < 0.1 or
                w < 3 or h < 5 or w > 200 or h > 200):
                continue
            
            characters.append({
                'contour': contour,
                'bbox': (x, y, w, h),
                'area': area,
                'center': (x + w//2, y + h//2)
            })
        
        characters.sort(key=lambda char: (char['bbox'][1], char['bbox'][0]))
        self.characters = characters
        
        return characters