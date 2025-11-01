import cv2
import numpy as np
import os
from typing import Optional


def load_image(image_path: str, color_mode: str = 'color') -> Optional[np.ndarray]:
      """Load an image from file path."""
      if not os.path.exists(image_path):
          print(f"Error: Image file {image_path} not found")
          return None

      try:
          if color_mode == 'grayscale':
              image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
          else:
              image = cv2.imread(image_path, cv2.IMREAD_COLOR)

          if image is None:
              print(f"Error: Could not read image {image_path}")
              return None

          return image
      except Exception as e:
          print(f"Error loading image {image_path}: {str(e)}")
          return None


def save_image(image: np.ndarray, output_path: str) -> bool:
      """Save an image to file."""
      try:
          os.makedirs(os.path.dirname(output_path), exist_ok=True)
          success = cv2.imwrite(output_path, image)
          if not success:
              print(f"Error: Failed to save image to {output_path}")
              return False
          return True
      except Exception as e:
          print(f"Error saving image to {output_path}: {str(e)}")
          return False

def validate_image(image: np.ndarray) -> bool:
      """Check if image is valid for processing."""
      if image is None:
          return False
      if len(image.shape) not in [2, 3]:
          return False
      if image.size == 0:
          return False

      height, width = image.shape[:2]
      if height < 50 or width < 50:
          return False

      return True


def resize_image(image: np.ndarray, target_width: int = None, target_height: int = None) -> np.ndarray:
      """Resize image maintaining aspect ratio."""
      height, width = image.shape[:2]

      if target_width is None and target_height is None:
          return image

      if target_width and target_height:
          scale_w = target_width / width
          scale_h = target_height / height
          scale = min(scale_w, scale_h)
          new_width = int(width * scale)
          new_height = int(height * scale)
      elif target_width:
          scale = target_width / width
          new_width = target_width
          new_height = int(height * scale)
      else:
          scale = target_height / height
          new_height = target_height
          new_width = int(width * scale)

      return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def get_image_info(image: np.ndarray) -> dict:
      """Get basic information about an image."""
      if image is None:
          return {}

      height, width = image.shape[:2]
      channels = image.shape[2] if len(image.shape) == 3 else 1

      return {
          'width': width,
          'height': height,
          'channels': channels,
          'aspect_ratio': width / height
      }
