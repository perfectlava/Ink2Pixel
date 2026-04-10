import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms as T
import string, os

from learning import TinyOCR
from dataset import OCRDataset
from decoder import ctc_greedy_decode
from datasets import load_dataset

from randomize import handwriting_transforms

# ---------- Collate function ----------
def collate_fn(batch):
    images, labels, texts = zip(*batch)
    widths = [img.shape[-1] for img in images]
    max_w = max(widths)

    padded = []
    for img in images:
        C, H, W = img.shape
        if W < max_w:
            pad = torch.zeros((C, H, max_w - W), dtype=img.dtype)
            img = torch.cat([img, pad], dim=2)
        padded.append(img)

    images = torch.stack(padded)
    labels_concat = torch.cat(labels)
    label_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)

    return images, labels_concat, label_lengths, texts

# ---------- Main ----------
def main():
    # GPU speedup
    torch.backends.cudnn.benchmark = True

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 16
    EPOCHS = 85
    LR = 1e-4

    os.makedirs("checkpoints", exist_ok=True)
    checkpoint_path = "checkpoints/best.pth"

    # ---------- Dataset ----------
    hf_ds = load_dataset("Teklia/IAM-line")["train"]
    hf_ds = hf_ds.shuffle(seed=42)

    chars = string.ascii_letters + string.digits + string.punctuation + " "
    char_to_idx = {c: i + 2 for i, c in enumerate(chars)}
    char_to_idx["<blank>"] = 0
    char_to_idx["<unk>"] = 1
    idx2char = {v: k for k, v in char_to_idx.items()}

    dataset = OCRDataset(hf_ds, char_to_idx, transform=handwriting_transforms)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE,
                        shuffle=True, collate_fn=collate_fn,
                        num_workers=2, pin_memory=True)

    # ---------- Model ----------
    model = TinyOCR(len(char_to_idx)).to(DEVICE)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    start_epoch = 0

    # ---------- Load checkpoint if exists ----------
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(checkpoint["model_state"])
        optimizer.load_state_dict(checkpoint["optimizer_state"])
        start_epoch = checkpoint.get("epoch", 0)
        char_to_idx = checkpoint.get("char_to_idx", char_to_idx)
        print(f"✔ Loaded checkpoint from epoch {start_epoch}")

    print("Training on", len(dataset), "samples")

    # ---------- Training ----------
    for epoch in range(start_epoch, EPOCHS):
        model.train()
        total_loss = 0

        for batch_idx, (images, labels_concat, target_lengths, texts) in enumerate(loader):
            images = images.to(DEVICE)
            labels_concat = labels_concat.to(DEVICE)
            target_lengths = target_lengths.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(images)
            log_probs = outputs.log_softmax(2)

            T_seq, B, _ = log_probs.shape
            input_lengths = torch.full((B,), T_seq, dtype=torch.long).to(DEVICE)

            loss = criterion(log_probs, labels_concat, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            # decode first batch of epoch for quick monitoring
        if epoch % 5 == 0:
            model.eval()
            with torch.no_grad():
                sample_imgs, _, _, sample_texts = next(iter(loader))
                out = model(sample_imgs[:2].to(DEVICE)).log_softmax(2)
                decoded = ctc_greedy_decode(out.cpu(), idx2char)
                for gt, pr in zip(sample_texts[:2], decoded):
                    print(f"  GT: {gt}")
                    print(f"  PR: {pr}")
            model.train()

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch+1}/{EPOCHS} | Avg Loss: {avg_loss:.4f}")

    # ---------- Save final model ----------
    torch.save({
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "epoch": EPOCHS,
        "char_to_idx": char_to_idx
    }, checkpoint_path)
    print("✔ Training complete and final model saved")

if __name__ == "__main__":
    main()