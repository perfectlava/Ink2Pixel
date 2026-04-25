import torch
from torch.utils.data import Dataset


class OCRDataset(Dataset):
    def __init__(self, hf_dataset, char_to_idx, transform=None):
        self.ds = hf_dataset
        self.char_to_idx = char_to_idx
        self.transform = transform

    def __len__(self):
        return len(self.ds)

    def __getitem__(self, idx):
        sample = self.ds[idx]
        image = sample["image"]
        text = sample["text"] or ""

        if self.transform:
            image = self.transform(image)

        encoded = [self.char_to_idx.get(c, 1) for c in text]
        if len(encoded) == 0:
            encoded = [0]

        label = torch.tensor(encoded, dtype=torch.long)

        return image, label, text