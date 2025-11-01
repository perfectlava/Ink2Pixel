import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
from preprocessing import ImagePreprocessor
from preprocessing.utils import load_image, save_image


def main():
    """Simple demo script for testing the preprocessing pipeline."""
    
    # Input and output paths
    input_image_path = "examples/sample_images/handwritten_note.jpg"  
    output_dir = "examples/output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== Ink2Pixel Preprocessing Demo ===")
    
    # Check if input image exists
    if not os.path.exists(input_image_path):
        print(f"Please add a sample image at: {input_image_path}")
        return
    
    # Load and save original
    print("Loading image...")
    original_image = load_image(input_image_path)
    if original_image is None:
        print("Failed to load image!")
        return
    
    save_image(original_image, os.path.join(output_dir, "original.jpg"))
    print(f"Original image: {original_image.shape}")
    
    # Run preprocessing
    print("Running preprocessing...")
    preprocessor = ImagePreprocessor()
    processed_image = preprocessor.preprocess(
        input_image_path, 
        os.path.join(output_dir, "preprocessed.jpg")
    )
    
    if processed_image is None:
        print("Preprocessing failed!")
        return
    
    print(f"Processed image: {processed_image.shape}")
    
    # Print results
    print(f"\nResults:")
    print(f"- Preprocessing completed successfully")
    print(f"- Output saved in: {output_dir}")
    print("- Files: original.jpg, preprocessed.jpg")
    print("\nPreprocessing pipeline working!")


if __name__ == "__main__":
    main()