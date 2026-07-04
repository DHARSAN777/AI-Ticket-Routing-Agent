# 📖 Ticket Agent - Quick Reference Guide

Your at-a-glance guide to Ticket Agent. Keep this handy!

---

## 🚀 Quick Start (Copy & Paste)

### Windows
```bash
cd "c:\Users\dhars\Downloads\project\ticket agent"
START-HERE.bat
```

### Mac/Linux - Terminal 1
```bash
cd backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

### Mac/Linux - Terminal 2
```bash
cd frontend
python3 -m http.server 8000
```

**Then open:** http://localhost:8000

---

## 📁 Folder Structure

```
ticket-agent/
├── backend/              → API server (Python)
├── frontend/            → Web interface (HTML/JS)
└── README.md           → Full documentation
```

---

## 🔑 Key Ports

| Service | Port | URL |
|---------|------|-----|
| Backend API | 5000 | http://localhost:5000 |
| Frontend | 8000 | http://localhost:8000 |
| API Docs | 5000 | http://localhost:5000/docs |

---

## 📝 Demo Credentials

```
admin@example.com      / admin123
support@example.com    / support123
user@example.com       / user123
```

**Note:** Any email works in demo mode

---

## 🌐 Frontend Pages

| Page | File | Purpose |
|------|------|---------|
| Login | `login.html` | Email-based login |
| Home | `index.html` | Dashboard, sample tickets |
| Submit | `ticket.html` | Create tickets |
| Dashboard | `dashboard.html` | View all tickets |
| Chat | `chat.html` | AI chat assistant |

---

## 🔌 Main API Endpoints

### Authentication
```
POST   /auth/login         Login with email/password
GET    /auth/me            Get current user
```

### Tickets
```
POST   /tickets            Create ticket (with AI analysis)
GET    /tickets            Get all tickets
GET    /tickets/{id}       Get single ticket
PATCH  /tickets/{id}/status  Update ticket status
```

### System
```
GET    /                   API info
GET    /health             Health check
GET    /docs               Swagger UI (interactive docs)
```

---

## 🤖 AI Analysis Features

| Feature | What It Does |
|---------|------------|
| **Category** | Detects ticket type (15+ categories) |
| **Priority** | Sets urgency (Critical/High/Medium/Low) |
| **Sentiment** | Detects mood (Angry/Frustrated/Happy/Neutral) |
| **Team** | Routes to correct department |
| **Tags** | Auto-generates keywords |
| **Confidence** | 0-100% confidence score |

---

## 🎯 Category Examples

| Category | Keywords | Team |
|----------|----------|------|
| Billing | payment, charge, refund | Billing Team |
| Technical | error, crash, bug | Technical Support |
| Login | password, access, login | Tech Support |
| Security | hack, breach, unauthorized | Security Team |
| Shipping | delivery, package, tracking | Logistics |

---

## 🔒 Authentication Flow

```
1. User enters email on login page
2. Frontend simulates sending "login link"
3. For demo: Auto-login after 3 seconds
4. User data stored in sessionStorage
5. Access token stored in localStorage
6. User redirected to home page
```

---

## 📊 Ticket Submission Flow

```
1. User fills ticket form
2. Click "Submit & Analyze"
3. Frontend sends to backend
4. Backend analyzes ticket
5. AI determines category, priority, team
6. Results displayed immediately
7. User can save/export
```

---

## 🛠️ File Locations

| File | Location | Purpose |
|------|----------|---------|
| Backend API | `backend/main_simple.py` | Main API |
| Frontend JS | `frontend/js/app.js` | JavaScript functions |
| Styling | `frontend/css/style.css` | CSS styling |
| API Config | `frontend/js/app.js` | Set `API_BASE` here |
| Demo Emails | `backend/main_simple.py` | Line ~20 |

---

## ⚙️ Change API URL

**File:** `frontend/js/app.js`

**Find:**
```javascript
const API_BASE = 'http://localhost:5000';
```

**Change to:**
```javascript
const API_BASE = 'http://your-url:port';
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | `pip install -r backend/requirements.txt` |
| Port already in use | Use different port: `--port 5001` |
| Can't connect | Check backend: `http://localhost:5000/health` |
| Always redirected | Clear cache: `Ctrl+Shift+Delete` |
| Form won't submit | Fill all required fields (* marked) |
| Styling looks wrong | Hard refresh: `Ctrl+Shift+R` |
| Python not found | Reinstall Python with "Add to PATH" |

---

## 📱 Using the App

### Submit a Ticket
1. Click "➕ Submit Ticket"
2. Fill in form
3. Click "🚀 Submit & Analyze"
4. See AI results
5. Click "View Dashboard"

### View Dashboard
1. Click "📊 Dashboard"
2. See all tickets
3. Click ticket for details
4. Update status if needed

### Dark Mode
1. Click "☀️ Light" / "🌙 Dark" in navbar
2. Theme changes instantly
3. Preference saved

### Logout
1. Click "🚪 Logout" button
2. Sent back to login
3. Session cleared

---

## 💾 Browser Storage

**sessionStorage:**
```javascript
// User data
{
  email: "user@example.com",
  name: "User Name",
  loginMethod: "email_link"
}
```

**localStorage:**
```javascript
// Auth token
access_token: "token-value"

// Theme preference
theme: "dark" or "light"
```

---

## 📊 Example Ticket Request

```json
{
  "title": "Cannot login",
  "description": "After update, can't log in. Error: auth failed",
  "submitter_name": "John Doe",
  "submitter_email": "john@example.com",
  "customer_type": "Enterprise"
}
```

---

## 📊 Example AI Response

```json
{
  "category": "Login Issue",
  "priority": "High",
  "sentiment": "Frustrated",
  "assigned_team": "Technical Support",
  "support_queue": "AUTHENTICATION",
  "summary": "Customer cannot log in after update",
  "tags": ["login", "authentication"],
  "requires_human_review": false,
  "confidence_score": 0.92
}
```

---

## 🔧 Environment Variables

**File:** `backend/.env`

```
API_TITLE=Ticket Agent API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=5000
DEBUG=False
ALLOW_ORIGINS=*
```

---

## 📱 Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Desktop | 1024px+ | Full layout |
| Tablet | 768-1023px | Adjusted grid |
| Mobile | < 768px | Stacked |

---

## 🎨 Color Scheme

**Light Mode:**
- Background: White
- Text: Dark gray
- Primary: Blue/Purple

**Dark Mode:**
- Background: Slate-900
- Text: Light gray
- Primary: Blue/Purple (lighter)

---

## 📚 Documentation Files

| File | Contains |
|------|----------|
| README.md | Project overview |
| GETTING_STARTED.md | Step-by-step setup |
| QUICK_REFERENCE.md | This file |
| backend/README.md | API documentation |
| frontend/README.md | Frontend guide |

---

## 🚀 Deployment Commands

### Heroku
```bash
git push heroku main
```

### Docker
```bash
docker build -t ticket-agent .
docker run -p 5000:5000 ticket-agent
```

### Manual Python
```bash
python -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

---

## 📞 Common Tasks

### Add New Demo User
**File:** `backend/main_simple.py`, line ~20

```python
"new@example.com": {"password": "password123", "name": "New User"},
```

### Change Theme Colors
**File:** `frontend/css/style.css`, search for `--primary-color`

```css
--primary-color: #667eea;
--secondary-color: #764ba2;
```

### Add New Ticket Category
**File:** `backend/main_simple.py`, `analyze_ticket_mock()` function

```python
"New Category": ["keyword1", "keyword2", "keyword3"],
```

### Change API Port
**Terminal:**
```bash
uvicorn main_simple:app --port 5001
```

Then update `frontend/js/app.js`:
```javascript
const API_BASE = 'http://localhost:5001';
```

---

## ✅ Pre-Launch Checklist

- [ ] Backend installed: `pip install -r requirements.txt`
- [ ] Backend running: `http://localhost:5000/health` returns ✅
- [ ] Frontend accessible: `http://localhost:8000` loads
- [ ] Can login with test email
- [ ] Can submit ticket
- [ ] AI analysis displays correctly
- [ ] Dashboard shows tickets
- [ ] Dark mode toggles
- [ ] No errors in console (F12)
- [ ] No network errors in DevTools

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F12` | Open DevTools |
| `Ctrl+Shift+R` | Hard refresh (clear cache) |
| `Ctrl+Shift+Delete` | Clear browser data |
| `Escape` | Close modal/form |

---

## 📱 Mobile Tips

- Use responsive design
- Tap-friendly buttons (44px minimum)
- Readable text at all zoom levels
- Forms work on mobile keyboard
- Dark mode better for battery

---

## 🔐 Security Quick Tips

✅ Use HTTPS in production  
✅ Never commit secrets to git  
✅ Validate input on backend  
✅ Use secure token storage  
✅ Enable CORS only for trusted origins  
✅ Rate limit API endpoints  
✅ Monitor for suspicious activity  

---

## 📈 Performance Tips

- Minify CSS/JS for production
- Enable gzip compression
- Cache static assets
- Use CDN for images
- Optimize database queries
- Monitor API response times

---

## 🤝 Quick Git Commands

```bash
# Clone
git clone <repo-url>

# Create branch
git checkout -b feature/my-feature

# Commit
git add .
git commit -m "Add feature"

# Push
git push origin feature/my-feature

# Create PR
# (Use GitHub/GitLab interface)
```

---

## 📞 Help Resources

| Resource | URL |
|----------|-----|
| FastAPI Docs | https://fastapi.tiangolo.com |
| Python Docs | https://docs.python.org/3/ |
| MDN Web Docs | https://developer.mozilla.org |
| Stack Overflow | https://stackoverflow.com |
| This Project | See README.md files |

---

## 💡 Tips & Tricks

1. **Pre-fill forms:** Click "Try →" on sample tickets
2. **Dark mode:** Better for eyes at night
3. **Copy JSON:** Right-click > Copy on raw JSON output
4. **Filter tickets:** Dashboard supports filtering
5. **Keyboard shortcuts:** DevTools (F12), hard refresh (Ctrl+Shift+R)
6. **Check logs:** Terminal shows what's happening
7. **Monitor network:** DevTools > Network tab
8. **Test endpoints:** Use http://localhost:5000/docs

---

## 🎓 Learning Path

1. **Day 1:** Get running (START-HERE.bat)
2. **Day 2:** Submit tickets, explore dashboard
3. **Day 3:** Try sample tickets, test AI analysis
4. **Day 4:** Read backend/README.md
5. **Day 5:** Read frontend/README.md
6. **Day 6:** Look at code, understand flows
7. **Day 7:** Customize and deploy

---

## 📝 Notes Template

When taking notes:

```markdown
## Issue: [Problem]
- When: [When it happens]
- Error: [Error message]
- Steps to reproduce: [Steps]
- Expected: [What should happen]
- Actual: [What actually happened]
- Solution: [How you fixed it]
```

---

**Print this page for quick reference!**

Version 1.0.0 | Last Updated: January 2025

---

## 🎉 You're Ready!

Everything you need to know is here. Start with one of these:

1. **New to Ticket Agent?** → Read GETTING_STARTED.md
2. **Want to customize?** → Read backend/README.md and frontend/README.md
3. **Just need quick answers?** → You're already reading it!

Go build something amazing! 🚀
