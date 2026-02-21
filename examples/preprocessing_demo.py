import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
from preprocessing import ImagePreprocessor
from preprocessing.contour_analyzer import ContourAnalyzer
from preprocessing.utils import load_image, save_image
import glob, csv

def main():
    input_image_path = "sample_images"  
    output_dir = "output"
    
    os.makedirs(output_dir, exist_ok=True)
    image_paths = glob.glob(os.path.join(input_image_path, "*.*"))
    
    if not image_paths:
        print(f"Please add a sample image at: {input_image_path}")
        return

    for input_image in image_paths: 
        original_image = load_image(input_image)
        if original_image is None:
            print("Failed to load image!")
            return
        
        base_name = os.path.basename(input_image)
        
        preprocessor = ImagePreprocessor()
        processed_image = preprocessor.preprocess(
            input_image, 
            os.path.join(output_dir, f"preprocessed_{base_name}")
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
        
        final_output_dir = os.path.join(output_dir, "final_output")
        os.makedirs(final_output_dir, exist_ok=True)
        
        save_image(lines_image, os.path.join(final_output_dir, base_name))
        print(f"Found {len(text_lines)} text lines")

    ### Delete after done
    print("This will rewrite all labels.")
    if input("Type Y to proceed: ") != "Y":
        exit()

    output_paths = glob.glob(os.path.join("output/final_output", "*.*"))
    output_paths = [os.path.relpath(path, "output") for path in output_paths]
    
    with open("output/labels.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "text"])

        for path in output_paths:
            writer.writerow([path, ""])

if __name__ == "__main__":
    main()