from .config import BM25_MIN_SCORE, SIM_THRESHOLD, TOP_BM25, TOP_DENSE, TOP_K


import re as _re

_SCHEME_PATTERNS = {
    "PM-KISAN": r"kisan|pm-?kisan",
    "PM-JAY": r"pm-?jay|ayushman|ab-?pmjay|health cover|empanel",
    "Post-Matric Scholarship (SC)": r"scholarship|post-?\s?matric",
}


def detect_scheme(query):
    """Return a scheme name only if the question clearly mentions exactly one scheme."""
    q = query.lower()
    hits = [name for name, pat in _SCHEME_PATTERNS.items() if _re.search(pat, q)]
    return hits[0] if len(hits) == 1 else None


def retrieve(query, chunks, dense, bm25, model, scheme=None):
    if scheme is None:
        scheme = detect_scheme(query)
    qv = model.encode([query], normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    # Search the full corpus so a scheme filter can be applied without hiding
    # relevant passages that sit below the global top ten.
    scores, ids = dense.search(qv, len(chunks))
    dense_scores = {int(i): float(s) for i, s in zip(ids[0], scores[0]) if i >= 0}
    keyword_scores = bm25.get_scores(query.lower().split())
    candidates = [i for i, c in enumerate(chunks) if not scheme or c["scheme"] == scheme]
    dr = sorted(candidates, key=lambda i: dense_scores.get(i, -1), reverse=True)[:TOP_DENSE]
    br = sorted(candidates, key=lambda i: keyword_scores[i], reverse=True)[:TOP_BM25]
    fused = {}
    for rank, i in enumerate(dr, 1): fused[i] = fused.get(i, 0) + 1 / (60 + rank)
    for rank, i in enumerate(br, 1): fused[i] = fused.get(i, 0) + 1 / (60 + rank)
    best_bm = max((keyword_scores[i] for i in candidates), default=0)
    confidence = max((dense_scores.get(i, 0) for i in candidates), default=0)
    if confidence < SIM_THRESHOLD and best_bm < BM25_MIN_SCORE:
        return [], confidence, True
    results = [{**chunks[i], "dense_score": dense_scores.get(i, 0), "bm25_score": float(keyword_scores[i]), "rrf_score": fused[i]} for i in sorted(fused, key=fused.get, reverse=True)[:TOP_K]]
    return results, confidence, False
