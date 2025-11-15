import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
from preprocessing import ImagePreprocessor
from preprocessing.contour_analyzer import ContourAnalyzer
from preprocessing.utils import load_image, save_image


def main():
    input_image_path = "examples/sample_images/handwritten_note.jpg"  
    output_dir = "examples/output"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_image_path):
        print(f"Please add a sample image at: {input_image_path}")
        return
    
    original_image = load_image(input_image_path)
    if original_image is None:
        print("Failed to load image!")
        return
    
    save_image(original_image, os.path.join(output_dir, "original.jpg"))
    
    preprocessor = ImagePreprocessor()
    processed_image = preprocessor.preprocess(
        input_image_path, 
        os.path.join(output_dir, "preprocessed.jpg")
    )
    
    if processed_image is None:
        print("Preprocessing failed!")
        return
    
    contour_analyzer = ContourAnalyzer()
    text_lines = contour_analyzer.find_text_lines_peaks(processed_image)
    
    lines_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
    
    for line in text_lines:
        x, y, w, h = line['bbox']
        cv2.rectangle(lines_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    save_image(lines_image, os.path.join(output_dir, "lines_detected.jpg"))
    print(f"Found {len(text_lines)} text lines")


if __name__ == "__main__":
    main()