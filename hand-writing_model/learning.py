import torch
import torch.nn as nn

class TinyOCR(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        # 2-layer CNN
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 64x32x128 -> 64x16x64

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2)   # 128x8x32
        )

        self.rnn_hidden = 128
        self.num_classes = num_classes

        # Correct LayerNorm: channels * height after CNN
        self.layer_norm = nn.LayerNorm(128 * 8)  # 1024
        self.rnn = nn.LSTM(
            input_size=128 * 8,  # channels*H after CNN
            hidden_size=self.rnn_hidden,
            num_layers=2,
            bidirectional=True,
            dropout=0.2
        )

        self.fc = nn.Linear(self.rnn_hidden * 2, self.num_classes)

    def forward(self, x):
        x = self.cnn(x)

        B, C, H, W = x.size()

        # Prepare for RNN: (seq_len=W, batch=B, features=C*H)
        x = x.permute(3, 0, 1, 2).contiguous()
        x = x.view(W, B, C * H)

        # LayerNorm along features
        x = self.layer_norm(x)

        x, _ = self.rnn(x)
        x = self.fc(x)

        return x