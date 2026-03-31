import torch

def ctc_greedy_decode(log_probs, idx2char, blank=0):
    """
    Greedy CTC decoding for predictions
    log_probs: (T, B, C)
    """
    preds = log_probs.argmax(2)  # (T, B)
    texts = []

    for b in range(preds.size(1)):
        prev = blank
        text = ""
        for t in preds[:, b]:
            t = t.item()
            if t != blank and t != prev:
                text += idx2char.get(t, "")
            prev = t
        texts.append(text)
    return texts