# Ink2Pixel Preprocessing

Image preprocessing pipeline for handwritten document analysis and OCR preparation.

## Overview

This module provides comprehensive image preprocessing functionality to prepare handwritten documents for optical character recognition (OCR). The pipeline includes contrast enhancement, noise reduction, thresholding, and cleanup operations.

## Project Structure

```
preprocessing/
├── __init__.py              # Module exports
├── image_preprocessor.py    # Main preprocessing pipeline
├── layout_detector.py       # Text region detection
├── contour_analyzer.py      # Text line and character analysis
└── utils.py                 # Helper functions

examples/
├── preprocessing_demo.py    # Demo script
└── output/                  # Generated output files

requirements.txt             # Dependencies
```

## Core Functions

### ImagePreprocessor

Main preprocessing class that handles the complete image processing pipeline.

**`preprocess(image_path, output_path=None)`**
- Runs the complete preprocessing pipeline
- Loads image, applies contrast enhancement, noise reduction, thresholding, and cleanup
- Returns binary image ready for OCR

**`enhance_contrast(image, method='clahe')`**
- Improves image contrast using CLAHE, histogram equalization, or gamma correction
- CLAHE (default) provides adaptive contrast enhancement

**`reduce_noise(image, method='bilateral')`**
- Reduces image noise while preserving edges
- Bilateral filtering (default) maintains text sharpness

**`apply_threshold(image, method='adaptive')`**
- Converts grayscale to binary image
- Adaptive thresholding (default) handles varying lighting conditions

**`clean_binary_image(image)`**
- Removes noise from binary images
- Uses median filtering, morphological operations, and component analysis

### LayoutDetector

Detects text regions and layout structure in documents.

**`find_text_regions(image)`**
- Finds text blocks in the image using contour analysis
- Returns list of regions with bounding boxes and areas

**`get_text_area_roi(image, padding=20)`**
- Extracts main text area excluding margins
- Returns cropped image focused on text content

### ContourAnalyzer

Analyzes contours for detailed text structure detection.

**`find_text_lines(image)`**
- Detects individual text lines using horizontal projection
- Returns list of line positions and heights

**`find_character_contours(image)`**
- Finds individual character boundaries
- Filters by size and aspect ratio to remove noise

### Utils

Helper functions for common image operations.

**`load_image(image_path, color_mode='color')`**
- Loads images from file with error handling
- Supports color, grayscale, and unchanged modes

**`save_image(image, output_path)`**
- Saves images to file with directory creation
- Returns success/failure status

**`validate_image(image)`**
- Checks if image is valid for processing
- Validates dimensions, size, and format

**`resize_image(image, target_width=None, target_height=None)`**
- Resizes image while maintaining aspect ratio
- Handles single dimension or constrained resizing

**`get_image_info(image)`**
- Returns image properties (dimensions, channels, type)
- Useful for debugging and analysis

## Usage Example

```python
from preprocessing import ImagePreprocessor

# Initialize preprocessor
preprocessor = ImagePreprocessor()

# Process image
result = preprocessor.preprocess('input.jpg', 'output.jpg')

if result is not None:
    print("Preprocessing completed successfully")
```

## Demo Script

Run the demo to test the preprocessing pipeline:

```bash
python examples/preprocessing_demo.py
```

**Requirements:**
- Place a handwritten image at `examples/sample_images/handwritten_note.jpg`
- Demo generates processed outputs in `examples/output/`

## Dependencies

Install required packages:

```bash
sudo apt update
sudo apt install python3-opencv python3-numpy python3-matplotlib python3-pil python3-skimage python3-scipy
```

## Pipeline Steps

1. **Load Image** - Read input image file
2. **Convert to Grayscale** - Prepare for processing
3. **Enhance Contrast** - Improve text visibility
4. **Reduce Noise** - Remove artifacts while preserving edges
5. **Apply Thresholding** - Create binary image
6. **Clean Binary Image** - Final noise removal and smoothing

## Output

The pipeline produces clean, binary images optimized for OCR processing with:
- High contrast between text and background
- Minimal noise and artifacts
- Preserved text character details
- Consistent formatting

## Next Steps

- Integrate with EasyOCR for text recognition
- Test with various handwriting styles
- Fine-tune parameters for specific use cases