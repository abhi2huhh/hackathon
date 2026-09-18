from __future__ import annotations

import time

import numpy as np
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.text_utils import STOPWORDS


_encoder = None
_encoder_failed = False


def _try_sentence_transformer():
    global _encoder, _encoder_failed
    if _encoder_failed:
        return None
    if _encoder is not None:
        return _encoder
    try:
        from sentence_transformers import SentenceTransformer

        name = current_app.config.get("EMBEDDING_MODEL_NAME")
        _encoder = SentenceTransformer(name, trust_remote_code=True)
        return _encoder
    except Exception:
        _encoder_failed = True
        current_app.logger.info("SentenceTransformer unavailable; using TF-IDF embeddings.")
        return None


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = _try_sentence_transformer()
    if model is not None:
        started = time.perf_counter()
        vectors = model.encode(texts, normalize_embeddings=True)
        current_app.logger.info("embedding_ms=%s count=%s", int((time.perf_counter() - started) * 1000), len(texts))
        return [v.tolist() for v in vectors]
    vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS), max_features=384)
    matrix = vectorizer.fit_transform(texts)
    dense = matrix.toarray().astype(float)
    norms = np.linalg.norm(dense, axis=1, keepdims=True)
    norms[norms == 0] = 1
    dense = dense / norms
    return dense.tolist()


def similarity_search(query: str, chunk_texts: list[str], top_k: int = 4) -> list[tuple[int, float]]:
    if not chunk_texts:
        return []
    model = _try_sentence_transformer()
    if model is not None:
        q = model.encode([query], normalize_embeddings=True)
        docs = model.encode(chunk_texts, normalize_embeddings=True)
        scores = np.dot(docs, q.T).ravel()
    else:
        vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS), max_features=4000)
        matrix = vectorizer.fit_transform(chunk_texts + [query])
        scores = cosine_similarity(matrix[:-1], matrix[-1]).ravel()
    ranked = sorted(enumerate(scores.tolist()), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
