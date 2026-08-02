# Backend

FastAPI service for AI Fitness Coach, with SQLAlchemy 2.0 persistence and JWT authentication.

## Run locally

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

By default the backend uses a local SQLite database at `sqlite:///./ai_fitness_coach.db`. To use PostgreSQL instead, set `AI_FITNESS_DATABASE_URL` in `.env` to your PostgreSQL connection string before running migrations.

## Authentication API

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout` (Bearer access token required)
- `GET /api/v1/users/me` (Bearer access token required)

Access tokens are short-lived. Refresh tokens rotate on use and their SHA-256 fingerprints are persisted, allowing logout and refresh-token replay prevention.
