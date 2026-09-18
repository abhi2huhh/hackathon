from __future__ import annotations

import math
import re
from collections import Counter

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "it", "its", "into", "about", "over", "after",
    "before", "between", "through", "during", "without", "within", "also", "can",
    "will", "would", "should", "could", "may", "might", "must", "shall", "do", "does",
    "did", "have", "has", "had", "not", "no", "nor", "so", "than", "too", "very",
    "just", "than", "then", "there", "here", "when", "where", "which", "who", "whom",
    "your", "you", "we", "our", "they", "their", "them", "he", "she", "his", "her",
}


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z+#.]{1,}", text.lower())


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    text = normalize_text(text)
    if not text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    buffer = ""
    for para in paragraphs:
        if len(buffer) + len(para) + 2 <= max_chars:
            buffer = f"{buffer}\n\n{para}".strip()
        else:
            if buffer:
                chunks.append(buffer)
            if len(para) <= max_chars:
                buffer = para
            else:
                start = 0
                while start < len(para):
                    end = min(start + max_chars, len(para))
                    chunks.append(para[start:end])
                    start = max(end - overlap, end)
                buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks


def cosine_sparse(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b.get(k, 0) for k in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def term_counter(text: str) -> Counter:
    return Counter(t for t in tokenize(text) if t not in STOPWORDS)
