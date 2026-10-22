import json
from pathlib import Path

import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL, INDEX_DIR
from .ingest import make_chunks


def build_index():
    chunks = make_chunks()
    if not chunks:
        raise RuntimeError("No readable PDF text found under data/.")
    model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
    vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    dense = faiss.IndexFlatIP(vectors.shape[1])
    dense.add(vectors)
    INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(dense, str(INDEX_DIR / "dense.faiss"))
    (INDEX_DIR / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    (INDEX_DIR / "bm25.json").write_text(json.dumps([[w.lower() for w in c["text"].split()] for c in chunks]), encoding="utf-8")
    return len(chunks)


def load_index():
    chunks = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    dense = faiss.read_index(str(INDEX_DIR / "dense.faiss"))
    tokenized = json.loads((INDEX_DIR / "bm25.json").read_text(encoding="utf-8"))
    model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
    return chunks, dense, BM25Okapi(tokenized), model
