# MediTalks Deployment Guide

## 🚀 Free Hosting Options

### Option 1: Render (Recommended for Full-Stack)

#### Backend Deployment (Flask + SEA-Lion/Gemini)
1. **Create Render Account**: https://render.com
2. **Connect GitHub**: Link your repository
3. **Create Web Service**:
   - Repository: `your-github-username/Meditalks`
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python app.py`
   - Environment Variables:
     ```
     GEMINI_API_KEY=your_gemini_key
     SEALION_API_KEY=your_sealion_key
     PORT=10000
     ```

#### Frontend Deployment (React)
1. **Create Static Site** on Render
2. **Build Settings**:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`

### Option 2: Railway

#### Backend (Flask)
1. **Create Railway Account**: https://railway.app
2. **Deploy from GitHub**:
   - Connect repository
   - Select `backend` folder
   - Add environment variables:
     ```
     GEMINI_API_KEY=your_key
     SEALION_API_KEY=your_key
     ```

#### Frontend (React)
1. **Deploy Static Site**:
   - Build command: `npm run build`
   - Output directory: `build`

### Option 3: Vercel + PythonAnywhere

#### Frontend on Vercel
1. **Create Vercel Account**: https://vercel.com
2. **Import GitHub Project**
3. **Configure**:
   - Framework: React
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

#### Backend on PythonAnywhere
1. **Create PythonAnywhere Account**: https://www.pythonanywhere.com
2. **Upload backend files**
3. **Configure WSGI file**
4. **Set environment variables**

## 📁 Project Structure for Deployment

```
Meditalks/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env (for local development)
│   ├── services/
│   ├── config/
│   └── utils/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── build/ (generated)
└── README.md
```

## 🔧 Pre-Deployment Setup

### 1. Create requirements.txt
```bash
cd backend
pip freeze > requirements.txt
```

### 2. Update Frontend API URLs
In `frontend/src/App.js`, update for production:
```javascript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.render.com'
  : 'http://localhost:5000';
```

### 3. Environment Variables
**Backend (.env for local, platform settings for production):**
```
GEMINI_API_KEY=your_gemini_api_key
SEALION_API_KEY=your_sealion_api_key
FLASK_ENV=production
PORT=5000
```

**Frontend (for API URL configuration):**
```
REACT_APP_API_URL=https://your-backend-url.com
```

## 🌐 Single Domain Deployment (Alternative)

### Serve React from Flask
1. **Build React app**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Move build to backend**:
   ```bash
   cp -r frontend/build backend/static
   ```

3. **Update Flask app.py**:
   ```python
   from flask import send_from_directory
   
   app = Flask(__name__, static_folder='static', static_url_path='')
   
   @app.route('/')
   def serve_index():
       return send_from_directory(app.static_folder, 'index.html')
   
   @app.route('/<path:path>')
   def serve_static(path):
       return send_from_directory(app.static_folder, path)
   ```

4. **Deploy single backend** with static files

## 🔑 API Keys Setup

### Google Gemini API
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key
3. Add to environment variables

### SEA-Lion API
1. Contact AI Singapore: https://www.aisingapore.org/sea-lion/
2. Request research/commercial access
3. Get API credentials
4. Add to environment variables

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Test application locally
- [ ] Create requirements.txt
- [ ] Update API URLs for production
- [ ] Prepare environment variables
- [ ] Test with production build

### Backend Deployment
- [ ] Deploy to chosen platform (Render/Railway/etc.)
- [ ] Configure environment variables
- [ ] Test API endpoints
- [ ] Verify AI service connections

### Frontend Deployment
- [ ] Update API URLs
- [ ] Build production version
- [ ] Deploy to platform
- [ ] Test frontend functionality
- [ ] Verify backend integration

### Post-Deployment
- [ ] Test full application workflow
- [ ] Test PDF upload functionality
- [ ] Verify cultural adaptation features
- [ ] Check error handling
- [ ] Monitor application logs

## 🔍 Troubleshooting

### Common Issues

#### CORS Errors
**Solution**: Update CORS origins in Flask app:
```python
CORS(app, origins=['https://your-frontend-domain.com'])
```

#### API Key Issues
**Solution**: Verify environment variables are set correctly on hosting platform

#### Build Failures
**Solution**: Check Node.js/Python versions match local development

#### File Upload Issues
**Solution**: Ensure hosting platform supports file uploads and has sufficient storage

### Testing Production
1. **Health Check**: Visit `https://your-backend-url/api/health`
2. **Frontend**: Test all features including PDF upload
3. **AI Services**: Verify which AI service is being used
4. **Error Handling**: Test with invalid inputs

## 💰 Cost Considerations

### Free Tier Limitations
- **Render**: 750 hours/month, sleeps after inactivity
- **Railway**: $5 credit/month, then pay-as-you-go
- **Vercel**: Unlimited static sites, generous bandwidth
- **PythonAnywhere**: Limited CPU time on free tier

### Upgrade Recommendations
For production use, consider:
- Paid hosting plans for always-on services
- CDN for static assets
- Database hosting for user data
- Monitoring and analytics tools

## 🔄 Continuous Deployment

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          # Render auto-deploys on push
          echo "Deployment triggered"
```

## 📊 Monitoring

### Health Checks
- Backend: `https://your-app.com/api/health`
- Monitor AI service availability
- Track response times

### Analytics
Consider adding:
- Google Analytics for frontend
- Application performance monitoring
- Error tracking (Sentry)
- Usage analytics for AI services

## 🚀 Going Live

1. **Test thoroughly** in staging environment
2. **Set up monitoring** and error tracking
3. **Configure custom domain** (if desired)
4. **Set up SSL certificates** (usually automatic)
5. **Monitor initial usage** and performance
6. **Gather user feedback** and iterate

## 📞 Support Resources

- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Vercel**: https://vercel.com/docs
- **Google AI**: https://ai.google.dev/docs
- **AI Singapore**: https://www.aisingapore.org
