# API

All responses:

```json
{ "success": true, "data": {}, "message": "" }
```

Errors:

```json
{ "success": false, "error": { "code": "VALIDATION_ERROR", "message": "..." } }
```

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | /api/health | no | Database ping |
| POST | /api/auth/register | no | Creates USER |
| POST | /api/auth/login | no | JWT |
| POST | /api/auth/logout | yes | Client discards token |
| GET | /api/auth/me | yes | Current user |
| GET | /api/users/me/dashboard | yes | Aggregated studio data |
| GET | /api/ats/roles | yes | Seeded job roles |
| POST | /api/ats/analyze | yes | multipart file + job_role_id |
| GET | /api/ats/history | yes | Previous analyses |
| POST | /api/summarization | yes | JSON text + line_count + method |
| POST | /api/summarization/document | yes | multipart |
| GET | /api/rag/documents | yes | |
| POST | /api/rag/upload | yes | multipart PDF/DOCX/TXT |
| POST | /api/rag/query | yes | document_id + question |
| GET | /api/roadmaps | yes | |
| GET | /api/roadmaps/:id | yes | Includes progress |
| POST | /api/roadmaps/:id/progress | yes | step_id + completed |
| GET | /api/resources | yes | filters q, subject, difficulty, type, tag |
| GET | /api/resources/:id | yes | |
| POST | /api/resources/:id/bookmark | yes | Toggle |
| GET | /api/resources/bookmarks | yes | |
| GET | /api/search | yes | q |
| GET | /api/admin/stats | admin | |
| GET | /api/admin/users | admin | |
| PATCH | /api/admin/users/:id | admin | role |
| POST/PUT/DELETE | /api/admin/job-roles | admin | |
| POST/PUT/DELETE | /api/admin/resources | admin | |
| POST | /api/admin/roadmaps | admin | |
