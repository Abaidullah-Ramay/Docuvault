# DocuVault

REST API for document storage and management. Users register, authenticate with JWT tokens, upload and retrieve text documents, search through their documents, and import documents from external URLs. An admin endpoint exports all documents across all users.

> **Note:** This application is intentionally built with common security flaws for SAST + DAST scanning demonstrations. Do not deploy to production.

---

## Endpoint Reference

### Authentication

#### `POST /auth/register`
Create a new user account.

- **Auth required:** No
- **Body:** `{ "email": "user@example.com", "password": "secret" }`
- **Response 201:** `{ "message": "registered", "user_id": 1 }`
- **Response 409:** `{ "error": "email already exists" }`

#### `POST /auth/login`
Authenticate and receive a JWT token.

- **Auth required:** No
- **Body:** `{ "email": "user@example.com", "password": "secret" }`
- **Response 200:** `{ "token": "<jwt>" }`
- **Response 401:** `{ "error": "invalid credentials" }`

---

### Documents

All document endpoints require a JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

#### `POST /documents`
Create a new document.

- **Auth required:** Yes
- **Body:** `{ "title": "My Doc", "content": "Body text here" }`
- **Response 201:** Document object

#### `GET /documents`
List all documents owned by the authenticated user.

- **Auth required:** Yes
- **Response 200:** Array of document objects

#### `GET /documents/<id>`
Fetch a single document by ID.

- **Auth required:** Yes
- **Response 200:** Document object
- **Response 404:** `{ "error": "not found" }`

#### `PUT /documents/<id>`
Update a document's title and content.

- **Auth required:** Yes
- **Body:** `{ "title": "New Title", "content": "New body" }`
- **Response 200:** Updated document object
- **Response 404:** `{ "error": "not found" }`

#### `DELETE /documents/<id>`
Delete a document.

- **Auth required:** Yes
- **Response 200:** `{ "message": "deleted" }`
- **Response 404:** `{ "error": "not found" }`

#### `GET /documents/search?q=<keyword>`
Search documents by title or content using a keyword.

- **Auth required:** Yes
- **Query param:** `q` — search keyword
- **Response 200:** Array of matching document objects

#### `POST /documents/import`
Fetch content from an external URL and save it as a document.

- **Auth required:** Yes
- **Body:** `{ "url": "https://example.com", "title": "Page title" }`
- **Response 201:** Created document object

---

### Admin

#### `GET /admin/export`
Export all documents across all users with owner information.

- **Auth required:** No
- **Response 200:** Array of objects containing `id`, `title`, `content`, `created_at`, `owner_id`, `owner_email`

---

## Document Object Shape

```json
{
  "id": 1,
  "title": "My Doc",
  "content": "Body text here",
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00"
}
```

---

## Local Setup

```bash
pip install -r requirements.txt
python app.py
```

The server starts on `http://127.0.0.1:5000`. The SQLite database file `docuvault.db` is created automatically on first run.

### Environment Variables

Copy `.env.example` and set values as needed:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | JWT signing key |
| `DATABASE_URL` | SQLAlchemy database URI (defaults to `sqlite:///docuvault.db`) |

---

## Railway Deployment

1. Push this repository to GitHub.
2. Go to [railway.app](https://railway.app) and create a new project.
3. Select **Deploy from GitHub repo** and choose this repository.
4. Railway detects the `Procfile` and `railway.json` automatically and starts the build.
5. The app will be available at the URL Railway assigns to the service.

The `Procfile` runs `gunicorn app:app` and `railway.json` sets the builder to NIXPACKS.
