import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathlib import Path
from dataset import OCRDataset
from learning import TinyOCR
from decoder import ctc_greedy_decode  # your decoder function
import time

# ------------------------
# Collate function for DataLoader
# ------------------------
def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images)  # (B, 1, H, W)
    target_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)
    return images, labels, target_lengths

def main():
    # ------------------------
    # Training Configuration
    # ------------------------
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    DATA_ROOT = Path.cwd().parent.parent / "Dataset - Handwriting model" / "train_10k_images_processed"
    CSV_FILE = Path(DATA_ROOT.parent / "train_10k.csv")

    BATCH_SIZE = 16      # Increase if you have more data and GPU memory
    EPOCHS = 1
    LR = 1e-3

    CHECKPOINT_DIR = Path.cwd().parent / "hand-writing_model" / "checkpoints"
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------
    # Dataset & DataLoader
    # ------------------------
    dataset = OCRDataset(CSV_FILE, DATA_ROOT)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, 
                        shuffle=True, 
                        collate_fn=collate_fn, 
                        num_workers=1,
                        pin_memory=torch.cuda.is_available()) 

    # ------------------------
    # Model, Loss, Optimizer
    # ------------------------
    model = TinyOCR(len(dataset.chars)).to(DEVICE)

    # Load previous checkpoint if it exists
    checkpoint_path = CHECKPOINT_DIR / "best.pth"
    if checkpoint_path.exists():
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(checkpoint["model"])
        print("✔ Loaded checkpoint")

    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    print("Training on", len(dataset), "samples")

    # ------------------------
    # Training Loop
    # ------------------------
    best_loss = float("inf")
    for epoch in range(EPOCHS):
        start_time = time.time()
        model.train()
        total_loss = 0
        
        for batch_idx, (images, labels_list, target_lengths) in enumerate(loader):
            images = images.to(DEVICE, non_blocking=True)
            target_lengths = target_lengths.to(DEVICE, non_blocking=True)
            labels_1d = torch.cat(labels_list).to(DEVICE, non_blocking=True)

            optimizer.zero_grad()
            outputs = model(images)               # (T, B, C)
            log_probs = outputs.log_softmax(2)

            T, B, C = log_probs.shape
            input_lengths = torch.full((B,), T, dtype=torch.long, device=DEVICE)

            loss = criterion(log_probs, labels_1d, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            if batch_idx % 100 == 0:
                print(f"Epoch {epoch} | Batch {batch_idx} | Loss: {loss.item():.4f}")

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch} | Avg Loss: {avg_loss:.4f} | Time: {(time.time() - start_time)/60} min")
        
    print("✔ Training loop finished")

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
        
        # --- Compute per-character confidence ---
        log_probs = preds.log_softmax(2)  # (T, B, C)
        probs = log_probs.exp()            # convert to probabilities
        sample_probs = probs[0]            # first sample
        top_probs, top_idx = sample_probs.max(1)  # max prob at each timestep
        confidence = top_probs.mean().item()

        # --- Compute per-character accuracy ---
        pred_text = decoded[0]
        correct = sum(a==b for a,b in zip(gt_text, pred_text))
        accuracy = correct / len(gt_text)

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

    print("successful")
    
if __name__ == "__main__":
    main()