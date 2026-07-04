# 🔧 Installation Guide - Ticket Agent

Complete installation instructions for all operating systems.

---

## 📋 Prerequisites

Before installing Ticket Agent, make sure you have:

✅ **Python 3.8 or higher** - https://www.python.org/downloads/  
✅ **Git** (optional) - https://git-scm.com/  
✅ **Web Browser** - Chrome, Firefox, Safari, or Edge  
✅ **Text Editor** (optional) - VS Code, Sublime, etc.  

---

## 🪟 Windows Installation

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Click **"Download Python 3.11"** (or latest 3.x version)
3. Run the installer
4. ⚠️ **IMPORTANT:** Check ✓ **"Add Python to PATH"**
5. Click **"Install Now"**
6. Wait for installation to complete
7. Click **"Close"**

### Step 2: Verify Python Installation

Open **Command Prompt** (`cmd.exe`):

```bash
python --version
```

You should see: `Python 3.11.x` or similar

**If error:** "python is not recognized"
- Restart Command Prompt
- Or reinstall Python with "Add to PATH" checked

### Step 3: Extract Project Files

If you have a zip file:

1. Right-click the zip file
2. Select **"Extract All..."**
3. Choose destination folder
4. Click **"Extract"**

### Step 4: Install Backend Dependencies

Open **Command Prompt** and navigate to the backend:

```bash
cd path\to\ticket agent\backend
```

Install requirements:

```bash
pip install -r requirements.txt
```

You'll see packages being downloaded and installed. Wait for completion.

**Expected output:**
```
Successfully installed fastapi-0.111.0 uvicorn-0.29.0 pydantic-2.7.1 ...
```

### Step 5: Run the Application

**Option A: Using START-HERE.bat (Easiest)**

Navigate to project folder and double-click:
```
START-HERE.bat
```

This automatically:
- Installs dependencies
- Starts the backend
- Opens frontend in browser

**Option B: Manual Start**

Terminal 1 - Start Backend:
```bash
cd backend
uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

Terminal 2 - Start Frontend:
```bash
cd frontend
python -m http.server 8000
```

Then open browser: **http://localhost:8000**

---

## 🍎 Mac Installation

### Step 1: Check Python

Open **Terminal** and check if Python 3 is installed:

```bash
python3 --version
```

You should see: `Python 3.8.0` or higher

**If not installed:**

Using **Homebrew** (recommended):
```bash
brew install python3
```

Or download from: https://www.python.org/downloads/

### Step 2: Verify Installation

```bash
python3 --version
python3 -m pip --version
```

Both should show versions without errors.

### Step 3: Extract Project Files

If you have a zip file:

1. Double-click the zip file (auto-extracts)
2. Or use Terminal:
   ```bash
   unzip ticket-agent.zip
   cd ticket-agent
   ```

### Step 4: Install Backend Dependencies

Open **Terminal** and navigate to backend:

```bash
cd path/to/ticket\ agent/backend
```

Install requirements:

```bash
pip3 install -r requirements.txt
```

Wait for completion.

### Step 5: Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8000
```

### Step 6: Open Browser

Click or copy this link: **http://localhost:8000**

---

## 🐧 Linux Installation

### Step 1: Check Python

Open **Terminal** and verify Python:

```bash
python3 --version
```

You should see: `Python 3.8.0` or higher

**If not installed (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**If not installed (Fedora/RHEL):**
```bash
sudo dnf install python3 python3-pip
```

### Step 2: Verify Installation

```bash
python3 --version
python3 -m pip --version
```

### Step 3: Extract Project Files

```bash
unzip ticket-agent.zip
cd ticket-agent
```

Or if already extracted:
```bash
cd path/to/ticket-agent
```

### Step 4: Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

If permission denied:
```bash
pip3 install --user -r requirements.txt
```

### Step 5: Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```

### Step 6: Open Browser

Visit: **http://localhost:8000**

---

## 📦 Alternative: Using Virtual Environment (Recommended)

Virtual environments isolate your project dependencies.

### Windows

**Create virtual environment:**
```bash
cd backend
python -m venv venv
```

**Activate it:**
```bash
venv\Scripts\activate
```

**Install requirements:**
```bash
pip install -r requirements.txt
```

**Run backend:**
```bash
uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

### Mac/Linux

**Create virtual environment:**
```bash
cd backend
python3 -m venv venv
```

**Activate it:**
```bash
source venv/bin/activate
```

**Install requirements:**
```bash
pip3 install -r requirements.txt
```

**Run backend:**
```bash
python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000
```

---

## 🐳 Docker Installation (Advanced)

### Prerequisites

- Docker installed: https://www.docker.com/products/docker-desktop

### Build Docker Image

```bash
# Navigate to project root
cd ticket-agent

# Build image
docker build -t ticket-agent .
```

### Run Container

```bash
docker run -p 5000:5000 -p 8000:8000 ticket-agent
```

Then open: **http://localhost:8000**

### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/main_simple.py .
COPY frontend frontend/

CMD ["uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "5000"]
```

---

## ✅ Verify Installation

After installation, verify everything works:

### Check Backend

Open browser and visit:
```
http://localhost:5000/health
```

You should see:
```json
{
  "status": "healthy",
  "tickets": 0
}
```

### Check Frontend

Open browser and visit:
```
http://localhost:8000
```

You should see the Ticket Agent login page.

### Check API Documentation

Visit:
```
http://localhost:5000/docs
```

You should see the interactive Swagger documentation.

---

## 🐛 Troubleshooting Installation

### Error: "Python not found"

**Windows:**
1. Reinstall Python from https://www.python.org
2. ✅ Make sure "Add Python to PATH" is checked
3. Restart Command Prompt
4. Try again

**Mac/Linux:**
```bash
# Use python3 instead of python
python3 --version
```

### Error: "pip not found"

**Windows:**
```bash
python -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: fastapi"

```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

Or with virtual environment:
```bash
# Create new virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Error: "Address already in use"

Port 5000 or 8000 is already being used.

**Change port:**

Backend - Use port 5001:
```bash
uvicorn main_simple:app --host 0.0.0.0 --port 5001
```

Frontend - Use port 8001:
```bash
python -m http.server 8001
```

Then update `frontend/js/app.js`:
```javascript
const API_BASE = 'http://localhost:5001';
```

### Error: "Permission denied"

**Mac/Linux:**

Use `sudo` (not recommended) or use `--user` flag:
```bash
pip install --user -r requirements.txt
```

---

## 🔐 Security Best Practices

### Never Commit Secrets

Don't commit to Git:
- `.env` files with API keys
- Database credentials
- Private keys
- Passwords

Create `.gitignore`:
```
.env
.env.local
*.key
*.pem
__pycache__/
node_modules/
venv/
```

### Update Dependencies Regularly

```bash
pip install --upgrade -r requirements.txt
```

### Use Virtual Environment

Always use virtual environment for production:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 File Permissions (Linux/Mac)

Make scripts executable:

```bash
chmod +x backend/main_simple.py
chmod +x frontend/index.html
```

---

## 🚀 Next Steps After Installation

1. ✅ Verify installation (see above)
2. 📖 Read `GETTING_STARTED.md`
3. 🎯 Submit your first ticket
4. 📊 View dashboard
5. 🔧 Customize system
6. 🚀 Deploy to production

---

## 📞 Installation Support

### Common Issues

| Issue | Solution |
|-------|----------|
| Python not found | Reinstall with "Add to PATH" |
| ModuleNotFoundError | Run: `pip install -r requirements.txt` |
| Port in use | Use different port (5001, 8001) |
| Permission denied | Use: `pip install --user` |
| Virtual env issue | Delete `venv/` folder and recreate |

### Get Help

1. Check this file for your issue
2. Check `GETTING_STARTED.md`
3. Check `backend/README.md`
4. Check `frontend/README.md`

---

## 🎯 Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Files extracted to folder
- [ ] Backend dependencies installed
- [ ] Backend runs on port 5000
- [ ] Frontend runs on port 8000
- [ ] Health check shows ✅
- [ ] Login page loads
- [ ] Can submit ticket
- [ ] AI analysis works

---

## 🎉 Success!

If all checks pass, you're ready to use Ticket Agent!

**To use later:**

Windows:
```bash
START-HERE.bat
```

Mac/Linux:
```bash
# Terminal 1
cd backend && python3 -m uvicorn main_simple:app --host 0.0.0.0 --port 5000

# Terminal 2
cd frontend && python3 -m http.server 8000
```

Then open: **http://localhost:8000**

---

Version 1.0.0 | Last Updated: January 2025
