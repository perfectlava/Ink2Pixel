import torch
from torch.utils.data import Dataset
from torchvision import transforms

class OCRDataset(Dataset):
    def __init__(self, hf_dataset, char_to_idx, transform=None):
        self.ds = hf_dataset
        self.char_to_idx = char_to_idx
        self.transform = transform

        self.idx2char = {v: k for k, v in char_to_idx.items()}

    def encode(self, text):
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