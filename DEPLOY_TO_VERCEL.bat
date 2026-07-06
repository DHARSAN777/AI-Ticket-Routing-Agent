@echo off
echo.
echo ========================================
echo   AI Ticket Agent - Vercel Deployment
echo ========================================
echo.

echo Step 1: Adding all files to Git...
git add .

echo Step 2: Committing changes...
git commit -m "Prepare for Vercel deployment with backend and frontend"

echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   DEPLOYMENT READY!
echo ========================================
echo.
echo Next steps:
echo 1. Go to vercel.com/dashboard
echo 2. Click "New Project"  
echo 3. Import your GitHub repository
echo 4. Add environment variables:
echo    - GEMINI_API_KEY=your_api_key
echo    - MONGODB_URL=mongodb://localhost:27017
echo    - ENVIRONMENT=production
echo 5. Click Deploy
echo.
echo Your app will be live at: https://your-project-name.vercel.app
echo.
pause