# 🚀 Render Deployment Guide for MediTalks

## Prerequisites

1. **GitHub Account** with your MediTalks repository
2. **Render Account** (free): https://render.com
3. **API Keys**:
   - Gemini API Key: `AIzaSyANF39ejA2C0I7gfbWHCvSMXOZxWINzjko`
   - SEA-Lion API Key: `sk-GL690ArTf8Ek5UzGjcMYjQ`

## Step 1: Prepare Your Repository

1. **Commit all changes** to your GitHub repository:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

## Step 2: Deploy Backend to Render

### 2.1 Create Web Service
1. **Log in to Render**: https://render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect Repository**: Select your GitHub repository
4. **Configure Service**:
   - **Name**: `meditalks-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 2.2 Set Environment Variables
In the **Environment** section, add:

```
GEMINI_API_KEY=AIzaSyANF39ejA2C0I7gfbWHCvSMXOZxWINzjko
SEALION_API_KEY=sk-GL690ArTf8Ek5UzGjcMYjQ
SEALION_API_URL=https://api.sealion.ai/v1
FLASK_ENV=production
FLASK_DEBUG=False
```

### 2.3 Deploy
1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Note your backend URL**: `https://meditalks-backend.onrender.com`

## Step 3: Deploy Frontend to Render

### 3.1 Create Static Site
1. **Click "New +"** → **"Static Site"**
2. **Connect Repository**: Same GitHub repository
3. **Configure Static Site**:
   - **Name**: `meditalks-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

### 3.2 Set Environment Variables
In the **Environment** section, add:
```
REACT_APP_API_URL=https://meditalks-backend.onrender.com
```

### 3.3 Deploy
1. **Click "Create Static Site"**
2. **Wait for deployment** (3-5 minutes)
3. **Note your frontend URL**: `https://meditalks-frontend.onrender.com`

## Step 4: Update CORS Settings

1. **Update backend CORS** to include your frontend URL
2. **In your GitHub repository**, edit `backend/app.py`:
   ```python
   allowed_origins = [
       'http://localhost:3000',
       'https://meditalks-frontend.onrender.com',  # Add your actual frontend URL
       # ... other origins
   ]
   ```
3. **Commit and push** the changes
4. **Render will auto-deploy** the updated backend

## Step 5: Test Deployment

### 5.1 Test Backend
1. **Visit**: `https://meditalks-backend.onrender.com/api/health`
2. **Should see**:
   ```json
   {
     "status": "OK",
     "service": "MediTalks Backend",
     "ai_services": {
       "sealion_available": true,
       "primary_service": "SEA-Lion"
     }
   }
   ```

### 5.2 Test Frontend
1. **Visit**: `https://meditalks-frontend.onrender.com`
2. **Click "Test Backend Connection"**
3. **Should show**: Primary AI service and availability

### 5.3 Test Full Workflow
1. **Test Text Adaptation**:
   - Enter medical message
   - Select cultural context
   - Generate adaptation

2. **Test PDF Upload**:
   - Upload PDF file
   - Select cultural context and language
   - Check AI-generated summary

## Step 6: Custom Domain (Optional)

### 6.1 Frontend Custom Domain
1. **In Render Dashboard** → Your static site → Settings
2. **Add Custom Domain**: `meditalks.yourdomain.com`
3. **Update DNS** records as instructed

### 6.2 Backend Custom Domain
1. **In Render Dashboard** → Your web service → Settings
2. **Add Custom Domain**: `api.meditalks.yourdomain.com`
3. **Update frontend** environment variable:
   ```
   REACT_APP_API_URL=https://api.meditalks.yourdomain.com
   ```

## Step 7: Monitoring & Maintenance

### 7.1 Monitor Logs
1. **Backend Logs**: Render Dashboard → meditalks-backend → Logs
2. **Frontend Logs**: Render Dashboard → meditalks-frontend → Logs

### 7.2 Auto-Deploy Setup
- **Already configured**: Pushes to `main` branch trigger auto-deployment
- **Manual deploy**: Use "Manual Deploy" button in dashboard

### 7.3 Environment Management
- **Staging**: Create separate services for testing
- **Production**: Use current setup with monitoring

## Troubleshooting

### Common Issues

#### 1. Backend Build Fails
**Solution**: Check `requirements-minimal.txt` has correct dependencies:
```
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
google-generativeai==0.3.2
PyPDF2==3.0.1
pdfplumber==0.9.0
requests==2.32.4
Werkzeug==2.3.7
gunicorn==21.2.0
```

#### 2. Frontend Can't Connect to Backend
**Solutions**:
- Check `REACT_APP_API_URL` environment variable
- Verify CORS settings in backend
- Check backend health endpoint

#### 3. PDF Upload Fails
**Solutions**:
- File size limits on free tier
- Check backend logs for errors
- Verify file upload permissions

#### 4. AI Services Not Working
**Solutions**:
- Verify API keys in environment variables
- Check backend logs for API errors
- Test individual service endpoints

### Free Tier Limitations

- **Backend**: 750 hours/month, sleeps after 15min inactivity
- **Frontend**: Unlimited static hosting
- **File uploads**: Limited to 100MB
- **Bandwidth**: 100GB/month

### Upgrade Considerations

For production use:
- **Paid plans**: $7/month for always-on backend
- **Monitoring**: Enable monitoring and alerts
- **Backup**: Database backup if you add user data
- **CDN**: For faster global access

## Success Checklist

- [ ] Backend deployed and responding at `/api/health`
- [ ] Frontend deployed and loading correctly
- [ ] API connection working (test button shows success)
- [ ] Text adaptation feature working
- [ ] PDF upload and summarization working
- [ ] SEA-Lion AI service active (or Gemini fallback)
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

## Your Deployed URLs

**Frontend**: `https://meditalks-frontend.onrender.com`
**Backend**: `https://meditalks-backend.onrender.com`
**Health Check**: `https://meditalks-backend.onrender.com/api/health`

🎉 **Congratulations!** Your MediTalks application is now live and accessible worldwide!
