import torch
import torch.nn.functional as F


def _logsumexp(*args):
    m = max(args)
    if m == float('-inf'):
        return float('-inf')
    return m + torch.log(sum(torch.exp(torch.tensor(a - m)) for a in args)).item()

def ctc_greedy_decode(log_probs, idx2char, blank=0):
    """log_probs: (T, B, C). Returns list of strings."""
    indices = log_probs.argmax(dim=2) 
    results = []
    for b in range(indices.shape[1]):
        seq = indices[:, b].tolist()
        decoded, prev = [], None
        for idx in seq:
            if idx != prev:
                if idx != blank:
                    decoded.append(idx2char.get(idx, ""))
            prev = idx
        results.append("".join(decoded))
    return results

def ctc_beam_search_decode(log_probs_1d, idx2char, beam_width=10, blank=0):
    """log_probs_1d: (T, C) single item, already log-softmaxed. Returns string."""
    T, C = log_probs_1d.shape
    NEG_INF = float('-inf')

    beams = {(): [0.0, NEG_INF]}

    for t in range(T):
        new_beams = {}

        def get(prefix):
            if prefix not in new_beams:
                new_beams[prefix] = [NEG_INF, NEG_INF]
            return new_beams[prefix]

        for prefix, (pb, pnb) in beams.items():
            for c in range(C):
                p = log_probs_1d[t, c].item()
                if c == blank:
                    b = get(prefix)
                    b[0] = _logsumexp(b[0], pb + p, pnb + p)
                else:
                    if prefix and prefix[-1] == c:
                        get(prefix + (c,))[1] = _logsumexp(get(prefix + (c,))[1], pb + p)
                        get(prefix)[1] = _logsumexp(get(prefix)[1], pnb + p)
                    else:
                        new_prefix = prefix + (c,)
                        b = get(new_prefix)
                        b[1] = _logsumexp(b[1], pb + p, pnb + p)

        beams = dict(sorted(
            new_beams.items(),
            key=lambda x: _logsumexp(x[1][0], x[1][1]),
            reverse=True
        )[:beam_width])

    best = max(beams.items(), key=lambda x: _logsumexp(x[1][0], x[1][1]))
    return "".join(idx2char.get(c, "") for c in best[0])