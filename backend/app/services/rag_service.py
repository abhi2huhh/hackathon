from __future__ import annotations

from app.extensions import db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import embed_texts, similarity_search
from app.services.llm_service import LLMNotConfigured, generate_answer
from app.services.resume_parser import extract_text
from app.utils.error_handlers import APIError
from app.utils.text_utils import chunk_text, normalize_text


def ingest_document(user_id: int, title: str, original: str, stored: str, path: str, file_type: str) -> Document:
    text = extract_text(path, original)
    chunks = chunk_text(text)
    if not chunks:
        raise APIError("INVALID_DOCUMENT", "The document did not contain enough text to index.", 400)
    embeddings = embed_texts(chunks)
    document = Document(
        user_id=user_id,
        title=title or original,
        original_filename=original,
        stored_filename=stored,
        file_type=file_type,
        char_count=len(text),
    )
    db.session.add(document)
    db.session.flush()
    for index, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        db.session.add(
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                text=chunk,
                embedding=vector,
            )
        )
    return document


def query_document(document: Document, question: str, top_k: int = 4) -> dict:
    question = normalize_text(question)
    if not question:
        raise APIError("VALIDATION_ERROR", "A question is required.", 400)
    chunks = document.chunks.order_by(DocumentChunk.chunk_index.asc()).all()
    if not chunks:
        raise APIError("NOT_FOUND", "This document has no indexed passages.", 404)
    texts = [c.text for c in chunks]
    ranked = similarity_search(question, texts, top_k=top_k)
    retrieved = []
    for idx, score in ranked:
        retrieved.append(
            {
                "chunk_index": chunks[idx].chunk_index,
                "text": chunks[idx].text,
                "score": round(float(score), 4),
            }
        )
    context = "\n\n".join(item["text"][:1200] for item in retrieved)
    confidence = round(min(0.99, max(0.0, ranked[0][1] if ranked else 0)), 3)
    llm_configured = True
    try:
        answer = generate_answer(context, question)
    except LLMNotConfigured:
        llm_configured = False
        answer = None
    return {
        "answer": answer,
        "llm_configured": llm_configured,
        "sources": [
            {"chunk_index": item["chunk_index"], "score": item["score"]}
            for item in retrieved
        ],
        "confidence": confidence,
        "retrieved_chunks": retrieved,
        "message": None
        if llm_configured
        else "Retrieved relevant passages, but no LLM API key is configured so an answer was not generated.",
    }
