import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathlib import Path
from dataset import OCRDataset
from learning import TinyOCR
from decoder import ctc_greedy_decode  # your decoder function

# ------------------------
# Collate function for DataLoader
# ------------------------
def collate_fn(batch):
    images, labels = zip(*batch)

    # --- IMAGE PADDING ---
    c, h = images[0].shape[0], images[0].shape[1]
    max_w = max(img.shape[2] for img in images)
    padded_images = torch.zeros(len(images), c, h, max_w)
    for i, img in enumerate(images):
        padded_images[i, :, :, :img.shape[2]] = img

    # --- LABELS ---
    target_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)

    return padded_images, list(labels), target_lengths

# ------------------------
# Training Configuration
# ------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATA_ROOT = Path.cwd().parent / "examples" / "output"
CSV_FILE = Path(DATA_ROOT) / "labels.csv"

BATCH_SIZE = 4      # Increase if you have more data and GPU memory
EPOCHS = 50
LR = 1e-3

CHECKPOINT_DIR = Path.cwd().parent / "hand-writing_model" / "checkpoints"
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------
# Dataset & DataLoader
# ------------------------
dataset = OCRDataset(CSV_FILE, DATA_ROOT)
loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=collate_fn
)

# ------------------------
# Model, Loss, Optimizer
# ------------------------
model = TinyOCR(len(dataset.chars)).to(DEVICE)
criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

print("Training on", len(dataset), "samples")

# ------------------------
# Training Loop
# ------------------------
best_loss = float("inf")

for epoch in range(1, EPOCHS + 1):
    total_loss = 0
    model.train()

    for batch_idx, (images, labels_list, target_lengths) in enumerate(loader):
        images = images.to(DEVICE)
        target_lengths = target_lengths.to(DEVICE)  # shape [B]

        # Flatten all labels into 1D tensor
        labels_1d = torch.cat(labels_list).to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)           # (B, T, C) or (T, B, C) depending on TinyOCR

        # Permute to (T, B, C) if needed
        if outputs.shape[0] == BATCH_SIZE:
            outputs = outputs.permute(1, 0, 2)

        log_probs = outputs.log_softmax(2)
        T, B, C = log_probs.shape
        input_lengths = torch.full((B,), T, dtype=torch.long).to(DEVICE)

        # Compute CTC loss
        loss = criterion(log_probs, labels_1d, input_lengths, target_lengths)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(loader)
    print(f"Epoch {epoch:03d} | Loss: {avg_loss:.4f}")

    # ------------------------
    # Optional: decode a sample for quick check
    # ------------------------
    model.eval()
    with torch.no_grad():
        sample_imgs, sample_labels, _ = next(iter(loader))
        sample_imgs = sample_imgs.to(DEVICE)

        preds = model(sample_imgs)
        if preds.shape[0] == BATCH_SIZE:
            preds = preds.permute(1, 0, 2)  # ensure (T, B, C)

        decoded = ctc_greedy_decode(preds, dataset.idx2char)
        gt_text = "".join([dataset.idx2char[i.item()] for i in sample_labels[0]])
        ### print("Sample GT:", gt_text)
        ### print("Sample PR:", decoded[0])
        
        # --- Compute per-character confidence ---
        log_probs = preds.log_softmax(2)  # (T, B, C)
        probs = log_probs.exp()            # convert to probabilities
        sample_probs = probs[0]            # first sample
        top_probs, top_idx = sample_probs.max(1)  # max prob at each timestep
        confidence = top_probs.mean().item()
        ### print(f"Approx. confidence: {confidence*100:.2f}%")

        # --- Compute per-character accuracy ---
        pred_text = decoded[0]
        correct = sum(a==b for a,b in zip(gt_text, pred_text))
        accuracy = correct / len(gt_text)
        ### print(f"Character-level accuracy: {accuracy*100:.2f}%")

    # ------------------------
    # Save checkpoint if best
    # ------------------------
    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save({
            "model": model.state_dict(),
            "chars": dataset.chars
        }, CHECKPOINT_DIR / "best.pth")
        print("✔ Saved checkpoint")
