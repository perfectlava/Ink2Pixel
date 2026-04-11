import numpy as np
from PIL import Image
from pix2tex.cli import LatexOCR

class Math2LaTeXPipeline:
    def __init__(self):
        """
        Initialize the model once. 
        Loading the model is the most CPU/RAM intensive part. 
        Doing it in the __init__ ensures it only happens once when your app starts.
        """
        print("Loading Math2LaTeX model into memory...")
        self.model = LatexOCR()
        print("Model loaded successfully!")

    def extract_latex(self, image_input, roi=None):
        """
        Helper function to extract LaTeX from an image.
        
        :param image_input: Can be a pre-cropped PIL Image, a NumPy array (OpenCV), or a file path.
        :param roi: Optional tuple (left, top, right, bottom). Used only if you want to crop here.
        :return: String containing the LaTeX code.
        """
        # 1. Handle the input type (Memory is faster than Disk)
        if isinstance(image_input, Image.Image):
            img = image_input
        elif isinstance(image_input, np.ndarray):
            # If you are using OpenCV, convert the numpy array to a PIL Image
            # Note: OpenCV uses BGR, PIL uses RGB. If colors matter (not usually for OCR), 
            # you might need cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB) first.
            img = Image.fromarray(image_input)
        elif isinstance(image_input, str):
            # Fallback: Read from disk if a path is provided
            img = Image.open(image_input)
        else:
            raise ValueError("image_input must be a PIL Image, NumPy array, or file path.")

        # 2. Apply ROI crop if provided (left, upper, right, lower)
        if roi is not None:
            img = img.crop(roi)

        # 3. Ensure image is in RGB mode (required by the AI model)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 4. Run inference
        try:
            latex_result = self.model(img)
            return latex_result
        except Exception as e:
            return f"Error processing image: {str(e)}"

# ==========================================
# Example Usage in your Application Pipeline
# ==========================================
if __name__ == "__main__":
    # 1. Initialize the pipeline once when your app starts
    math_pipeline = Math2LaTeXPipeline()

    # --- APPROACH 1: The Faster Way (Pre-cropped in memory) ---
    # Imagine 'full_image' is already loaded in your app's memory
    full_image = Image.open("sample_math.png") 
    
    # App logic crops the image in memory (left, top, right, bottom)
    cropped_image = full_image.crop((50, 50, 300, 150)) 
    
    # Pass the image directly (No disk read, very fast)
    result_1 = math_pipeline.extract_latex(cropped_image)
    print(f"Result from pre-cropped image:\n{result_1}\n")


    # --- APPROACH 2: The Fallback Way (Path + ROI) ---
    # Slower because it forces the script to read "sample_math.png" from the hard drive
    roi_coordinates = (50, 50, 300, 150)
    result_2 = math_pipeline.extract_latex("sample_math.png", roi=roi_coordinates)
    print(f"Result from Path + ROI:\n{result_2}")