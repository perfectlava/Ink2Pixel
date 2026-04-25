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
    T.Pad((8, 0, 8, 0)),          
    T.ToTensor(),
    T.Normalize((0.5,), (0.5,)),
])

def clean_output(text):
    """strip trailing punctuation only"""
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9]+$', '', text)  
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
    ("testing_images/third.png", "How to improve your handwriting"),
    ("testing_images/fourth.png", "to us human is what water to"),
    ("testing_images/fifth.png", "saying the quickest way to receive love is to give"), 
]

for val, (img_path, gt_text) in enumerate(test_images):
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")
   
print("-------------------------------------------------------------\n")
   
controlled_images = [
    ("controlled_images/first.png", "Edna goes to the ocean"),
    ("controlled_images/second.png", "This is one of the few"),
]

for val, (img_path, gt_text) in enumerate(controlled_images):
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")
   
# ------------------ ACCURACY METRICS ------------------
def levenshtein_distance(s1, s2):
    """Compute edit distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      
                dp[i][j-1] + 1,      
                dp[i-1][j-1] + cost  
            )
    return dp[m][n]

def evaluate_dataset(dataset, name="Dataset"):
    total_chars = 0
    total_errors = 0

    print(f"\nEvaluating {name}...\n")

    for img_path, gt_text in dataset:
        if not os.path.exists(img_path):
            print(f"⚠ Image not found: {img_path}")
            continue

        pr_text = predict_image(img_path)

        gt = clean_output(gt_text.lower())
        pr = clean_output(pr_text.lower())

        dist = levenshtein_distance(gt, pr)

        total_chars += len(gt)
        total_errors += dist

    if total_chars == 0:
        return 0

    accuracy = (total_chars - total_errors) / total_chars

    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Total chars: {total_chars}, Errors: {total_errors}\n")

    return accuracy

# ------------------ RUN EVALUATION ------------------
test_acc = evaluate_dataset(test_images, "Images Collected From The Internet")
controlled_acc = evaluate_dataset(controlled_images, "Handwritten Images From My Notebook")

total_acc = (test_acc + controlled_acc) / 2

print("=====================================================")
print(f"Overall Accuracy: {total_acc * 100:.2f}%")
print("=====================================================")
