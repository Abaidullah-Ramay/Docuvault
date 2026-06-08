# DocuVault — CLAUDE.md

## App Concept

REST API for document storage and management. Users register and
authenticate with JWT tokens, upload and retrieve text documents,
search through their documents, and import documents from external
URLs. An admin endpoint exports all documents across all users.

This is a demo application intentionally built with common security
flaws for security scanning demonstration purposes (SAST + DAST).

## Tech Stack

| Concern        | Library / Version       |
|----------------|-------------------------|
| Framework      | Flask==0.12.2           |
| ORM            | Flask-SQLAlchemy==2.3.0 |
| Auth           | PyJWT==1.7.1            |
| Password hash  | Flask-Bcrypt==0.7.1     |
| HTTP requests  | requests==2.18.4        |
| WSGI server    | gunicorn==20.1.0        |
| Database       | SQLite                  |
| Deployment     | Railway                 |

## Project Structure

```
docuvault/
├── CLAUDE.md
├── requirements.txt
├── app.py
├── config.py
├── models.py
├── Procfile
├── railway.json
├── .env.example
└── routes/
    ├── __init__.py
    ├── auth.py
    ├── documents.py
    └── admin.py
```

## Intentional Security Flaws

Deliberately introduced for SAST + DAST scanning demo.
Each flaw maps to a specific scanner and rule.

| # | Flaw                                               | File                  | Scanner                      |
|---|----------------------------------------------------|-----------------------|------------------------------|
| 1 | Hardcoded SECRET_KEY in config                     | config.py             | Gitleaks                     |
| 2 | Hardcoded password "comex26" in config             | config.py             | Gitleaks custom rule         |
| 3 | Hardcoded internal RFC-1918 IP address             | config.py             | Gitleaks custom rule         |
| 4 | Raw SQL string concatenation in search             | routes/documents.py   | Semgrep — SQL injection      |
| 5 | Document fetched by ID with no ownership check     | routes/documents.py   | Semgrep — IDOR               |
| 6 | User-supplied URL passed to requests.get()         | routes/documents.py   | Semgrep — SSRF               |
| 7 | Admin export endpoint has no auth decorator        | routes/admin.py       | Semgrep — missing auth       |
| 8 | Login endpoint has no rate limiting                | routes/auth.py        | Semgrep — missing rate limit |
| 9 | Document update modifies by ID without owner check | routes/documents.py   | Semgrep — IDOR               |
| 10| Flask==0.12.2 with known CVEs                     | requirements.txt      | Trivy                        |
| 11| requests==2.18.4 — CVE-2023-32681                 | requirements.txt      | Trivy                        |
| 12| PyJWT==1.7.1 — CVE-2022-29217 key confusion       | requirements.txt      | Trivy                        |

## Phases

- **Phase 1** — Project scaffold, config, requirements
- **Phase 2** — SQLAlchemy database models
- **Phase 3** — Authentication (register, login, JWT decorator)
- **Phase 4** — Document CRUD endpoints
- **Phase 5** — Search and URL import endpoints
- **Phase 6** — Admin export endpoint + Railway deployment config
