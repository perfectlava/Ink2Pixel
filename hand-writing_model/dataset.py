import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import torchvision.transforms as T

class OCRDataset(Dataset):
    def __init__(self, csv_file, root_dir):
        self.data = pd.read_csv(csv_file)
        self.root = root_dir
        self.transform = self.transform = T.Compose([
            T.Grayscale(),
            T.Resize(32),
            T.ToTensor(),          # converts PIL → Tensor [0,1]
        ])

        chars = set("".join(self.data["text"]))
        self.chars = ["<blank>"] + sorted(chars)
        self.char2idx = {c: i for i, c in enumerate(self.chars)}
        self.idx2char = {i: c for c, i in self.char2idx.items()}

    def __len__(self):
        return len(self.data)

    def encode(self, text):
        return torch.tensor(
            [self.char2idx[c] for c in text],
            dtype=torch.long
        )

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        img_path = self.root / row["image_path"]
        image = Image.open(img_path)
        image = self.transform(image)

        label = self.encode(row["text"])
        return image, label
