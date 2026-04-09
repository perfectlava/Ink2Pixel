import torch
from torchvision import transforms as T
from PIL import Image, ImageOps, ImageEnhance
import string
import os

from learning import TinyOCR
from decoder import ctc_greedy_decode

# ---------- Settings ----------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CHECKPOINT_PATH = "checkpoints/best.pth"

# ---------- Character set ----------
chars = string.ascii_letters + string.digits + string.punctuation + " "
char_to_idx = {c: i + 2 for i, c in enumerate(chars)}
char_to_idx["<blank>"] = 0
char_to_idx["<unk>"] = 1
idx2char = {v: k for k, v in char_to_idx.items()}

# ---------- Load model ----------
model = TinyOCR(len(char_to_idx)).to(DEVICE)

# Load checkpoint dictionary
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
if "model_state" in checkpoint:
    model.load_state_dict(checkpoint["model_state"])
else:
    # fallback if saved directly as state_dict
    model.load_state_dict(checkpoint)

# Optionally load char_to_idx from checkpoint if it exists
char_to_idx = checkpoint.get("char_to_idx", char_to_idx)
idx2char = {v: k for k, v in char_to_idx.items()}

model.eval()
print("✔ Model loaded")

# ---------- Transform ----------
normalize_transform = T.Compose([
    T.ToTensor(),
    T.Normalize((0.5,), (0.5,))
])

# ---------- Preprocess function ----------
def preprocess_image(img_path, target_height=32, target_width=256):
    """Convert a single line image to a model-ready tensor."""
    img = Image.open(img_path).convert("L")  # grayscale

    # 1. Invert if text is light on dark
    if img.getextrema()[0] > 128:  # mostly white background
        img = ImageOps.invert(img)

    # 2. Autocontrast and slight brightness boost
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Brightness(img).enhance(1.2)

    # 3. Resize while keeping aspect ratio
    w, h = img.size
    new_w = max(1, int(w * target_height / h))
    img = img.resize((new_w, target_height), Image.BILINEAR)

    # 4. Pad width to target_width (right-padding)
    if new_w < target_width:
        pad = Image.new("L", (target_width, target_height), 255)  # white background
        pad.paste(img, (0, 0))
        img = pad
    elif new_w > target_width:
        img = img.crop((0, 0, target_width, target_height))

    return normalize_transform(img).unsqueeze(0)  # add batch dim

# ---------- Prediction function ----------
def predict_image(img_path):
    img_tensor = preprocess_image(img_path).to(DEVICE)
    with torch.no_grad():
        output = model(img_tensor)
        log_probs = output.log_softmax(2)
        decoded = ctc_greedy_decode(log_probs.cpu(), idx2char)
    return decoded[0]

# ---------- Test multiple images ----------
test_dir = "testing_images"
os.makedirs(test_dir, exist_ok=True)

test_images = [
    ("testing_images/image.png", "this is a handwritten"),
    ("testing_images/second.png", "Write as good as you can."),
    ("testing_images/third.png", "Plants to buy"),
    ("testing_images/fourth.png", "How to improve your handwriting")
]

for img_path, gt_text in test_images:
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")