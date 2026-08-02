# AI Fitness Coach

AI Fitness Coach is a production-oriented monorepo for an AI-assisted fitness application. It pairs a **Next.js** web client with a **FastAPI** service, while keeping cross-cutting contracts and utilities in a small shared workspace.

## Repository layout

```text
frontend/   Next.js application: routes, UI, client state, and API clients
backend/    FastAPI application: APIs, domain services, persistence, and AI prompts
shared/     Framework-agnostic constants, types, and utilities
```

The backend follows a clean, layered organization: API handlers validate and orchestrate requests; services contain application logic; repositories isolate data access; models and schemas define persistence and API contracts. AI prompt templates live separately from endpoint code so they can be reviewed and evolved independently.

## Getting started

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

The frontend is available at `http://localhost:3000` by default.

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`; interactive documentation is at `/docs`.

By default the backend uses a local SQLite database at `sqlite:///./ai_fitness_coach.db`. To switch back to PostgreSQL, override `AI_FITNESS_DATABASE_URL` in `backend/.env` with your PostgreSQL connection string.

## Docker

Start the development stack with:

```bash
docker compose up --build
```

The included service Dockerfiles provide local development containers for both applications.

## Environment configuration

Copy the example environment files before development. Do not commit real credentials. Configure `NEXT_PUBLIC_API_BASE_URL` on the frontend to point to the backend URL and set backend secrets (database URL, CORS origins, model provider keys) in `backend/.env`.

## Quality expectations

- Add frontend component and route tests alongside the feature or in the chosen test suite.
- Add backend tests under `backend/tests`.
- Make schema and model changes through Alembic migrations.
- Keep shared code framework-neutral; do not import backend or frontend frameworks into `shared`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
