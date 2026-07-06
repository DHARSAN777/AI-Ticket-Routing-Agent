# 🚀 Vercel Deployment Guide - AI Ticket Routing Agent

This guide will help you deploy both the frontend and backend to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```
3. **GitHub Repository**: Your code should be in a GitHub repository

## 🔧 Pre-Deployment Setup

### 1. Environment Variables
You'll need to set these environment variables in Vercel:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `MONGODB_URL`: MongoDB connection string (or use `mongodb://localhost:27017` for demo)
- `ENVIRONMENT`: Set to `production`

### 2. Project Structure
Your project is already configured with:
- ✅ `vercel.json` - Deployment configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `api/index.py` - Serverless API handler
- ✅ Frontend files in `/frontend/` directory

## 🚀 Deployment Methods

### Method 1: GitHub Integration (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Select your repository: `AI-Ticket-Routing-Agent`

3. **Configure Build Settings**:
   - Framework Preset: **Other**
   - Root Directory: **Leave empty** (uses root)
   - Build Command: **Leave default**
   - Output Directory: **Leave default**

4. **Add Environment Variables**:
   - In project settings, go to "Environment Variables"
   - Add:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     MONGODB_URL=mongodb://localhost:27017
     ENVIRONMENT=production
     ```

5. **Deploy**: Click "Deploy" button

### Method 2: Vercel CLI

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy**:
   ```bash
   cd "c:\Users\dhars\Downloads\project\ticket agent"
   vercel --prod
   ```

3. **Set Environment Variables**:
   ```bash
   vercel env add GEMINI_API_KEY
   vercel env add MONGODB_URL  
   vercel env add ENVIRONMENT
   ```

## 🔗 After Deployment

### Your URLs will be:
- **Frontend**: `https://your-project-name.vercel.app`
- **Backend API**: `https://your-project-name.vercel.app/api`

### Test the deployment:
1. **API Health Check**: Visit `https://your-project-name.vercel.app/api/`
2. **Frontend**: Visit `https://your-project-name.vercel.app`
3. **Login**: Go to `https://your-project-name.vercel.app/login.html`

## 🛠️ Troubleshooting

### Common Issues:

1. **Python Dependencies Error**:
   - Ensure `requirements.txt` is in the root directory
   - Check all dependencies are listed correctly

2. **API Not Working**:
   - Verify environment variables are set in Vercel dashboard
   - Check function logs in Vercel dashboard

3. **Frontend Not Loading**:
   - Ensure all frontend files are in `/frontend/` directory
   - Check `vercel.json` routes configuration

4. **CORS Issues**:
   - API is configured to allow all origins in production
   - If issues persist, check browser network tab

### Debug Steps:

1. **Check Vercel Function Logs**:
   - Go to Vercel dashboard > Your Project > Functions tab
   - Click on any function to see logs

2. **Test API Endpoints**:
   ```bash
   curl https://your-project-name.vercel.app/api/
   curl https://your-project-name.vercel.app/api/tickets
   ```

## 📱 Production URLs

Once deployed, your application will be available at:
- **Home**: `https://your-project-name.vercel.app`
- **Login**: `https://your-project-name.vercel.app/login.html`
- **Dashboard**: `https://your-project-name.vercel.app/dashboard.html`
- **Submit Ticket**: `https://your-project-name.vercel.app/ticket.html`

## 🔄 Redeployment

To update your deployment:
1. Make changes to your code
2. Push to GitHub: `git push origin main`
3. Vercel will automatically redeploy

## 🎉 Success!

Your AI Ticket Routing Agent is now live on Vercel with:
- ✅ Serverless backend API
- ✅ Static frontend hosting  
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic deployments from GitHub

## 📞 Need Help?

- Vercel Documentation: https://vercel.com/docs
- Vercel Discord: https://vercel.com/discord
- Check Vercel function logs for API issues