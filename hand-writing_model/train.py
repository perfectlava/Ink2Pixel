import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathlib import Path
from dataset import OCRDataset
from learning import TinyOCR

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
    # labels are not padded; keep them as individual tensors
    target_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)

    return padded_images, labels, target_lengths


# ------------------------
# Training Loop
# ------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATA_ROOT = Path.cwd().parent / "examples" / "output"
CSV_FILE = Path(DATA_ROOT) / "labels.csv"

BATCH_SIZE = 1  # small dataset
EPOCHS = 50
LR = 1e-3

# Dataset and loader
dataset = OCRDataset(CSV_FILE, DATA_ROOT)
loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=collate_fn
)

# Model, loss, optimizer
model = TinyOCR(len(dataset.chars)).to(DEVICE)
criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

print("Training on", len(dataset), "samples")

for epoch in range(EPOCHS):
    total_loss = 0

    for batch_idx, (images, labels_list, target_lengths) in enumerate(loader):
        images = images.to(DEVICE)
        target_lengths = target_lengths.to(DEVICE)

        # Flatten all labels into a single 1D tensor
        labels_1d = torch.cat(labels_list).to(DEVICE)

        optimizer.zero_grad()

        # --- Forward pass ---
        outputs = model(images)  # Assume output shape is (T, B, C)
        log_probs = outputs.log_softmax(2)

        T, B, C = log_probs.shape
        batch_size = B
        seq_len = T

        # --- Input lengths for each sample in batch ---
        input_lengths = torch.full(
            size=(batch_size,),   # B
            fill_value=seq_len,   # T
            dtype=torch.long
        ).to(DEVICE)

        # --- Compute CTC loss ---
        loss = criterion(
            log_probs,
            labels_1d,
            input_lengths,
            target_lengths
        )

        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1:03d} | Loss: {total_loss:.4f}")
