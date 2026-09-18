# InnoLearn

**A Seamless Interface for Learning and Technical Innovation**

An original full-stack platform that combines estimated resume–role compatibility, TF-IDF (and optional LLM) summarization, retrieval-augmented document Q&A, educational roadmaps, and a curated resource library.

This is not a clone of a marketing template. The product name, copy, and visual system are original.

## 1. Overview

Students and practitioners get one authenticated workspace for:

- ATS-style **estimated** compatibility scoring (not an employer ATS)
- Line-limited text summarization
- RAG over uploaded PDF / DOCX / TXT
- Domain roadmaps with saved progress
- Searchable, bookmarkable learning resources
- Admin stewardship of roles, resources, roadmaps, and users

## 2. Architecture

Monorepo:

- `frontend/` — React 18, Vite, TypeScript, Tailwind, Motion, React Three Fiber
- `backend/` — Flask blueprints, SQLAlchemy, JWT, NLP/RAG services
- `docs/` — architecture and API notes
- `docker/` — container build files

See `docs/architecture.md`.

## 3. Folder structure

```
frontend/src/{pages,components,services,context,hooks,lib,router,types}
backend/app/{models,routes,services,utils,schemas}
backend/tests
docker/
docs/
```

## 4. Environment setup

Copy `.env.example` to `.env` and replace every `YOUR_*` placeholder. Never commit `.env`.

## 5. PostgreSQL

```sql
CREATE DATABASE seamless_learning;
```

Or run the `postgres` service in `docker-compose.yml` (pgvector image).

Local development can omit `DATABASE_URL`; Flask then uses SQLite at `backend/instance/seamless.db`.

## 6. Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional heavy models:

```powershell
pip install -r requirements-ml.txt
```

## 7. Frontend setup

```powershell
cd frontend
npm install
```

## 8–9. Migrations and seed

```powershell
cd backend
$env:FLASK_APP = "run.py"
python seed_db.py
```

`seed_db.py` runs `db.create_all()` and loads job roles, roadmaps, resources, and an admin user when `ADMIN_EMAIL` and `ADMIN_PASSWORD` are set.

Flask-Migrate:

```powershell
flask --app run:app db init
flask --app run:app db migrate -m "initial"
flask --app run:app db upgrade
```

## 10. Environment variables

See `.env.example`. Required for production: `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`. LLM keys are required only for abstractive summaries and generated RAG answers.

## 11. Run locally

Terminal A:

```powershell
cd backend
python seed_db.py
python run.py
```

Terminal B:

```powershell
cd frontend
npm run dev
```

Open http://localhost:5173. API: http://localhost:5000/api/health

## 12. Docker

```powershell
docker compose up --build
```

Frontend on port 80, API on 5000, Postgres on 5432.

## 13. API documentation

See `docs/api.md`.

## 14. Testing

```powershell
cd backend
pytest -q

cd frontend
npm test
npm run build
```

## 15. Production

- Serve the Flask app with Gunicorn behind TLS.
- Serve the Vite `dist/` from nginx (as in `docker/nginx.conf`).
- Set strong secrets, restrict CORS, configure Postgres backups.
- Provide LLM keys only on the server.

## 16. Troubleshooting

- **401 on API calls:** register/login again; token lives in `localStorage`.
- **LLM_NOT_CONFIGURED:** extractive summarization still works; RAG returns passages without an answer.
- **Unsupported file:** ATS accepts PDF/DOCX; RAG also accepts TXT. 10MB limit.
- **Postgres connection:** check `DATABASE_URL` and that the server is running.
- **spaCy / SentenceTransformers missing:** the app falls back to regex sentence split and TF-IDF retrieval.

## Known limitations

- Abstractive summarization and RAG answers need a live LLM provider key.
- Embedding quality is higher with `requirements-ml.txt`; TF-IDF is the default portable retriever.
- Scores are estimated compatibility, not vendor ATS results.
- Newspaper ingestion described in the academic report is not a live crawl; upload the article instead.
- The frontend template URL was not supplied as a live site; visuals are an original editorial system (ink, bone, chartreuse).
