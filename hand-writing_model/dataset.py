import torch
from torch.utils.data import Dataset
import pandas as pd
from pathlib import Path

class OCRDataset(Dataset):
    def __init__(self, csv_file, tensor_root):
        self.df = pd.read_csv(csv_file)
        self.tensor_root = tensor_root

        # character set
        chars = sorted(set("".join(self.df["IDENTITY"])))
        self.char2idx = {c: i + 1 for i, c in enumerate(chars)}
        self.char2idx["<blank>"] = 0
        self.idx2char = {i: c for c, i in self.char2idx.items()}
        self.chars = chars

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        # Lazy load: only load when needed
        img = torch.load(self.tensor_root / row["FILENAME"].replace(".jpg", ".pt"))

        label = torch.tensor([self.char2idx[c] for c in row["IDENTITY"]],
                             dtype=torch.long)

        return img, label

