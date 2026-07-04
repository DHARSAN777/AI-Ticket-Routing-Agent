# 🎫 START HERE - Ticket Agent

**Welcome to Ticket Agent!** This file gets you started in the next 5 minutes.

---

## ⚡ Super Quick Start (Windows)

**This is the easiest way:**

1. **Double-click this file:**
   ```
   START-HERE.bat
   ```

2. **Wait 30 seconds** while it:
   - Installs dependencies
   - Starts the backend
   - Opens your browser

3. **You're done!** The app opens automatically.

---

## 📖 All You Need to Know (5 minutes)

### What is Ticket Agent?

An AI system that automatically:
- ✅ Analyzes customer support tickets
- ✅ Categorizes them (Billing, Technical, Security, etc.)
- ✅ Sets priority levels (Critical, High, Medium, Low)
- ✅ Routes to the correct team instantly
- ✅ Suggests responses to customers

**No AI API calls needed** - works completely offline!

---

## 🚀 Get Started in 5 Steps

### Step 1: Run the App (30 seconds)

**Windows:**
```bash
START-HERE.bat
```

**Mac/Linux:** Open Terminal and run:
```bash
cd backend
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000

# In new Terminal window
cd frontend
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

### Step 2: Login (10 seconds)

- Enter any email (e.g., `admin@example.com`)
- Click **"📧 Send Login Link"**
- Wait 3 seconds for auto-login

### Step 3: Submit a Ticket (60 seconds)

Click **"➕ Submit Ticket"** and fill in:
- **Customer Name:** John Doe
- **Email:** john@example.com
- **Type:** Enterprise
- **Subject:** Cannot login after update
- **Description:** After yesterday's update I can't log into my account...

Click **"🚀 Submit & Analyze"**

### Step 4: See AI Magic (2 seconds)

The AI instantly shows:
- ✅ **Category:** Login Issue
- ✅ **Priority:** High
- ✅ **Sentiment:** Frustrated
- ✅ **Team:** Technical Support
- ✅ **Confidence:** 97%
- ✅ **Suggested Response:** (ready to send)

### Step 5: Explore (2 minutes)

- Click **"📊 View Dashboard"** to see all tickets
- Click **"🏠 Home"** to see sample tickets
- Try clicking **"Try →"** on any sample to auto-fill the form
- Try **Dark Mode** (toggle in navbar)

---

## 📋 What Files Do What?

**Root Folder:**
- `README.md` - Project overview
- `GETTING_STARTED.md` - Step-by-step setup
- `QUICK_REFERENCE.md` - Quick commands
- `API_REFERENCE.md` - API documentation
- `DEPLOYMENT.md` - Deploy to production
- `INSTALLATION.md` - Detailed installation

**Backend Folder:**
- `backend/main_simple.py` - The API
- `backend/requirements.txt` - Dependencies
- `backend/README.md` - Backend docs
- `backend/.env` - Configuration

**Frontend Folder:**
- `frontend/index.html` - Home page
- `frontend/login.html` - Login page
- `frontend/ticket.html` - Ticket form
- `frontend/dashboard.html` - View tickets
- `frontend/README.md` - Frontend docs

---

## 🔑 Demo Credentials (Optional)

If not using email login, try these:

```
admin@example.com      / admin123
support@example.com    / support123
user@example.com       / user123
```

**Note:** In demo mode, any email works.

---

## 📱 What Can You Do?

### Immediately
- ✅ Login with any email
- ✅ Submit support tickets
- ✅ See instant AI analysis
- ✅ View ticket dashboard
- ✅ Change ticket status
- ✅ Toggle dark/light theme

### With Customization
- 🔧 Add your company logo
- 🎨 Change colors
- 📝 Add more ticket categories
- 🤖 Modify AI analysis rules
- 📧 Connect to database
- 🚀 Deploy to production

---

## 🐛 Troubleshooting

### It says "Can't connect to backend"

**Solution:** Make sure backend is running

**Windows:** Double-click `START-HERE.bat` again

**Mac/Linux:**
```bash
cd backend
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

### It says "Port already in use"

**Solution:** Use a different port

```bash
# Use port 5001 instead
uvicorn main_simple:app --port 5001

# Then update frontend/js/app.js line:
# const API_BASE = 'http://localhost:5001';
```

### Form won't submit

**Solution:** Fill in all required fields (marked with *)

- Customer Name (required)
- Email (required)
- Type (required)
- Subject (required)
- Description (required)

### Page looks broken

**Solution:** Hard refresh browser

- Windows/Linux: `Ctrl+Shift+R`
- Mac: `Cmd+Shift+R`

---

## 📚 Documentation Quick Links

| Need | Read This |
|------|-----------|
| Project overview | `README.md` |
| Step-by-step setup | `GETTING_STARTED.md` |
| Quick commands | `QUICK_REFERENCE.md` |
| Detailed setup | `INSTALLATION.md` |
| API docs | `API_REFERENCE.md` |
| Deploy to production | `DEPLOYMENT.md` |
| All files explained | `FILE_GUIDE.md` |

---

## 🎯 Next Steps

### Try These Now
1. Submit a few tickets
2. Try the sample tickets (Home page)
3. View the dashboard
4. Try dark mode

### Try These Later
1. Read `backend/README.md` to understand the API
2. Read `frontend/README.md` to customize the UI
3. Read `DEPLOYMENT.md` to deploy to production
4. Connect to a real database (MongoDB)

---

## 💡 Pro Tips

1. **Pre-filled forms:** Click "Try →" on any sample ticket
2. **Quick commands:** See `QUICK_REFERENCE.md`
3. **API testing:** Visit `http://localhost:5000/docs`
4. **Dark mode:** Better for eyes at night
5. **Copy JSON:** Right-click raw JSON to copy

---

## ✅ Launch Checklist

- [ ] Backend running ✓
- [ ] Frontend accessible ✓
- [ ] Can login ✓
- [ ] Can submit ticket ✓
- [ ] AI analysis works ✓
- [ ] Dashboard shows tickets ✓
- [ ] Dark mode works ✓

**If all checked:** You're ready to go! 🚀

---

## 🚀 You're All Set!

**That's it! You now have a fully functional AI ticket routing system.**

### Key URLs

| What | URL |
|------|-----|
| App | http://localhost:8000 |
| API | http://localhost:5000 |
| API Docs | http://localhost:5000/docs |
| Health Check | http://localhost:5000/health |

### Key Commands

```bash
# Start backend
uvicorn main_simple:app --host 0.0.0.0 --port 5000

# Start frontend
python -m http.server 8000

# Or on Windows, just double-click:
START-HERE.bat
```

---

## 🎓 Learn More

### For Beginners
- Read `GETTING_STARTED.md`
- Try all features
- Submit some tickets

### For Developers
- Read `backend/README.md`
- Read `frontend/README.md`
- Look at the code

### For DevOps
- Read `DEPLOYMENT.md`
- Choose a platform
- Deploy!

---

## 🤔 Questions?

### "How do I customize it?"
→ See `backend/README.md` and `frontend/README.md`

### "How do I deploy it?"
→ See `DEPLOYMENT.md`

### "What's the API?"
→ See `API_REFERENCE.md` or visit `/docs`

### "I'm stuck"
→ Check Troubleshooting section above

### "What else can I do?"
→ Read `README.md` for full feature list

---

## 🎉 Enjoy!

You now have a professional AI ticket routing system running locally!

**Questions?** Check the documentation files.  
**Ready to deploy?** Read `DEPLOYMENT.md`.  
**Ready to customize?** Read `backend/README.md` or `frontend/README.md`.

---

## 📞 Quick Reference Card

### Ports
- Backend: 5000
- Frontend: 8000

### Commands
- Windows: `START-HERE.bat`
- Mac/Linux: See GETTING_STARTED.md

### Files to Edit
- Backend: `backend/main_simple.py`
- Frontend: `frontend/index.html`, `frontend/ticket.html`
- Styling: `frontend/css/style.css`
- Config: `backend/.env`

### Key Endpoints
- Login: `POST /auth/login`
- Create Ticket: `POST /tickets`
- Get Tickets: `GET /tickets`
- View Docs: `GET /docs`

---

**Version 1.0.0 | Made for Support Teams Everywhere | January 2025**

🚀 **Now go build something awesome!**
