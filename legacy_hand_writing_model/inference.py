import torch
import re
import string
import os
from PIL import Image
from torchvision import transforms as T

try:
    from .learning import TinyOCR
    from .decoder import ctc_beam_search_decode
except ImportError:
    from learning import TinyOCR
    from decoder import ctc_beam_search_decode


class HandwritingPredictor:
    def __init__(self, checkpoint_path=None, device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        if checkpoint_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            checkpoint_path = os.path.join(current_dir, "checkpoints", "best.pth")
            
        self.checkpoint_path = checkpoint_path
        
        chars = string.ascii_letters + string.digits + string.punctuation + " "
        self.char_to_idx = {c: i + 2 for i, c in enumerate(chars)}
        self.char_to_idx["<blank>"] = 0
        self.char_to_idx["<unk>"] = 1
        self.idx2char = {v: k for k, v in self.char_to_idx.items()}
        
        self.model = TinyOCR(len(self.char_to_idx)).to(self.device)
        self._load_checkpoint()
        self.model.eval()
        
        self.infer_transform = T.Compose([
            T.Grayscale(num_output_channels=1),
            T.Resize((32, 240)),
            T.Pad((8, 0, 8, 0)),         
            T.ToTensor(),
            T.Normalize((0.5,), (0.5,)),
        ])

    def _load_checkpoint(self):
        if not os.path.exists(self.checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found at {self.checkpoint_path}")
            
        checkpoint = torch.load(self.checkpoint_path, map_location=self.device)
        state_dict = checkpoint["model_state"] if "model_state" in checkpoint else checkpoint
        self.model.load_state_dict(state_dict)
        
        if "char_to_idx" in checkpoint:
            self.char_to_idx = checkpoint["char_to_idx"]
            self.idx2char = {v: k for k, v in self.char_to_idx.items()}
        
        print(f"✔ Model loaded from {self.checkpoint_path}")

    @staticmethod
    def clean_output(text):
        text = text.strip()
        text = re.sub(r'[^a-zA-Z0-9]+$', '', text) 
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def predict(self, image, beam_width=5):
        """
        Predict text from an image.
        image: PIL Image or path to image
        """
        if isinstance(image, str):
            img = Image.open(image).convert("L")
        else:
            img = image.convert("L")
        
        img_tensor = self.infer_transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            output = self.model(img_tensor)
            log_probs = output.log_softmax(2)
            logits = log_probs[:, 0, :].cpu()
            
        prediction = ctc_beam_search_decode(logits, self.idx2char, beam_width=beam_width)
        return self.clean_output(prediction)

_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = HandwritingPredictor()
    return _predictor

def predict_handwriting(image_path):
    return get_predictor().predict(image_path)
