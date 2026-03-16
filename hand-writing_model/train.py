import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets import load_dataset
from torchvision import transforms
import time, string
from pathlib import Path

from learning import TinyOCR
from dataset import OCRDataset

torch.backends.cudnn.benchmark = True

def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images)
    label_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)
    labels_concat = torch.cat(labels)
    return images, labels_concat, label_lengths


def main():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    BATCH_SIZE = 32
    EPOCHS = 1
    LR = 3e-4

    CHECKPOINT_DIR = Path("checkpoints")
    CHECKPOINT_DIR.mkdir(exist_ok=True)

    hf_ds = load_dataset("Teklia/IAM-line")
    train_split = hf_ds["train"]

    characters = string.ascii_letters + string.digits + string.punctuation + " "
    char_to_idx = {c: i + 1 for i, c in enumerate(characters)}
    char_to_idx["<blank>"] = 0

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((64, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    dataset = OCRDataset(train_split, char_to_idx, transform)

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=4,
        pin_memory=torch.cuda.is_available()
    )

    model = TinyOCR(len(char_to_idx)).to(DEVICE)
    checkpoint_path = CHECKPOINT_DIR / "best.pth"

    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    scaler = torch.amp.GradScaler(device=DEVICE, enabled=(DEVICE == "cuda"))
    best_loss = float("inf")
    
    if checkpoint_path.exists():
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(checkpoint["model"], strict=True)

        if "optimizer" in checkpoint:
            try:
                optimizer.load_state_dict(checkpoint["optimizer"])
            except Exception:
                print("⚠ Optimizer state not compatible — starting optimizer fresh")
        best_loss = checkpoint.get("best_loss", float("inf"))
        print("✔ Loaded checkpoint")

    print("Training on", len(dataset), "samples")

    for epoch in range(EPOCHS):
        model.train()

        total_loss = 0
        start_time = time.time()

        for batch_idx, (images, labels_concat, target_lengths) in enumerate(loader):
            images = images.to(DEVICE)
            labels_concat = labels_concat.to(DEVICE)
            target_lengths = target_lengths.to(DEVICE)

            optimizer.zero_grad()

            with torch.amp.autocast(device_type=DEVICE, enabled=(DEVICE == "cuda")):
                outputs = model(images)

                log_probs = outputs.log_softmax(2)

                T, B, C = log_probs.shape

                input_lengths = torch.full(
                    (B,),
                    T,
                    dtype=torch.long,
                    device=DEVICE
                )

                loss = criterion(
                    log_probs,
                    labels_concat,
                    input_lengths,
                    target_lengths
                )

            scaler.scale(loss).backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item()

            # if batch_idx % 100 == 0: print(batch_idx)

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch} | Avg Loss {avg_loss:.4f} | Time {(time.time()-start_time)/60:.2f} min")

        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save({
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "best_loss": best_loss,
                "chars": char_to_idx
            }, checkpoint_path)
            print("✔ Saved checkpoint")

    print("✔ Training finished")

if __name__ == "__main__":
    main()