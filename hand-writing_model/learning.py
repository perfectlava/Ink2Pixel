import torch
import torch.nn as nn

class TinyOCR(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        # CNN feature extractor
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.cnn_out_channels = 256
        self.cnn_out_height = 8

        self.rnn_hidden = 256
        self.num_classes = num_classes

        self.layer_norm = nn.LayerNorm(self.cnn_out_channels * self.cnn_out_height)

        self.rnn = nn.LSTM(
            input_size=self.cnn_out_channels * self.cnn_out_height,
            hidden_size=self.rnn_hidden,
            num_layers=3,
            bidirectional=True,
            dropout=0.3
        )

        self.fc = nn.Linear(self.rnn_hidden * 2, self.num_classes)

    def forward(self, x):
        x = self.cnn(x)

        B, C, H, W = x.size()

        x = x.permute(3, 0, 1, 2).contiguous()
        x = x.view(W, B, C * H)

        x = self.layer_norm(x)

        x, _ = self.rnn(x)

        x = self.fc(x)

        return x