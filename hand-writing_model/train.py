import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets import load_dataset
from torchvision import transforms
import time, string, os

from learning import TinyOCR
from dataset import OCRDataset
from decoder import ctc_greedy_decode

# ---------- Collate Function ----------
def collate_fn(batch):
    images, labels, texts = zip(*batch)
    widths = [img.shape[-1] for img in images]
    max_w = max(widths)

    padded_images = []
    for img in images:
        C, H, W = img.shape
        pad_w = max_w - W
        if pad_w > 0:
            pad = torch.zeros((C, H, pad_w))
            img = torch.cat([img, pad], dim=2)
        padded_images.append(img)

    images = torch.stack(padded_images)
    label_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)
    labels_concat = torch.cat(labels)

    return images, labels_concat, label_lengths, texts

# ---------- Main ----------
def main():
    use_cuda = torch.cuda.is_available()
    DEVICE = "cuda" if use_cuda else "cpu"
    BATCH_SIZE = 32
    EPOCHS = 4
    LR = 3e-4
    checkpoint_path = "checkpoints/best.pth"
    os.makedirs("checkpoints", exist_ok=True)
    torch.backends.cudnn.benchmark = True

    # ---------- Dataset ----------
    hf_ds = load_dataset("Teklia/IAM-line")
    train_split = hf_ds["train"]

    characters = string.ascii_letters + string.digits + string.punctuation + " "
    char_to_idx = {c: i + 2 for i, c in enumerate(characters)}
    char_to_idx["<blank>"] = 0
    char_to_idx["<unk>"] = 1
    idx2char = {v: k for k, v in char_to_idx.items()}

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(32),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x[:, :, :512] if x.shape[-1] > 512 else x),
        transforms.Normalize((0.5,), (0.5,))
    ])

    dataset = OCRDataset(train_split, char_to_idx, transform)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True,
                        collate_fn=collate_fn, num_workers=0, pin_memory=True)

    # ---------- Model ----------
    model = TinyOCR(len(char_to_idx)).to(DEVICE)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    scaler = torch.amp.GradScaler(enabled=use_cuda)

    # ---------- Load checkpoint ----------
    best_loss = float("inf")
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(checkpoint["model"], strict=True)
        if "optimizer" in checkpoint:
            try:
                optimizer.load_state_dict(checkpoint["optimizer"])
            except Exception:
                print("⚠ Optimizer state not compatible — starting optimizer fresh")
        if "scaler" in checkpoint:
            scaler.load_state_dict(checkpoint["scaler"])
        best_loss = checkpoint.get("best_loss", float("inf"))
        char_to_idx = checkpoint.get("char_to_idx", char_to_idx)
        print("✔ Loaded checkpoint")

    print("Training on", len(dataset), "samples")

    # ---------- Training ----------
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        start_time = time.time()
        scaler = torch.amp.GradScaler(enabled=use_cuda)

        for batch_idx, (images, labels_concat, target_lengths, texts) in enumerate(loader):
            images, labels_concat, target_lengths = images.to(DEVICE), labels_concat.to(DEVICE), target_lengths.to(DEVICE)
            optimizer.zero_grad()
            device_type = "cuda" if use_cuda else "cpu"

            with torch.amp.autocast(device_type=device_type, enabled=use_cuda):
                outputs = model(images)
                log_probs = outputs.log_softmax(2)
                T, B, C = log_probs.shape
                input_lengths = torch.full((B,), T, dtype=torch.long, device=DEVICE)
                loss = criterion(log_probs, labels_concat, input_lengths, target_lengths)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            total_loss += loss.item()

            # if batch_idx % 200 == 0:
            #     decoded = ctc_greedy_decode(log_probs.detach(), idx2char)
            #     print("\n--- DEBUG ---")
            #     print("GT :", texts[0])
            #     print("PR :", decoded[0])
            #     print("----------------")

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch} | Avg Loss {avg_loss:.4f} | Time {(time.time()-start_time)/60:.2f} min")

        # ---------- Checkpoint ----------
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save({
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "scaler": scaler.state_dict(),
                "best_loss": best_loss,
                "char_to_idx": char_to_idx
            }, checkpoint_path)
            print(f"✔ Saved checkpoint (best_loss: {best_loss:.4f})")

    print("✔ Training finished")

if __name__ == "__main__":
    main()