# 🚀 AQUA Guardian - Quick Start Guide

## Get Started in 5 Minutes!

### 1. Prerequisites

**Install these first:**
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

**Verify installation:**
```bash
python --version  # Should be 3.9+
node --version    # Should be 18+
npm --version     # Should be 9+
```

---

### 2. Clone & Setup

**Windows:**
```cmd
# Run the setup script
setup.bat
```

**Linux/Mac:**
```bash
# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

This will automatically:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Install blockchain tools (optional)

---

### 3. Configure Environment

#### Backend Configuration

Create `backend/.env`:
```env
# Supabase (Get from: https://supabase.com/dashboard/project/_/settings/api)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key_here
STORAGE_BUCKET=photos

# Email (Gmail - for testing)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
GOVT_EMAIL=govt@example.com
NGO_EMAIL=ngo@example.com

# Blockchain (optional - configure later)
WEB3_PROVIDER_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
CONTRACT_ADDRESS=
```

#### Frontend Configuration

Create `frontend/.env`:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
VITE_API_URL=http://localhost:8000
```

---

### 4. Setup Database

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create new project (or use existing)
3. Go to SQL Editor
4. Run these files in order:
   - `database/supabase_schema.sql`
   - `database/add_dashboard_tables.sql`
5. Go to Storage → Create bucket named `photos` (make it public)

---

### 5. Run the Application

**Option A: Use Start Scripts (Easiest)**

Windows:
```cmd
# Terminal 1: Start backend
start_backend.bat

# Terminal 2: Start frontend
start_frontend.bat
```

Linux/Mac:
```bash
# Terminal 1: Start backend
./start_backend.sh

# Terminal 2: Start frontend
./start_frontend.sh
```

**Option B: Manual Start**

Terminal 1 - Backend:
```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn main:app --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

---

### 6. Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

### 7. Test the App

1. Open http://localhost:5173
2. Click "Report Pollution"
3. Fill the form:
   - Location: Use "Get Current Location"
   - Description: "Test pollution report"
   - Severity: Select any level
   - Photo: Upload any image (optional)
4. Click "Submit Report"
5. Should see success message!

---

## 📚 Next Steps

### For Development:
- [ ] Review `implementation_plan.md` for remaining work
- [ ] Train AI model (see Phase 1 in implementation plan)
- [ ] Deploy blockchain contract (see Phase 2)
- [ ] Run tests: `cd backend && pytest tests/`

### For Production:
- [ ] Follow `DEPLOYMENT_GUIDE.md`
- [ ] Complete `LAUNCH_CHECKLIST.md`
- [ ] Deploy to Vercel + Render

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Kill the process or use different port:
uvicorn main:app --reload --port 8001
```

### Frontend won't start
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database connection fails
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `backend/.env`
- Check Supabase project isactive
- Test connection: `cd backend && python test_supabase_connection.py`

### Email not sending
- Gmail: Enable 2FA and create App Password
- Verify SMTP credentials in `.env`
- Test: `cd backend && python test_notification.py`

---

## 📖 Documentation

- **Implementation Plan:** `implementation_plan.md` - What's left to build
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md` - How to deploy
- **Launch Checklist:** `LAUNCH_CHECKLIST.md` - Pre-launch verification
- **API Docs:** http://localhost:8000/docs (when backend running)

---

## 🎯 Key Features to Test

1. **Report Submission** `/report`
   - With and without images
   - AI classification
   - Location capture

2. **Dashboard** `/dashboard`
   - Real-time water quality charts
   - Recent reports

3. **Success Stories** `/success-stories`
   - Showcases resolved cases

4. **NFT Adoption** `/nft-adoption`
   - Gamification features

5. **Marine Impact** `/marine-impact`
   - Educational content

---

## 💡 Pro Tips

1. **Use Chrome DevTools** (F12) to debug frontend issues
2. **Check Backend Logs** in terminal for API errors
3. **Supabase Dashboard** has great SQL editor and logs
4. **API Docs** at `/docs` let you test endpoints directly

---

## 🚀 Ready to Build?

You're all set! The basic infrastructure is running. Now:

1. Review the **implementation_plan.md** for complete feature list
2. Start with **AI model training** (Phase 1)
3. Then move to **blockchain deployment** (Phase 2)
4. Follow with **testing** and **deployment**

**Need help?** Check the documentation files or review the code comments.

---

**Happy Building! 🌊**
