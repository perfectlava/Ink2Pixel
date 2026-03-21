import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets import load_dataset
from torchvision import transforms
import time, string
from pathlib import Path

from learning import TinyOCR
from dataset import OCRDataset
from decoder import ctc_greedy_decode

# ---------- Collate Function ----------
def collate_fn(batch):
    images, labels, texts = zip(*batch)

    images = torch.stack(images)
    label_lengths = torch.tensor([len(l) for l in labels], dtype=torch.long)
    labels_concat = torch.cat(labels)

    return images, labels_concat, label_lengths, texts


# ---------- Main ----------
def main():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 16
    EPOCHS = 10
    LR = 3e-4

    CHECKPOINT_DIR = Path("checkpoints")
    CHECKPOINT_DIR.mkdir(exist_ok=True)

    # ---------- Dataset ----------
    hf_ds = load_dataset("Teklia/IAM-line")
    train_split = hf_ds["train"]

    characters = string.ascii_letters + string.digits + string.punctuation + " "

    # 🔴 FIXED VOCAB
    char_to_idx = {c: i + 2 for i, c in enumerate(characters)}
    char_to_idx["<blank>"] = 0
    char_to_idx["<unk>"] = 1

    idx2char = {v: k for k, v in char_to_idx.items()}

    # ---------- Transform ----------
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((32, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    dataset = OCRDataset(train_split, char_to_idx, transform)

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=2,
        pin_memory=torch.cuda.is_available()
    )

    # ---------- Model ----------
    model = TinyOCR(len(char_to_idx)).to(DEVICE)

    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    print("Training on", len(dataset), "samples")

    # ---------- Training ----------
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        start_time = time.time()

        for batch_idx, (images, labels_concat, target_lengths, texts) in enumerate(loader):
            images = images.to(DEVICE)
            labels_concat = labels_concat.to(DEVICE)
            target_lengths = target_lengths.to(DEVICE)

            optimizer.zero_grad()

            outputs = model(images)
            log_probs = outputs.log_softmax(2)

            T, B, C = log_probs.shape
            input_lengths = torch.full((B,), T, dtype=torch.long, device=DEVICE)

            loss = criterion(log_probs, labels_concat, input_lengths, target_lengths)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()

            total_loss += loss.item()

            # 🔍 DEBUG (VERY IMPORTANT)
            if batch_idx % 200 == 0:
                decoded = ctc_greedy_decode(log_probs.detach(), idx2char)

                print("\n--- DEBUG ---")
                print("GT :", texts[0])
                print("PR :", decoded[0])
                preds = log_probs.argmax(2)
                blank_ratio = (preds == 0).float().mean().item()
                print("Blank ratio:", blank_ratio)
                print("----------------")

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch} | Avg Loss {avg_loss:.4f} | Time {(time.time()-start_time)/60:.2f} min")

    print("✔ Training finished")


if __name__ == "__main__":
    main()