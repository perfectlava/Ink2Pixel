import torch
from torch.utils.data import Dataset


class OCRDataset(Dataset):
    def __init__(self, hf_dataset, char_to_idx, transform=None):
        self.ds = hf_dataset
        self.char_to_idx = char_to_idx
        self.transform = transform

        # 🔥 Pre-encode ALL labels once
        self.encoded_labels = []
        self.texts = []

        for sample in self.ds:
            text = sample["text"] or ""
            self.texts.append(text)

            # Encode characters
            encoded = [self.char_to_idx.get(c, 1) for c in text]  # 1 = <unk>
            if len(encoded) == 0:
                encoded = [0]  # blank if empty

            self.encoded_labels.append(torch.tensor(encoded, dtype=torch.long))

    def __len__(self):
        return len(self.ds)

    def __getitem__(self, idx):
        sample = self.ds[idx]
        image = sample["image"]

        if self.transform:
            image = self.transform(image)

        label = self.encoded_labels[idx]
        text = self.texts[idx]

        return image, label, text