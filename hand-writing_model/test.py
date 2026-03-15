import torch
from PIL import Image
from torchvision import transforms

from learning import TinyOCR

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CHECKPOINT_PATH = "checkpoints/best.pth"
IMAGE_PATH = "test.jpg"   # image you want to test


# ---------- Load checkpoint ----------
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)

char_to_idx = checkpoint["chars"]
idx_to_char = {v: k for k, v in char_to_idx.items()}

# ---------- Load model ----------
model = TinyOCR(len(char_to_idx)).to(DEVICE)
model.load_state_dict(checkpoint["model"], strict=True)
model.eval()

print("✔ Model loaded")


# ---------- Image transform (must match training) ----------
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


# ---------- Load image ----------
img = Image.open(IMAGE_PATH)

img = transform(img)
img = img.unsqueeze(0)  # add batch dimension
img = img.to(DEVICE)


# ---------- Run model ----------
with torch.no_grad():
    outputs = model(img)

# outputs shape: T, B, C
preds = outputs.argmax(2)

preds = preds.squeeze().cpu().numpy()


# ---------- CTC Decode ----------
decoded = []
prev = None

for p in preds:
    if p != prev and p != 0:
        decoded.append(idx_to_char[p])
    prev = p

prediction = "".join(decoded)

print("\nPrediction:")
print(prediction)