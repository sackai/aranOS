# AgentForge AI

AgentForge AI is a production-ready hackathon project for building an autonomous software development team with eight collaborating AI agents. Users submit a software idea, watch agents execute in real time, review generated specifications and files, and download the generated project bundle.

## Stack

- Frontend: React 19, Vite, Tailwind CSS, React Router, Axios, Framer Motion, Lucide React
- Backend: FastAPI, SQLAlchemy, PostgreSQL, JWT, Alembic, Uvicorn
- AI: OpenAI API with a multi-agent orchestration layer

## Quick start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. If PostgreSQL is not available, set `DATABASE_URL=sqlite:///./agentforge.db` in `backend/.env` for local development.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI runs at `http://localhost:5173`.

### Docker Compose

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Frontend: `http://localhost:5173`, API: `http://localhost:8000`.

## Features

- User registration, login, JWT authentication, and profile endpoint
- Dashboard with project history and empty/loading/error states
- Create Project workflow
- Real-time agent execution screen using Server-Sent Events
- Agent status timeline and live logs
- Generated project files viewer and Markdown documentation viewer
- Download generated project as ZIP
- Dark mode, responsive glassmorphism UI, and animated interactions

## API overview

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/me`
- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `POST /api/projects/{project_id}/execute`
- `GET /api/projects/{project_id}/stream`
- `GET /api/projects/{project_id}/download`

## OpenAI configuration

Set `OPENAI_API_KEY` in `backend/.env`. Without a key, AgentForge uses a deterministic local generation mode so the app remains runnable for demos and tests.
