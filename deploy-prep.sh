#!/bin/bash

# MediTalks Deployment Preparation Script

echo "🚀 Preparing MediTalks for Render Deployment"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "RENDER_DEPLOYMENT.md" ]; then
    echo "❌ Please run this script from the MediTalks root directory"
    exit 1
fi

echo "📋 Pre-deployment checklist:"

# 1. Check backend requirements
echo "✅ Checking backend requirements..."
if [ ! -f "backend/requirements-minimal.txt" ]; then
    echo "❌ backend/requirements-minimal.txt not found"
    exit 1
fi

# 2. Check frontend package.json
echo "✅ Checking frontend configuration..."
if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json not found"
    exit 1
fi

# 3. Check render.yaml
echo "✅ Checking Render configuration..."
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found"
    exit 1
fi

# 4. Check API keys are configured (in .env for testing)
echo "✅ Checking API configuration..."
if [ -f "backend/.env" ]; then
    if grep -q "GEMINI_API_KEY" backend/.env && grep -q "SEALION_API_KEY" backend/.env; then
        echo "✅ API keys found in .env (remember to set these in Render dashboard)"
    else
        echo "⚠️  API keys not found in .env file"
    fi
else
    echo "⚠️  .env file not found (API keys will be set in Render dashboard)"
fi

echo ""
echo "🎯 Ready for deployment! Next steps:"
echo "1. Commit all changes to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Follow the RENDER_DEPLOYMENT.md guide"
echo "3. Create backend web service on Render"
echo "4. Create frontend static site on Render"
echo "5. Set environment variables in Render dashboard"
echo ""
echo "📖 Full guide: cat RENDER_DEPLOYMENT.md"
