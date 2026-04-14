import cv2
import numpy as np
from PIL import Image

# Import your existing modules
from preprocessing.image_preprocessor import ImagePreprocessor
from preprocessing.layout_detector import LayoutDetector
from preprocessing.layout_detector import LayoutDetector
from preprocessing.contour_analyzer import ContourAnalyzer

# Import OCR parts
from hand_writing_model.inference import HandwritingPredictor

class DocumentDigitizerPipeline:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.layout_detector = LayoutDetector()
        self.contour_analyzer = ContourAnalyzer()
        self.ocr_predictor = HandwritingPredictor()
        
    def crop_and_predict(self, image_np, bbox):
        x, y, w, h = bbox
        
        # Crop line from the original (or normalized) image
        cropped = image_np[y:y+h, x:x+w]
        
        # Convert CV2 image (numpy) to PIL Image
        img_pil = Image.fromarray(cropped).convert("L")
        
        # Run Inference using the new predictor
        return self.ocr_predictor.predict(img_pil)

    def process_document(self, image_path, output_format="md"):
        # 1. Preprocess
        binary_image = self.preprocessor.preprocess(image_path)
        original_gray = cv2.cvtColor(self.preprocessor.original_image, cv2.COLOR_BGR2GRAY)
        
        # 2. Layout Detection (Optional: Use to group sections)
        # regions = self.layout_detector.find_text_regions(binary_image)
        
        # 3. Line Detection
        lines = self.contour_analyzer.find_text_lines_peaks(binary_image)
        
        # 4. Sort lines purely by Y coordinate (top to bottom)
        lines.sort(key=lambda line: line['y_start'])
        
        # 5. Extract text for each line and calculate layout
        document_text = []
        base_x = min([line['bbox'][0] for line in lines]) if lines else 0
        
        for line in lines:
            text = self.crop_and_predict(original_gray, line['bbox'])
            
            # Basic Layout logic: Check indentation
            indent_threshold = 50 # pixels
            if line['bbox'][0] > base_x + indent_threshold:
                text = "\t" + text
                
            document_text.append(text)
            
        # 6. Format and Export
        return self.export_document(document_text, "output", output_format)

    def export_document(self, text_lines, filename, format="md"):
        final_text = "\n".join(text_lines)
        file_path = f"{filename}.{format}"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_text)
            
        return file_path

# Usage
# pipeline = DocumentDigitizerPipeline()
# result_path = pipeline.process_document("scanned_notes.jpg", output_format="md")