import torch
from torchvision import transforms
from datasets import load_dataset

from learning import TinyOCR
from decoder import ctc_greedy_decode

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CHECKPOINT_PATH = "checkpoints/best.pth"
NUM_SAMPLES = 50

# ---------- Load checkpoint ----------
checkpoint = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
char_to_idx = checkpoint["char_to_idx"]
idx_to_char = {v: k for k, v in char_to_idx.items()}

# ---------- Load model ----------
model = TinyOCR(len(char_to_idx)).to(DEVICE)
model.load_state_dict(checkpoint["model"], strict=True)
model.eval()
print("✔ Model loaded")

# ---------- Transform (must match training) ----------
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize(32),
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x[:, :, :512] if x.shape[-1] > 512 else x),
    transforms.Normalize((0.5,), (0.5,))
])

# ---------- Load dataset ----------
dataset = load_dataset("Teklia/IAM-line")["test"]
print("Testing on", NUM_SAMPLES, "samples\n")

correct = 0

for i in range(NUM_SAMPLES):
    sample = dataset[i]
    img = sample["image"]
    gt_text = sample["text"]

    img = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(img)
        log_probs = outputs.log_softmax(2)
        pred_text = ctc_greedy_decode(log_probs, idx_to_char)[0]

    is_correct = pred_text.strip() == gt_text.strip()
    if is_correct: correct += 1

    print(f"Sample {i}\nGT  : {gt_text}\nPRED: {pred_text}\n{'✔ Correct' if is_correct else '✘ Wrong'}\n")

accuracy = correct / NUM_SAMPLES
print("-------------")
print(f"Accuracy: {accuracy:.4f}")
print(f"Correct: {correct}/{NUM_SAMPLES}")