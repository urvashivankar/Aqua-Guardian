## Aqua Guardian

AI-assisted water quality monitoring platform with FastAPI backend, Supabase storage, and a modern Vite + React frontend.

### Project Structure
- `backend/`: FastAPI app, ML utilities, Supabase integrations.
- `frontend/`: Vite + React UI with shadcn components and Leaflet maps.
- `database/supabase_schema.sql`: Supabase tables, relationships, and policies.
- `docker-compose.yml`: Multi-service orchestration for local dev.

### Prerequisites
- Python 3.9+
- Node.js 18+ with npm
- Supabase project (URL + anon/service keys)

### Backend Setup
```bash
cd backend
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # create if missing
uvicorn main:app --reload
```
Populate `.env` with:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `STORAGE_BUCKET` (if using Supabase Storage)
- Blockchain/Web3 credentials as needed.

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Environment variables:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_API_URL` (default `http://localhost:8000`)

### Database Migration
Run `database/supabase_schema.sql` inside Supabase SQL editor or `supabase db push` to provision tables (`reports`, `photos`, `cleanup_actions`, `blockchain_logs`, `rewards`, `users`) and row-level security policies.

### Docker
```bash
docker compose up --build
```
Frontend available at `http://localhost:5173`, backend at `http://localhost:8000`.

### Testing Checklist
- `npm run lint` inside `frontend`
- `pytest` (add tests) for backend logic
- Manual upload flow via `/report` page and API `/reports` endpoint

### Contributing
1. Create feature branch
2. Add/Update tests
3. Run formatters/linters
4. Submit PR with screenshots for UI changes

