import torch
from torch.utils.data import Dataset

class OCRDataset(Dataset):
    def __init__(self, hf_dataset, char_to_idx, transform=None):
        self.ds = hf_dataset
        self.char_to_idx = char_to_idx
        self.transform = transform

    def encode(self, text):
        if text is None or len(text) == 0:
            return torch.tensor([0], dtype=torch.long)

        return torch.tensor(
            [self.char_to_idx.get(c, 0) for c in text],
            dtype=torch.long
        )

    def __len__(self):
        return len(self.ds)

    def __getitem__(self, idx):
        sample = self.ds[idx]
        image = sample["image"]
        text = sample["text"]

        if self.transform:
            image = self.transform(image)

        label = self.encode(text)

        return image, label