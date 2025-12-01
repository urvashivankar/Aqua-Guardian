# Deployment Guide - AQUA Guardian

## Prerequisites

Before deploying, ensure you have:
- GitHub repository with latest code
- Render account (for backend)
- Vercel account (for frontend)
- Supabase project with database configured

## Backend Deployment (Render)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Fix: Configure backend for production deployment"
git push origin main
```

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `aqua-guardian-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

### Step 3: Set Environment Variables

In Render dashboard, add these environment variables:

```
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
WEB3_PROVIDER_URL=your_web3_provider_url
CONTRACT_ADDRESS=your_contract_address
DEPLOYER_PRIVATE_KEY=your_deployer_private_key
```

### Step 4: Deploy

Click **Create Web Service** and wait for deployment to complete.

**Copy your backend URL** (e.g., `https://aqua-guardian-api.onrender.com`)

---

## Frontend Deployment (Vercel)

### Step 1: Update Production Environment

Edit `frontend/.env.production` and replace with your Render backend URL:

```env
VITE_API_URL=https://aqua-guardian-api.onrender.com
```

### Step 2: Commit Changes
```bash
git add frontend/.env.production
git commit -m "Update production API URL"
git push origin main
```

### Step 3: Deploy to Vercel

#### Option A: Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel --prod
```

#### Option B: Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://aqua-guardian-api.onrender.com` (your backend URL)

6. Click **Deploy**

**Copy your frontend URL** (e.g., `https://aqua-guardian.vercel.app`)

---

## Post-Deployment Configuration

### Update CORS Settings

1. Go back to Render dashboard
2. Update the `ALLOWED_ORIGINS` environment variable with your Vercel URL:
   ```
   ALLOWED_ORIGINS=https://aqua-guardian.vercel.app
   ```
3. Redeploy the backend service

---

## Testing Deployment

### 1. Test Backend Health
```bash
curl https://aqua-guardian-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AQUA Guardian API",
  "version": "1.0.0"
}
```

### 2. Test Frontend

1. Visit your Vercel URL
2. Navigate to the Report page
3. Fill out the form with test data
4. Upload a test image
5. Submit the report
6. Check browser console for any errors

### 3. Verify CORS

Open browser DevTools → Network tab:
- Submit a report
- Check the `/reports/` request
- Verify `Access-Control-Allow-Origin` header is present

---

## Troubleshooting

### Issue: CORS Error

**Symptom**: Browser console shows "CORS policy" error

**Solution**:
1. Verify `ALLOWED_ORIGINS` in Render includes your Vercel URL
2. Ensure no trailing slashes in URLs
3. Redeploy backend after changing environment variables

### Issue: API Connection Failed

**Symptom**: "Failed to fetch" or network errors

**Solution**:
1. Check `VITE_API_URL` in Vercel environment variables
2. Verify backend is running (check Render logs)
3. Test backend health endpoint directly

### Issue: Report Submission Fails

**Symptom**: Report submission returns 500 error

**Solution**:
1. Check Render logs for backend errors
2. Verify Supabase credentials are correct
3. Ensure database tables exist (reports, photos, blockchain_logs)

### Issue: AI Classification Not Working

**Symptom**: Reports submitted but no AI classification

**Solution**:
1. Check if ML model files are deployed
2. Verify TensorFlow is installed (check Render build logs)
3. May need to upload model files separately

---

## Environment Variables Reference

### Backend (Render)

| Variable | Required | Description |
|----------|----------|-------------|
| `ENVIRONMENT` | Yes | Set to `production` |
| `ALLOWED_ORIGINS` | Yes | Vercel frontend URL |
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase anon key |
| `WEB3_PROVIDER_URL` | Optional | Blockchain provider |
| `CONTRACT_ADDRESS` | Optional | Smart contract address |
| `DEPLOYER_PRIVATE_KEY` | Optional | Blockchain private key |

### Frontend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Render backend URL |

---

## Quick Commands

### Update and Redeploy
```bash
# Make changes
git add .
git commit -m "Your commit message"
git push origin main

# Vercel will auto-deploy
# Render will auto-deploy if connected to GitHub
```

### View Logs
```bash
# Render: Check dashboard → Logs tab
# Vercel: Check dashboard → Deployments → View Function Logs
```
