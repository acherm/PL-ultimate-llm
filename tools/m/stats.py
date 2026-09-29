"""Small, dependency-free estimators used by the `.m` analysis.

  wilson(k, n)                     95% Wilson interval for a simple random sample
  weighted_prop(xs, ws)            Hájek estimate + CI using Kish's effective n
  ppi_prop(gold, pred_l, pred_u)   prediction-powered inference (Angelopoulos
                                   et al., Science 2023) for a class proportion
  cohen_kappa(a, b)                chance-corrected agreement
  dawid_skene(items, labellers)    EM estimate of each labeller's confusion
                                   matrix with no gold standard (Dawid & Skene 1979)
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

Z = 1.959964


def wilson(k: int, n: int, z: float = Z) -> tuple[float, float, float]:
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def weighted_prop(xs: list[int], ws: list[float], z: float = Z) -> tuple[float, float, float, float]:
    """Return (p, lo, hi, n_eff). xs are 0/1 indicators, ws sampling weights."""
    sw = sum(ws)
    if sw == 0:
        return (float("nan"),) * 4
    p = sum(x * w for x, w in zip(xs, ws)) / sw
    n_eff = sw * sw / sum(w * w for w in ws)
    lo, hi = wilson(round(p * n_eff), max(1, round(n_eff)))[1:]
    return p, lo, hi, n_eff


def ppi_prop(gold: list[int], pred_l: list[int], pred_u: list[int], z: float = Z):
    """PPI point estimate and CI for P(Y=1).

    gold / pred_l : gold label and cheap prediction on the n labelled items
    pred_u        : cheap prediction on the N unlabelled items (same population)
    θ = mean(pred_u) + mean(gold − pred_l)       (the "rectifier")
    """
    n, N = len(gold), len(pred_u)
    if n == 0 or N == 0:
        return (float("nan"),) * 3
    m_u = sum(pred_u) / N
    rect = [g - f for g, f in zip(gold, pred_l)]
    m_r = sum(rect) / n
    v_u = sum((x - m_u) ** 2 for x in pred_u) / max(N - 1, 1)
    v_r = sum((x - m_r) ** 2 for x in rect) / max(n - 1, 1)
    theta = m_u + m_r
    se = math.sqrt(v_u / N + v_r / n)
    return theta, max(0.0, theta - z * se), min(1.0, theta + z * se)


def ppi_pp_prop(gold: list[int], pred_l: list[int], pred_u: list[int], z: float = Z):
    """Power-tuned PPI ("PPI++", Angelopoulos, Duchi & Zrnic 2023) for P(Y=1).

    θ = mean(gold) + λ·(mean(pred_u) − mean(pred_l)), with the variance-minimising
    λ = Cov(Y, f) / ((1 + n/N)·Var(f)), clipped to [0, 1]. λ = 0 is the classical
    estimate, λ = 1 plain PPI — so PPI++ is never (asymptotically) worse than
    classical, which matters when the unlabelled pool is not ≫ the labelled set.
    Returns (θ, lo, hi, λ, classical_wald_width, ppi_width).
    """
    n, N = len(gold), len(pred_u)
    if n < 2 or N < 2:
        return (float("nan"),) * 6
    my, mfl, mfu = sum(gold) / n, sum(pred_l) / n, sum(pred_u) / N
    cov = sum((y - my) * (f - mfl) for y, f in zip(gold, pred_l)) / (n - 1)
    fa = pred_l + pred_u
    mfa = sum(fa) / len(fa)
    vf = sum((f - mfa) ** 2 for f in fa) / (len(fa) - 1)
    lam = 0.0 if vf == 0 else max(0.0, min(1.0, cov / ((1 + n / N) * vf)))
    theta = my + lam * (mfu - mfl)
    vfu = sum((f - mfu) ** 2 for f in pred_u) / (N - 1)
    rect = [y - lam * f for y, f in zip(gold, pred_l)]
    mr = sum(rect) / n
    vr = sum((x - mr) ** 2 for x in rect) / (n - 1)
    se = math.sqrt(lam * lam * vfu / N + vr / n)
    classical_w = 2 * z * math.sqrt(my * (1 - my) / n)
    return theta, max(0.0, theta - z * se), min(1.0, theta + z * se), lam, classical_w, 2 * z * se


def classical_ci_width(k: int, n: int) -> float:
    _, lo, hi = wilson(k, n)
    return hi - lo


def cohen_kappa(a: list, b: list) -> float:
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def dawid_skene(items: dict[str, dict[str, str]], classes: list[str], iters: int = 50):
    """items: {item_id: {labeller: label}}. Returns (posteriors, confusion, priors).

    Assumes labellers err independently given the true class — flagged in the
    report because several of ours share heuristics (Synid ⊃ Linguist rules).
    """
    labellers = sorted({l for d in items.values() for l in d})
    K = len(classes)
    idx = {c: i for i, c in enumerate(classes)}
    # init posteriors by majority vote
    post = {}
    for it, d in items.items():
        v = [0.0] * K
        for lab in d.values():
            if lab in idx:
                v[idx[lab]] += 1
        s = sum(v) or 1
        post[it] = [x / s if sum(v) else 1 / K for x in v]
    conf = {}
    prior = [1 / K] * K
    for _ in range(iters):
        # M-step
        prior = [sum(p[k] for p in post.values()) / len(post) for k in range(K)]
        conf = {}
        for lab in labellers:
            m = [[0.01] * K for _ in range(K)]  # smoothing
            for it, d in items.items():
                if lab in d and d[lab] in idx:
                    for k in range(K):
                        m[k][idx[d[lab]]] += post[it][k]
            conf[lab] = [[x / sum(row) for x in row] for row in m]
        # E-step
        for it, d in items.items():
            v = [math.log(max(prior[k], 1e-12)) for k in range(K)]
            for lab, l in d.items():
                if l in idx:
                    for k in range(K):
                        v[k] += math.log(conf[lab][k][idx[l]])
            mx = max(v)
            e = [math.exp(x - mx) for x in v]
            s = sum(e)
            post[it] = [x / s for x in e]
    return post, conf, prior


def ds_accuracy(conf: dict, prior: list[float]) -> dict[str, float]:
    """Prior-weighted accuracy of each labeller from its DS confusion matrix."""
    return {lab: sum(prior[k] * m[k][k] for k in range(len(prior))) for lab, m in conf.items()}


def pairwise(recs, labellers, key):
    """Pairwise agreement & kappa over items where both labellers answered."""
    out = defaultdict(dict)
    for a in labellers:
        for b in labellers:
            xs = [(key(r, a), key(r, b)) for r in recs]
            xs = [(x, y) for x, y in xs if x is not None and y is not None]
            if not xs:
                continue
            A, B = zip(*xs)
            out[a][b] = {"n": len(xs), "agree": sum(x == y for x, y in xs) / len(xs),
                         "kappa": cohen_kappa(list(A), list(B))}
    return out
