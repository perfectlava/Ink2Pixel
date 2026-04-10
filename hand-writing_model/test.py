import torch
import re
from torchvision import transforms as T
from PIL import Image
import string
import os


from learning import TinyOCR
from decoder import ctc_beam_search_decode


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CHECKPOINT_PATH = "checkpoints/best.pth"


chars = string.ascii_letters + string.digits + string.punctuation + " "
char_to_idx = {c: i + 2 for i, c in enumerate(chars)}
char_to_idx["<blank>"] = 0
char_to_idx["<unk>"] = 1
idx2char = {v: k for k, v in char_to_idx.items()}


model = TinyOCR(len(char_to_idx)).to(DEVICE)
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
model.load_state_dict(checkpoint["model_state"] if "model_state" in checkpoint else checkpoint)
char_to_idx = checkpoint.get("char_to_idx", char_to_idx)
idx2char = {v: k for k, v in char_to_idx.items()}
model.eval()
print("✔ Model loaded")


infer_transform = T.Compose([
    T.Grayscale(num_output_channels=1),
    T.Resize((32, 240)),
    T.Pad((8, 0, 8, 0)),          # 8px white margin left & right
    T.ToTensor(),
    T.Normalize((0.5,), (0.5,)),
])


def clean_output(text):
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9]+$', '', text)  # strip trailing punctuation only
    text = re.sub(r' +', ' ', text)
    return text.strip()


def predict_image(img_path):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    img = img.crop((int(w * 0.015), 0, w, h))
    img_tensor = infer_transform(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model(img_tensor)
        log_probs = output.log_softmax(2)
        logits = log_probs[:, 0, :].cpu()
    return clean_output(ctc_beam_search_decode(logits, idx2char, beam_width=5))


test_images = [
    ("testing_images/first.png",  "this is a handwritten"),
    ("testing_images/second.png", "Write as good as you can."),
    ("testing_images/third.png",  "Plants to buy"),
    ("testing_images/fourth.png", "How to improve your handwriting"),
    ("testing_images/fifth.png", "HELLO, MY NAME IS"),
    ("testing_images/sixth.png", "to us human is what water to"),
    ("testing_images/seventh.png", "fish.Love shines the"),
    ("testing_images/eight.png", "light of humanity,we born in it,we live by it.Too"),
    ("testing_images/ninth.png", "take it as granted,but we should know love is o"),
    ("testing_images/tenth.png", "saying the quickest way to recieve love is to give")
]


for img_path, gt_text in test_images:
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")
