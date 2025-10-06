# Music_Service

Lightweight FastAPI-based prototype for a music service (users, listeners, performers).

This README gives quick setup and run instructions based on the current project layout.

## What is in this repository
- `main.py` — FastAPI app entrypoint (creates DB tables on start and mounts routers).
- `config.py` — local configuration (builds the SQLite path used by SQLAlchemy).
- `src/app` — application package:
  - `core/security.py` — password hashing and JWT helpers
  - `database/session.py` — SQLAlchemy engine, `Base` and `get_db()` dependency
  - `models/user.py` — ORM models: `User`, `Listener`, `Perfomer`
  - `schemas/*` — Pydantic request/response schemas
  - `crud/*` — DB helpers for users
  - `services/*` — business logic / registration and login
  - `routers/auth.py` — API endpoints for register/login/me/listeners/performers
- `templates/test.html` — minimal HTML page with a registration test form
- `requirements.txt` — Python dependencies
- `.env.example` — example env vars for JWT secrets
- `migration/` (alembic) — migration files (keep these in version control)

## Quick start (Windows PowerShell)
1. Activate your virtual environment (example path used in this repo):
```powershell
C:\Users\vyalk\Desktop\Music_Service\Music_Service\Scripts\Activate.ps1
```

2. Install dependencies (only once or when updated):
```powershell
python -m pip install -r requirements.txt
```

3. Create a `.env` (copy `.env.example`) and set secure secrets for JWT keys:
```powershell
Copy-Item .env.example .env
#$env:JWT_SECRET_KEY="some_long_random_secret"
#$env:JWT_REFRESH_SECRET_KEY="another_random_secret"
```
You can also export them into the session before running the server:
```powershell
$env:JWT_SECRET_KEY = 'your_access_secret'
$env:JWT_REFRESH_SECRET_KEY = 'your_refresh_secret'
```

4. Run the server:
```powershell
python -m uvicorn main:app --reload
```

5. Open the quick test page in your browser:
```
http://127.0.0.1:8000/test
```

## Important environment variables
- `JWT_SECRET_KEY` — used to sign access tokens (HS256)
- `JWT_REFRESH_SECRET_KEY` — used to sign refresh tokens

## API endpoints (overview)
- POST `/register/listener` — create a Listener (see `ListenerCreate` schema)
- POST `/register/performer` — create a Performer
- POST `/login` — login with `{ email, password }`, returns `access_token`, `refresh_token`
- GET `/me` — current user info (requires `Authorization: Bearer <token>`)
- GET `/listeners` — list all listeners
- GET `/performers` — list all performers

Schemas: check `src/app/schemas/user.py` and `src/app/schemas/auth.py` for expected request/response shapes.

## Database & migrations
- The project uses SQLite by default (see `config.py`) and SQLAlchemy `Base.metadata.create_all()` is called at startup.
- Migration files (alembic) live in the `migration/` folder; keep migration files under source control — DO NOT add migration folder to `.gitignore`.

## Troubleshooting (common issues seen while developing)
- "no such table: users": means the app is connected to a DB file without the tables. Ensure the app uses the same `SQLALCHEMY_DATABASE_URL` as you expect and run `Base.metadata.create_all(bind=engine)` or start the app so it creates tables.
- "password cannot be longer than 72 bytes": comes from raw `bcrypt`. The project uses `bcrypt_sha256` (or can use Argon2) to avoid this limit. Don't call low‑level `bcrypt.hashpw` with long passwords.
- `jinja2 must be installed to use Jinja2Templates`: install Jinja2 (`pip install jinja2`) or run `pip install -r requirements.txt`.
- If you accidentally committed local files (venv, .env, DB), update `.gitignore` and run:
```powershell
git rm -r --cached .
git add .
git commit -m "Apply .gitignore and remove local artifacts from index"
```


---
