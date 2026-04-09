import torch
from torchvision import transforms
from PIL import Image
import random

# Custom transform for small random affine rotations
class RandomAffineSmall:
    def __init__(self, max_rotation=5, max_shear=5, max_translate=0.05):
        self.max_rotation = max_rotation
        self.max_shear = max_shear
        self.max_translate = max_translate

    def __call__(self, img):
        angle = random.uniform(-self.max_rotation, self.max_rotation)
        translate = (random.uniform(-self.max_translate, self.max_translate) * img.width,
                     random.uniform(-self.max_translate, self.max_translate) * img.height)
        shear = random.uniform(-self.max_shear, self.max_shear)
        return transforms.functional.affine(img, angle=angle, translate=translate, scale=1.0, shear=shear)

# Main augmentation pipeline
handwriting_transforms = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    RandomAffineSmall(max_rotation=5, max_shear=3, max_translate=0.05),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.Resize((32, 256)),  # <-- add resize here if needed
    transforms.GaussianBlur(kernel_size=(3, 3), sigma=(0.1, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
