# Architecture

The platform is a Flask API plus a React SPA.

- Browser talks only to `/api`.
- JWT access tokens authorize students and administrators.
- ATS, summarization, and RAG live in service modules so providers can change without touching routes.
- PostgreSQL is the system of record. SQLite is accepted for local/tests when `DATABASE_URL` is unset.
- Embeddings prefer Sentence Transformers when installed; otherwise TF-IDF cosine retrieval is used.
- LLM calls (Together / Hugging Face / OpenAI-compatible) are optional. Retrieval still runs if keys are missing.
