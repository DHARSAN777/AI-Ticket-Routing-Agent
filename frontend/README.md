# 🎫 Ticket Agent - Frontend

Modern, responsive web interface for AI-powered customer support ticket management.

## 📋 Overview

The Ticket Agent frontend is a clean, professional web application that allows users to:

✅ **Login with email** - Simple, passwordless email-based authentication  
✅ **Submit support tickets** - Describe issues with full context  
✅ **Get instant AI analysis** - See categorization, priority, and routing  
✅ **View ticket dashboard** - Track all submitted tickets  
✅ **Chat with AI** - Get support and answers in real-time  
✅ **Dark/Light theme** - Comfortable viewing in any environment  
✅ **Mobile responsive** - Works on desktop, tablet, and phone  

---

## 🚀 Quick Start

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Backend API running on `http://localhost:5000`

### Running the Frontend

#### Option 1: Using the Batch File (Windows)

```bash
# Double-click this file
open-app.bat
```

This opens the app in your default browser.

#### Option 2: Using Live Server (VS Code)

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"
4. Page opens at `http://127.0.0.1:5500`

#### Option 3: Manual - Using Python

```bash
cd frontend
python -m http.server 8000
```

Then open: `http://localhost:8000`

#### Option 4: Manual - Using Node.js

```bash
cd frontend
npx http-server
```

Then open the URL shown in terminal.

---

## 📖 User Guide

### 1. Login Page

**URL:** `login.html`

- Enter any email address
- Click "Send Login Link"
- For demo: Auto-login after 3 seconds
- You're logged in!

**Demo Emails (any email works):**
- `admin@example.com`
- `support@example.com`
- `user@example.com`
- Or enter your own email

### 2. Home Page

**URL:** `index.html`

Features:
- **Hero section** - Overview of the Ticket Agent
- **Live examples** - Click "Try →" to pre-fill ticket form with sample data
- **How it works** - 4-step process explanation
- **Capabilities** - 10 AI features performed automatically
- **Routing rules** - See team assignments
- **Prompt engineering demo** - Input/output example

### 3. Submit Ticket Page

**URL:** `ticket.html`

**Form Fields:**
- **Customer Name** - Your name (required)
- **Email Address** - Your email (required)
- **Customer Type** - Free/Premium/Enterprise (required)
- **Subject** - Brief issue summary (required)
- **Description** - Detailed explanation (required)
- **Category** - Auto-detect or manually select
- **Priority** - Auto-detect or manually select
- **Ticket ID** - Auto-generated

**After Submission:**
- Ticket sent to backend
- AI analyzes immediately
- Results show:
  - ✅ Detected category
  - ✅ Priority level
  - ✅ Assigned team
  - ✅ Support queue
  - ✅ Customer sentiment
  - ✅ AI confidence score
  - ✅ Suggested response
  - ✅ Recommended tags
  - ✅ Raw JSON output

### 4. Dashboard Page

**URL:** `dashboard.html`

- View all submitted tickets
- Filter by status (Open, Closed, In Progress)
- Click ticket to see full details
- Update ticket status
- Export ticket data

### 5. Chat Page

**URL:** `chat.html`

- Chat with AI assistant
- Get instant responses
- Ask questions about tickets
- Get support tips and tricks

---

## 🎨 Styling & Themes

### CSS Files

1. **css/style.css** - Main stylesheet (1000+ lines)
   - Grid layouts
   - Color schemes
   - Responsive design
   - Component styles
   - Animations (removed)
   - Theme system

2. **styles.css** - Legacy/legacy stylesheet

### Theme Toggle

- Button in navbar: "☀️ Light" / "🌙 Dark"
- Theme preference saved in localStorage
- Switches between light (white) and dark (dark slate) modes

### Color Palette

**Light Mode:**
- Background: White
- Text: Dark gray
- Accents: Blue/Purple gradients

**Dark Mode:**
- Background: Slate-900
- Text: Light gray
- Accents: Same gradients

---

## 🔌 Backend Integration

### API Configuration

**File:** `js/app.js`

```javascript
const API_BASE = 'http://localhost:5000';
```

Change this if your backend runs on a different URL.

### Key API Endpoints Used

| Action | Endpoint | Method |
|--------|----------|--------|
| Login | `/auth/login` | POST |
| Get current user | `/auth/me` | GET |
| Create ticket | `/tickets` | POST |
| Get all tickets | `/tickets` | GET |
| Get single ticket | `/tickets/{id}` | GET |
| Update status | `/tickets/{id}/status` | PATCH |

### CORS Requirements

Backend must have CORS enabled:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📁 File Structure

```
frontend/
├── index.html              # Home page
├── login.html              # Login page
├── ticket.html             # Ticket submission page
├── dashboard.html          # Dashboard/view tickets
├── chat.html               # Chat with AI
├── app.js                  # Legacy app file
├── styles.css              # Legacy stylesheet
├── README.md               # This file
├── css/
│   └── style.css           # Main stylesheet (1200+ lines)
└── js/
    ├── app.js              # Core JavaScript functions
    ├── chat.js             # Chat functionality
    └── theme.js            # Theme toggle logic
```

---

## 🔐 Authentication System

### How It Works

1. User enters email on login page
2. Frontend simulates sending a "login link"
3. For demo: Auto-login after 3 seconds
4. User data stored in `sessionStorage`
5. Access token stored in `localStorage`
6. User redirected to home page

### Session Storage

```javascript
// User info
sessionStorage.setItem('user', JSON.stringify({
  email: 'user@example.com',
  name: 'User Name',
  loginMethod: 'email_link'
}));

// Auth token
localStorage.setItem('access_token', 'token-value');
```

### Protected Pages

All pages check for login:

```javascript
<script>
  if (!sessionStorage.getItem('user')) {
    window.location.href = 'login.html';
  }
</script>
```

If user not logged in → redirected to login page

---

## 🎫 Ticket Submission Flow

### Step 1: Fill Form

```
Customer Name:    John Doe
Email:            john@example.com
Customer Type:    Enterprise
Subject:          Cannot login after update
Description:      After the latest update I can't...
Category:         Auto-detect (or select manually)
Priority:         Auto-detect (or select manually)
```

### Step 2: Submit

Click "🚀 Submit & Analyze with AI"

### Step 3: Backend Processing

Backend receives ticket and:
1. Validates all fields
2. Analyzes ticket content
3. Detects category, priority, sentiment
4. Assigns team and queue
5. Generates tags and suggestions
6. Calculates confidence score
7. Returns full analysis

### Step 4: Display Results

Frontend shows:
- Ticket ID
- All AI analysis results
- Confidence score with visual bar
- Suggested response
- Recommended tags
- Option to download JSON

### Step 5: Actions

- "➕ New Ticket" - Reset form and submit another
- "📊 View Dashboard" - See all tickets

---

## 📱 Responsive Design

### Breakpoints

- **Desktop:** 1024px+ (full layout)
- **Tablet:** 768px - 1023px (adjusted grid)
- **Mobile:** < 768px (stacked layout)

### Mobile Features

✅ Touch-friendly buttons  
✅ Readable text at all sizes  
✅ Optimized form inputs  
✅ Collapsible navigation  
✅ Single-column layouts  

---

## 🔍 Browser Support

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full support |
| Firefox | ✅ Full support |
| Safari | ✅ Full support |
| Edge | ✅ Full support |
| IE 11 | ❌ Not supported |

---

## 🚨 Troubleshooting

### Page Redirects to Login

**Problem:** Even though I'm logged in, I keep going to login page

**Solution:**
1. Check browser console (F12)
2. Check sessionStorage has `user` key
3. Make sure `localStorage` has `access_token`
4. Clear browser cache and try again

### Backend Connection Failed

**Problem:** "Cannot connect to backend" error

**Solution:**
1. Make sure backend is running: `uvicorn main_simple:app --host 0.0.0.0 --port 5000`
2. Check API_BASE in `js/app.js` points to correct URL
3. Check backend CORS is enabled
4. Try `http://localhost:5000/health` in browser

### Form Won't Submit

**Problem:** Submit button doesn't respond

**Solution:**
1. Check all required fields are filled
2. Open browser console (F12) for error messages
3. Check backend is accessible
4. Try submitting with demo data

### Styling Looks Wrong

**Problem:** Page looks broken or unstyled

**Solution:**
1. Hard refresh browser: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
2. Clear browser cache
3. Check `css/style.css` is being loaded (F12 > Network)
4. Check for console errors

### Dark Mode Not Toggling

**Problem:** Theme button doesn't work

**Solution:**
1. Enable localStorage in browser
2. Check browser console for errors
3. Click button multiple times
4. Refresh page

---

## 🔧 Customization

### Change Backend URL

Edit `frontend/js/app.js`:

```javascript
const API_BASE = 'http://your-backend-url:5000';
```

### Change Logo/Branding

Search for `🎫` emoji and replace with your own:

```html
<!-- In navbar -->
<div class="nav-brand-icon">🎫</div>

<!-- Or replace with image -->
<img src="logo.png" alt="Logo" class="nav-brand-icon">
```

### Change Color Theme

Edit `frontend/css/style.css`:

```css
/* Find color variables */
--primary-color: #667eea;
--secondary-color: #764ba2;
--success-color: #34d399;
--danger-color: #ef4444;
```

### Add New Pages

1. Create `new-page.html`
2. Include navbar at top:
   ```html
   <script>if (!sessionStorage.getItem('user')) window.location.href = 'login.html';</script>
   <nav class="navbar">...</nav>
   ```
3. Link from navbar

### Modify AI Analysis Display

Edit the `renderResult()` function in `ticket.html`:

```javascript
function renderResult(data, payload) {
  // Customize what information is displayed
  // Add new fields, change formatting, etc.
}
```

---

## 📊 Sample Data

### Sample Tickets (on Home Page)

Pre-filled examples to test:

1. 💬 "I forgot my password and can't log in." → Login Issue
2. 💬 "My payment failed and I was charged twice." → Billing
3. 💬 "The website is loading very slowly." → Technical
4. 💬 "I want a refund for my last purchase." → Refund
5. 💬 "I think my account has been hacked." → Security (Critical)
6. 💬 "Can you add dark mode to the app?" → Feature Request
7. 💬 "The export button crashes the app." → Bug
8. 💬 "My package hasn't arrived after 2 weeks." → Shipping

Click "Try →" on any row to auto-fill the ticket form.

---

## 🎯 Key Features Implemented

### ✅ Complete Features

- [x] Email-based login
- [x] Ticket submission form
- [x] AI analysis display
- [x] Dashboard with ticket list
- [x] Status updates
- [x] Dark/light theme
- [x] Mobile responsive
- [x] Live sample tickets
- [x] Confidence scoring
- [x] Sentiment analysis display
- [x] Team assignment
- [x] Priority detection
- [x] Tag recommendations
- [x] Suggested responses
- [x] Export JSON
- [x] Chat interface
- [x] Navigation bar
- [x] Error handling
- [x] Form validation
- [x] Session management

---

## 🚀 Performance Tips

### Optimize Load Time

1. **Minimize HTTP requests** - CSS and JS already combined
2. **Enable gzip compression** - Configure on your web server
3. **Cache static assets** - Set Cache-Control headers
4. **Lazy load images** - Add `loading="lazy"` to images
5. **Minify CSS/JS** - For production deployment

### Browser Caching

Add to `.htaccess` or web server config:

```
Cache-Control: public, max-age=31536000
```

---

## 📈 Analytics Integration

To add Google Analytics:

1. Get your tracking ID from Google Analytics
2. Add to `index.html` (before closing `</head>`):

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-ID');
</script>
```

---

## 🔐 Security Best Practices

✅ **HTTPS only** - Always use HTTPS in production  
✅ **Secure tokens** - Store in secure storage  
✅ **Input validation** - All forms validated client-side  
✅ **XSS protection** - HTML escaped in templates  
✅ **CSRF tokens** - Implement for form submissions  
✅ **Rate limiting** - Implement on backend  

---

## 🤝 Integration Checklist

- [ ] Backend running on `http://localhost:5000`
- [ ] Frontend files accessible in browser
- [ ] Login page loads
- [ ] Can log in and access home page
- [ ] Can submit a ticket
- [ ] AI analysis displays correctly
- [ ] Dashboard shows tickets
- [ ] Dark mode works
- [ ] Mobile layout responsive
- [ ] No console errors (F12)

---

## 📚 Additional Resources

- [MDN Web Docs](https://developer.mozilla.org)
- [HTML5 Specification](https://html.spec.whatwg.org)
- [CSS Tricks](https://css-tricks.com)
- [JavaScript.info](https://javascript.info)
- [Web Accessibility](https://www.w3.org/WAI)

---

## 📞 Support

For issues:

1. **Check console errors** - Press F12, go to Console tab
2. **Verify backend is running** - Try `http://localhost:5000/health`
3. **Check network requests** - F12 > Network tab
4. **Review API response** - F12 > Network > Click request > Response tab
5. **Check file paths** - Make sure all HTML/CSS/JS files exist
6. **Clear cache** - `Ctrl+Shift+R` hard refresh

---

## 📄 License

MIT License - Feel free to use and modify this frontend for any purpose.

---

## 🎉 You're Ready!

Your Ticket Agent frontend is ready to use. Make sure:

1. ✅ Backend is running on port 5000
2. ✅ Frontend files are accessible
3. ✅ You're connected to the internet (or localhost)
4. ✅ Browser allows localStorage

**Now go submit some tickets and see the AI magic happen!** 🚀
