import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets import load_dataset
from torchvision import transforms
import time, string, os

from learning import TinyOCR
from dataset import OCRDataset
from decoder import ctc_greedy_decode


# ---------- Collate Function (CLEANED) ----------
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
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 32   # 🔥 Increased for GPU throughput
    EPOCHS = 11
    LR = 3e-4

    checkpoint_path = "checkpoints/best.pth"

    torch.backends.cudnn.benchmark = True  # 🔥 autotune

    # ---------- Dataset ----------
    hf_ds = load_dataset("Teklia/IAM-line")
    train_split = hf_ds["train"]

    characters = string.ascii_letters + string.digits + string.punctuation + " "
    char_to_idx = {c: i + 2 for i, c in enumerate(characters)}
    char_to_idx["<blank>"] = 0
    char_to_idx["<unk>"] = 1
    idx2char = {v: k for k, v in char_to_idx.items()}

    # ---------- Transform ----------
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(32),
        transforms.ToTensor(),  # convert FIRST
        transforms.Lambda(lambda x: x[:, :, :512] if x.shape[-1] > 512 else x),  # cap width
        transforms.Normalize((0.5,), (0.5,))
    ])

    dataset = OCRDataset(train_split, char_to_idx, transform)

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=2,   # 🔥 prevent freezing
        pin_memory=True
    )

    # ---------- Model ----------
    model = TinyOCR(len(char_to_idx)).to(DEVICE)

    # 🔥 LSTM smaller/faster
    # In learning.py:
    # self.rnn = nn.LSTM(input_size=128*8, hidden_size=64, num_layers=1, bidirectional=True)

    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    # ---------- Load checkpoint ----------
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
        model.load_state_dict(checkpoint["model"], strict=False)
        print("✔ Loaded checkpoint")

    print("Training on", len(dataset), "samples")

    # ---------- Training ----------
    scaler = torch.cuda.amp.GradScaler()  # 🔥 mixed precision

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        start_time = time.time()

        for batch_idx, (images, labels_concat, target_lengths, texts) in enumerate(loader):
            images = images.to(DEVICE)
            labels_concat = labels_concat.to(DEVICE)
            target_lengths = target_lengths.to(DEVICE)

            optimizer.zero_grad()

            # 🔥 Mixed precision
            with torch.cuda.amp.autocast():
                outputs = model(images)
                log_probs = outputs.log_softmax(2)

                T, B, C = log_probs.shape
                input_lengths = torch.full((B,), T, dtype=torch.long, device=DEVICE)

                loss = criterion(log_probs, labels_concat, input_lengths, target_lengths)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item()

            # ---------- DEBUG ----------
            if batch_idx % 200 == 0:
                decoded = ctc_greedy_decode(log_probs.detach(), idx2char)
                preds = log_probs.argmax(2)
                blank_ratio = (preds == 0).float().mean().item()

                print("\n--- DEBUG ---")
                print("GT :", texts[0])
                print("PR :", decoded[0])
                print("Blank ratio:", blank_ratio)
                print("----------------")

            # 🔥 Batch speed logging
            if batch_idx % 50 == 0:
                print(f"Batch {batch_idx} | Loss: {loss.item():.4f}")

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch} | Avg Loss {avg_loss:.4f} | Time {(time.time()-start_time)/60:.2f} min")

    print("✔ Training finished")


if __name__ == "__main__":
    main()