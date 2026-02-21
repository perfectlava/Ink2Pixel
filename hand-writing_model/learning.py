import torch
import torch.nn as nn


class TinyOCR(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.rnn = nn.LSTM(
            input_size=32*16,
            hidden_size=64,
            num_layers=1,
            bidirectional=True,
            batch_first=False  # we will use (T, B, C)
        )
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        # x: (B, 1, H, W)
        x = self.cnn(x)
        B, C, H, W = x.size()          # (B, C, H, W)
        x = x.permute(3, 0, 1, 2)      # (W, B, C, H)
        x = x.contiguous().view(W, B, C * H)  # (T=W, B, C*H)
        x, _ = self.rnn(x)
        x = self.fc(x)                 # (T, B, num_classes)
        return x


