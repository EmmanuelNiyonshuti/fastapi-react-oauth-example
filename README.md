# FastAPI + React OAuth 2.0 Example

example for OAuth 2.0 login implementation with Google and GitHub using FastAPI and React

## Run the application
```bash
# Clone and setup
git clone <your-repo-url>
cd <repo-name>
cp .env.example .env  # Add your OAuth credentials here and your database credentials

# With Docker
docker compose up
docker compose exec backend uv run alembic upgrade head

# Without Docker - Backend
cd backend
python -m venv .venv
source .venv/bin/activate 
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Without Docker - Frontend
cd frontend
npm install
npm run dev
```

for setting up oauth2.0 providers in this application and getting credentials you can use these urls:
- Google: https://console.cloud.google.com/apis/credentials
- GitHub: https://github.com/settings/developers