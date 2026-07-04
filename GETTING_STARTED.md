# 🚀 Getting Started with Ticket Agent

Your complete step-by-step guide to get Ticket Agent running in 5 minutes.

---

## ⚡ Super Quick Start (Windows)

1. **Open Command Prompt** or **PowerShell**
2. **Navigate to project folder:**
   ```bash
   cd "c:\Users\dhars\Downloads\project\ticket agent"
   ```
3. **Run start script:**
   ```bash
   START-HERE.bat
   ```
4. **Wait 30 seconds** for backend to start
5. **Browser opens automatically** with the app

That's it! You're done. Start submitting tickets! 🎉

---

## 📝 Detailed Setup (All Platforms)

### For Windows Users

#### Step 1: Check Python

Open **Command Prompt** and verify Python is installed:

```bash
python --version
```

You should see: `Python 3.8.0` or higher

**If not installed:**
- Download: https://www.python.org/downloads/
- Run installer
- ✅ Check "Add Python to PATH"

#### Step 2: Install Dependencies

Open **Command Prompt** in the backend folder:

```bash
cd backend
pip install -r requirements.txt
```

Wait for installation to complete. You should see green ✓ marks.

#### Step 3: Start Backend

Still in Command Prompt:

```bash
uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**Leave this window open!** This is your backend server.

#### Step 4: Start Frontend

Open **a new Command Prompt** and navigate to frontend:

```bash
cd frontend
python -m http.server 8000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8000...
```

#### Step 5: Open Browser

Click this link: **http://localhost:8000**

Or open your browser and type: `http://localhost:8000`

---

### For Mac/Linux Users

#### Step 1: Check Python

Open **Terminal** and verify Python is installed:

```bash
python3 --version
```

You should see: `Python 3.8.0` or higher

**If not installed on Mac:**
```bash
brew install python3
```

**If not installed on Linux:**
```bash
sudo apt-get install python3 python3-pip
```

#### Step 2: Install Dependencies

Open **Terminal** in the backend folder:

```bash
cd backend
pip3 install -r requirements.txt
```

Wait for installation to complete.

#### Step 3: Start Backend

Still in Terminal:

```bash
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**Leave this window open!** This is your backend server.

#### Step 4: Start Frontend

Open **a new Terminal** window and navigate to frontend:

```bash
cd frontend
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8000
```

#### Step 5: Open Browser

Open your browser and go to: **http://localhost:8000**

---

## 🌐 Using the App

### 1. Login Page

When you first open the app, you'll see the login page.

**What to do:**
1. Enter any email address (or use a test email)
2. Click **"📧 Send Login Link"**
3. Wait 3 seconds (auto-login in demo mode)
4. You're logged in! ✅

**Example emails to try:**
- `admin@example.com`
- `support@example.com`
- `user@example.com`
- Or enter your own email

### 2. Home Page

After login, you'll see the home page with:

- **Overview** - What Ticket Agent does
- **Sample Tickets** - Pre-filled examples
- **How It Works** - 4-step process
- **Features** - 10 AI capabilities
- **Routing Rules** - Team assignments

**Try this:**
- Scroll down to the **"Live Examples"** table
- Click **"Try →"** on any sample ticket
- The ticket form will auto-fill with that example

### 3. Submit a Ticket

Click **"➕ Submit Ticket"** or **"➕ Create Ticket"** in the navbar.

**Form fields:**
- **Customer Name** - Your name
- **Email Address** - Your email
- **Customer Type** - Free / Premium / Enterprise
- **Subject** - Brief problem summary
- **Description** - Detailed explanation
- **Category** - Auto-detect or select manually
- **Priority** - Auto-detect or select manually

**Example ticket:**
```
Name:        John Doe
Email:       john@example.com
Type:        Enterprise
Subject:     Cannot login after update
Description: After the latest update I cannot log into my account. 
             It keeps showing "authentication failed". This is blocking 
             my whole team from working.
```

Click **"🚀 Submit & Analyze with AI"**

### 4. See AI Analysis

The backend instantly analyzes your ticket and shows:

✅ **Category** - Auto-detected (Login Issue)  
✅ **Priority** - Auto-detected (High)  
✅ **Sentiment** - Customer mood (Frustrated)  
✅ **Assigned Team** - Who should handle it (Technical Support)  
✅ **Support Queue** - Specific queue (Authentication)  
✅ **AI Confidence** - How sure (97%)  
✅ **Suggested Response** - What to say to customer  
✅ **Tags** - Auto-generated (#login, #auth, #urgent)  

### 5. View Dashboard

Click **"📊 Dashboard"** in navbar to see all submitted tickets.

Features:
- View all tickets
- See ticket status
- Filter by status
- Click ticket for details
- Update ticket status

---

## 🔧 Configuration

### Change Backend URL

If backend is running on different port or machine:

**Edit:** `frontend/js/app.js`

Find this line:
```javascript
const API_BASE = 'http://localhost:5000';
```

Change `5000` to your port or URL:
```javascript
const API_BASE = 'http://localhost:5001';  // Different port
const API_BASE = 'http://192.168.1.5:5000';  // Different machine
const API_BASE = 'https://api.example.com';  // Remote server
```

Then refresh the browser page.

### Change Frontend Port

If port 8000 is already in use:

```bash
# Use port 8001 instead
python -m http.server 8001
```

Then open: **http://localhost:8001**

### Change Backend Port

If port 5000 is already in use:

```bash
# Use port 5001 instead
uvicorn main_simple:app --host 0.0.0.0 --port 5001
```

Then update `API_BASE` in frontend accordingly.

---

## 🎯 Test Workflow

Follow this to test the complete system:

### Test 1: Login
- [ ] Open app
- [ ] Enter email
- [ ] Click "Send Login Link"
- [ ] Wait for auto-login
- [ ] Should see home page

### Test 2: View Home Page
- [ ] See "Ticket Agent" heading
- [ ] See sample tickets table
- [ ] See "How It Works" section
- [ ] See features and routing rules

### Test 3: Try Sample Ticket
- [ ] Click "Try →" on any sample
- [ ] Should auto-fill ticket form
- [ ] Click "Submit & Analyze"
- [ ] Should see AI results

### Test 4: Submit Custom Ticket
- [ ] Fill in custom ticket details
- [ ] Click "Submit & Analyze"
- [ ] Should see AI analysis
- [ ] Click "View Dashboard"
- [ ] Should see ticket in list

### Test 5: Update Status
- [ ] On dashboard, click a ticket
- [ ] See ticket details
- [ ] Change status (if available)
- [ ] Verify change saved

### Test 6: Dark Mode
- [ ] Click light/dark toggle in navbar
- [ ] Page should change colors
- [ ] Toggle back to light mode
- [ ] Should switch back

**If all tests pass:** ✅ Everything works!

---

## ⚠️ Troubleshooting

### Problem: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

Wait for all packages to install, then try again.

### Problem: Port already in use

**Error:** `Address already in use`

**Solution:**

Find what's using the port:

**Windows:**
```bash
netstat -ano | findstr :5000
```

**Mac/Linux:**
```bash
lsof -i :5000
```

Then either:
1. Stop the other process
2. Use a different port (see Configuration section above)

### Problem: Frontend can't connect to backend

**Error:** `Failed to fetch` or connection timeout

**Solution:**

1. **Check backend is running:**
   ```bash
   # In browser, visit:
   http://localhost:5000/health
   ```
   Should show: `{"status": "healthy", "tickets": 0}`

2. **Check API_BASE URL:**
   - Open `frontend/js/app.js`
   - Verify `API_BASE = 'http://localhost:5000'`
   - Refresh browser

3. **Check firewall:**
   - Make sure Windows Firewall isn't blocking ports
   - Try disabling temporarily to test

### Problem: Keeps redirecting to login

**Error:** Always sent back to login.html

**Solution:**

1. **Enable localStorage:**
   - Chrome/Firefox: Settings > Privacy > Storage
   - Make sure localStorage is enabled

2. **Clear browser data:**
   - Press `Ctrl+Shift+Delete`
   - Clear cache and storage
   - Try again

3. **Check console for errors:**
   - Press `F12` to open DevTools
   - Go to "Console" tab
   - Look for red error messages

### Problem: Form won't submit

**Error:** Button doesn't respond

**Solution:**

1. **Check all fields are filled:**
   - All marked with `*` are required
   - Customer Name (required)
   - Email (required)
   - Customer Type (required)
   - Subject (required)
   - Description (required)

2. **Check backend is running:**
   - Visit `http://localhost:5000/health`
   - Should return success

3. **Open DevTools:**
   - Press `F12`
   - Go to "Network" tab
   - Try submitting
   - Look for the `/tickets` request
   - Check response for error

### Problem: Styling looks wrong

**Error:** Page looks unstyled or broken

**Solution:**

1. **Hard refresh:**
   - Windows: `Ctrl+Shift+R`
   - Mac: `Cmd+Shift+R`

2. **Clear cache:**
   - Close browser completely
   - Open again
   - Visit page

3. **Check CSS is loading:**
   - Press `F12`
   - Go to "Network" tab
   - Look for `style.css`
   - Should show 200 status code

### Problem: Python not found

**Error:** `'python' is not recognized` (Windows) or command not found (Mac/Linux)

**Solution:**

**Windows:**
- Reinstall Python from https://www.python.org
- ✅ Check "Add Python to PATH"
- Restart Command Prompt

**Mac/Linux:**
- Use `python3` instead of `python`
- Or install Python: `brew install python3` (Mac) or `sudo apt-get install python3` (Linux)

---

## 📚 Next Steps

After getting the app running:

1. **Explore the Code:**
   - Open `backend/main_simple.py` to see API
   - Open `frontend/ticket.html` to see form logic
   - Check `frontend/css/style.css` for styling

2. **Customize:**
   - Add your own company logo
   - Change color theme
   - Add more ticket categories
   - Modify AI analysis rules

3. **Connect Database:**
   - See `backend/README.md`
   - Instructions for MongoDB connection
   - For persistent data storage

4. **Deploy:**
   - Deploy backend to Heroku, AWS, or Docker
   - Deploy frontend to Netlify, Vercel, or GitHub Pages
   - See README files for deployment guides

5. **Integrate:**
   - Connect to Slack for notifications
   - Send emails via SendGrid
   - Sync with CRM systems
   - Add real AI with OpenAI API

---

## 🎓 Learning Resources

### Backend (FastAPI)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Python Docs](https://docs.python.org/3/)
- [Uvicorn](https://www.uvicorn.org)

### Frontend (HTML/CSS/JavaScript)
- [MDN Web Docs](https://developer.mozilla.org)
- [JavaScript.info](https://javascript.info)
- [CSS Tricks](https://css-tricks.com)
- [HTML5 Spec](https://html.spec.whatwg.org)

### AI/NLP
- [Wikipedia: NLP](https://en.wikipedia.org/wiki/Natural_language_processing)
- [Wikipedia: Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis)

---

## ✨ You Did It!

You now have a fully functional AI ticket routing system! 🎉

**Next time you want to use it:**

**Windows:**
```bash
START-HERE.bat
```

**Mac/Linux:**
```bash
# Terminal 1
cd backend
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000

# Terminal 2
cd frontend
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

---

## 🆘 Still Need Help?

1. **Check the README files:**
   - `backend/README.md` - API documentation
   - `frontend/README.md` - UI documentation
   - `README.md` - Project overview

2. **Check the code comments:**
   - `backend/main_simple.py` - Well commented
   - `frontend/ticket.html` - Detailed comments
   - `frontend/js/app.js` - Function explanations

3. **Check browser DevTools:**
   - Press `F12` to open
   - Console tab for errors
   - Network tab for requests
   - Application tab for storage

4. **Common issues section above:**
   - Most problems covered
   - With solutions ready to copy/paste

---

**Happy ticketing!** 🎫

Feel free to customize and extend this system. It's yours to play with!

Version 1.0.0 | Last Updated: January 2025
