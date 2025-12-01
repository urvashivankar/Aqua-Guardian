# 🚀 AQUA Guardian - Production Deployment Guide

This guide walks you through deploying AQUA Guardian to production.

---

## 📋 Table of Contents

1. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Alternative: AWS Deployment](#alternative-aws-deployment)
4. [Database Configuration](#database-configuration)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Checklist](#post-deployment-checklist)

---

## 1. Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Code pushed to GitHub repository

### Step-by-Step

#### 1.1 Prepare Frontend

```bash
cd frontend

# Install dependencies
npm install

# Test build locally
npm run build

# Expected output:
# ✓ built in XXXms
# dist/ folder created
```

#### 1.2 Deploy to Vercel

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# ? Set up and deploy "frontend"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? aqua-guardian
# ? In which directory is your code located? ./
```

**Expected Output:**
```
🔍 Inspect: https://vercel.com/your-username/aqua-guardian/xxx
✅  Production: https://aqua-guardian.vercel.app [copied]
```

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Click "Deploy"

#### 1.3 Configure Environment Variables

In Vercel Dashboard → Project → Settings → Environment Variables:

```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc...your_anon_key
VITE_API_URL=https://your-backend.onrender.com
```

Click "Save" and redeploy.

#### 1.4 Configure Custom Domain (Optional)

1. Settings → Domains
2. Add domain (e.g., `aquaguardian.com`)
3. Update DNS records as shown
4. SSL automatically enabled

---

## 2. Backend Deployment (Render)

### Prerequisites
- GitHub account
- Render account (free tier available)
- Code pushed to GitHub repository

### Step-by-Step

#### 2.1 Prepare Backend

```bash
cd backend

# Test locally first
pip install -r requirements.txt
uvicorn main:app --reload

# Should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### 2.2 Deploy to Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:

```
Name: aqua-guardian-api
Region: Oregon (US West) or closest to your users
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

5. Click "Create Web Service"

#### 2.3 Configure Environment Variables

In Render Dashboard → Environment:

```
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key_here
STORAGE_BUCKET=photos

# Blockchain
WEB3_PROVIDER_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
CONTRACT_ADDRESS=0x1234567890abcdef...
DEPLOYER_PRIVATE_KEY=your_private_key_here

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_app_password_here
GOVT_EMAIL=government@example.com
NGO_EMAIL=ngo@example.com

# Or Email (SendGrid for production)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your_sendgrid_api_key
```

Click "Save Changes" - service will auto-redeploy.

#### 2.4 Verify Deployment

```bash
# Test health endpoint
curl https://your-api.onrender.com/health

# Expected:
# {"status": "healthy"}

# Test reports endpoint
curl https://your-api.onrender.com/reports/

# Expected:
# [array of reports]
```

**Expected URL:**
```
https://aqua-guardian-api.onrender.com
```

---

## 3. Alternative: AWS Deployment

### Frontend (AWS Amplify)

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize
cd frontend
amplify init

# Add hosting
amplify add hosting

# Choose:
# ? Select the plugin module: Hosting with Amplify Console
# ? Choose a type: Manual deployment

# Publish
amplify publish

# Expected URL:
# https://main.dxxxxxx.amplifyapp.com
```

### Backend (AWS Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
cd backend
eb init -p python-3.11 aqua-guardian

# Create environment
eb create aqua-guardian-env

# Set environment variables
eb setenv SUPABASE_URL=xxx SUPABASE_KEY=xxx ...

# Deploy
eb deploy

# Open
eb open

# Expected URL:
# http://aqua-guardian-env.eba-xxxx.us-west-2.elasticbeanstalk.com
```

---

## 4. Database Configuration

### Supabase Production Setup

1. **Log in to Supabase Dashboard**
   - Go to [supabase.com](https://supabase.com)
   - Select your project

2. **Run Migrations**
   ```sql
   -- In Supabase SQL Editor, run:
   -- database/supabase_schema.sql
   -- database/add_dashboard_tables.sql
   ```

3. **Configure Storage**
   - Storage → Create bucket: `photos`
   - Make public: Settings → Public bucket ✓
   - Set up policies:
   ```sql
   -- Allow public read
   CREATE POLICY "Public Access"
   ON storage.objects FOR SELECT
   USING (bucket_id = 'photos');
   
   -- Allow authenticated upload
   CREATE POLICY "Authenticated Upload"
   ON storage.objects FOR INSERT
   TO authenticated
   WITH CHECK (bucket_id = 'photos');
   ```

4. **Enable Connection Pooling**
   - Settings → Database → Connection Pooling
   - Enable Transaction mode
   - Copy connection string for production

5. **Set up Backups**
   - Settings → Database → Backups
   - Enable daily backups (Pro plan)

---

## 5. Environment Variables

### Complete List

#### Frontend (Vercel)
```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_API_URL=https://aqua-guardian-api.onrender.com
```

#### Backend (Render/AWS)
```env
# Database
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (service_role)
STORAGE_BUCKET=photos

# Blockchain
WEB3_PROVIDER_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
CONTRACT_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
DEPLOYER_PRIVATE_KEY=0xYOUR_PRIVATE_KEY

# Email - Gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # App password

# Email - SendGrid (Production)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxxxxxxxxxxx

# Recipients
GOVT_EMAIL=pollution-dept@government.in
NGO_EMAIL=water-watch@ngo.org
```

---

## 6. Post-Deployment Checklist

### 6.1 Functionality Tests

- [ ] Frontend loads at production URL
- [ ] All pages render correctly (Home, Dashboard, Report, etc.)
- [ ] User can sign up
- [ ] User can log in
- [ ] User can submit report without image
- [ ] User can submit report with image
- [ ] AI classification works
- [ ] Dashboard shows data
- [ ] Success stories load
- [ ] NFT adoption page works

### 6.2 API Tests

```bash
# Replace with your production URL
API_URL="https://aqua-guardian-api.onrender.com"

# Test health
curl $API_URL/health

# Test reports
curl $API_URL/reports/

# Test create report
curl -X POST $API_URL/reports/ \
  -F "user_id=test_user" \
  -F "latitude=28.6139" \
  -F "longitude=77.2090" \
  -F "description=Test report" \
  -F "severity=5"
```

### 6.3 Performance Tests

```bash
# Install Lighthouse
npm install -g lighthouse

# Test frontend
lighthouse https://aqua-guardian.vercel.app \
  --output html \
  --output-path ./report.html

# Target scores:
# Performance: > 90
# Accessibility: > 95
# Best Practices: > 95
# SEO: > 95
```

### 6.4 Security Checklist

- [ ] All `.env` files in `.gitignore`
- [ ] No API keys in frontend code
- [ ] HTTPS enabled (SSL)
- [ ] CORS configured properly
- [ ] Supabase RLS policies enabled
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] File upload size limits (5MB)

### 6.5 Monitoring Setup

#### Vercel Analytics
1. Vercel Dashboard → Analytics
2. Enable Web Analytics
3. View real-time traffic

#### Render Dashboard
1. Render Dashboard → Metrics
2. Monitor CPU, Memory, Response time

#### UptimeRobot (Free)
1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add Monitor:
   - Type: HTTP(s)
   - URL: `https://aqua-guardian-api.onrender.com/health`
   - Interval: 5 minutes
3. Set up email alerts

#### Sentry (Error Tracking)
```bash
# Frontend
npm install @sentry/react

# Backend
pip install sentry-sdk
```

Update code:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## 🎉 Deployment Complete!

Your AQUA Guardian application is now live at:
- **Frontend:** https://aqua-guardian.vercel.app
- **Backend:** https://aqua-guardian-api.onrender.com

### Next Steps:
1. Monitor logs for the first 24 hours
2. Test all features in production
3. Collect user feedback
4. Plan next sprint features

### Rollback Plan:
```bash
# Vercel - revert to previous deployment
vercel --prod --force

# Render - Settings → Deploys → Redeploy previous version
```

---

## 🆘 Troubleshooting

### Frontend Issues

**Build fails:**
```bash
# Check node version
node --version  # Should be 18+

# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Environment variables not working:**
- Ensure variables start with `VITE_`
- Redeploy after adding variables
- Check browser console for undefined values

### Backend Issues

**Deployment fails:**
```bash
# Check requirements.txt
pip install -r requirements.txt

# Test start command locally
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Database connection fails:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY`
- Check Supabase project is active
- Test connection from local machine first

**Email not sending:**
- Verify SMTP credentials
- Check 2FA enabled for Gmail
- Regenerate app password
- Test with test_notification.py first

---

## 📞 Support

If you encounter issues:
1. Check deployment logs
2. Review this guide
3. Test locally first
4. Check service status pages (Vercel, Render, Supabase)

**Status Pages:**
- Vercel: https://www.vercel-status.com/
- Render: https://status.render.com/
- Supabase: https://status.supabase.com/
