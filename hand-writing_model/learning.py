import torch
import torch.nn as nn

class TinyOCR(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.rnn_hidden = 128
        self.num_classes = num_classes

        # Correct LayerNorm
        self.layer_norm = nn.LayerNorm(128 * 8)

        self.rnn = nn.LSTM(
            input_size=128 * 8,
            hidden_size=self.rnn_hidden,
            num_layers=2,
            bidirectional=True,
            dropout=0.2
        )

        self.fc = nn.Linear(self.rnn_hidden * 2, self.num_classes)

    def forward(self, x):
        x = self.cnn(x)

        B, C, H, W = x.size()

        x = x.permute(3, 0, 1, 2)
        x = x.contiguous().view(W, B, C * H)

        x = self.layer_norm(x)

        x, _ = self.rnn(x)
        x = self.fc(x)

        return x