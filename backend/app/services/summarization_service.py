from __future__ import annotations

import math
import time

from flask import current_app

from app.utils.error_handlers import APIError
from app.utils.text_utils import STOPWORDS, split_sentences, tokenize


def frequency_matrix(sentences: list[str]) -> dict[int, dict[str, int]]:
    matrix = {}
    for i, sent in enumerate(sentences):
        table: dict[str, int] = {}
        for word in tokenize(sent):
            if word in STOPWORDS:
                continue
            table[word] = table.get(word, 0) + 1
        matrix[i] = table
    return matrix


def calculate_tf_matrix(freq_matrix):
    return {
        sent: {word: count / max(sum(freq_table.values()), 1) for word, count in freq_table.items()}
        for sent, freq_table in freq_matrix.items()
    }


def sentences_per_words(freq_matrix):
    counts: dict[str, int] = {}
    for freq_table in freq_matrix.values():
        for word in freq_table:
            counts[word] = counts.get(word, 0) + 1
    return counts


def calculate_idf_matrix(freq_matrix, word_sentence_count, total_sentences):
    return {
        sent: {
            word: math.log10(total_sentences / (1 + word_sentence_count[word]))
            for word in freq_table
        }
        for sent, freq_table in freq_matrix.items()
    }


def calculate_tf_idf_matrix(tf_matrix, idf_matrix):
    return {
        sent: {word: tf_val * idf_matrix[sent].get(word, 0) for word, tf_val in tf_table.items()}
        for sent, tf_table in tf_matrix.items()
    }


def score_sentences(tf_idf_matrix):
    return {
        sent: (sum(word_scores.values()) / len(word_scores) if word_scores else 0)
        for sent, word_scores in tf_idf_matrix.items()
    }


def extractive_summary(text: str, num_sentences: int) -> str:
    sentences = split_sentences(text)
    if not sentences:
        raise APIError("VALIDATION_ERROR", "The provided text is empty.", 400)
    if len(sentences) <= num_sentences:
        return " ".join(sentences)
    freq = frequency_matrix(sentences)
    tf = calculate_tf_matrix(freq)
    df = sentences_per_words(freq)
    idf = calculate_idf_matrix(freq, df, len(sentences))
    tfidf = calculate_tf_idf_matrix(tf, idf)
    scores = score_sentences(tfidf)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    ranked = sorted(ranked, key=lambda x: x[0])
    return " ".join(sentences[i] for i, _ in ranked)


def abstractive_summary(text: str, num_sentences: int) -> str:
    from app.services.llm_service import LLMNotConfigured, generate_completion

    prompt = (
        "Summarize the following text in exactly "
        f"{num_sentences} concise sentences. Preserve key facts. Do not invent details.\n\n{text[:8000]}"
    )
    try:
        started = time.perf_counter()
        output = generate_completion(prompt, max_tokens=min(80 * num_sentences, 700))
        current_app.logger.info("abstractive_summary_ms=%s", int((time.perf_counter() - started) * 1000))
        return output.strip()
    except LLMNotConfigured:
        raise
    except Exception as exc:
        raise APIError("AI_PROVIDER_UNAVAILABLE", f"Abstractive summarization failed: {exc}", 503) from exc


def summarize(text: str, line_count: int, method: str = "extractive") -> dict:
    method = (method or "extractive").lower()
    if method not in {"extractive", "abstractive"}:
        raise APIError("VALIDATION_ERROR", "method must be extractive or abstractive.", 400)
    if method == "extractive":
        summary = extractive_summary(text, line_count)
    else:
        summary = abstractive_summary(text, line_count)
    lines = [ln for ln in summary.splitlines() if ln.strip()] or [summary]
    return {
        "summary": summary,
        "line_count": min(line_count, len(split_sentences(summary)) or line_count),
        "method": method,
        "original_length": len(text),
        "summary_length": len(summary),
        "paragraphs": lines,
    }
