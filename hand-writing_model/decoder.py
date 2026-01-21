import torch

def ctc_greedy_decode(log_probs, idx2char, blank=0):
    preds = log_probs.argmax(2)  # (T, B)
    texts = []

    for b in range(preds.size(1)):
        prev = blank
        text = ""
        for t in preds[:, b]:
            t = t.item()
            if t != blank and t != prev:
                text += idx2char[t]
            prev = t
        texts.append(text)

    return texts
