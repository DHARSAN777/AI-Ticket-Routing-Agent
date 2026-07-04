# 🚀 Deployment Guide - Ticket Agent

Complete guide to deploy Ticket Agent to production.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All tests pass locally
- [ ] No hardcoded credentials
- [ ] `.env` configured for production
- [ ] Database ready (if using)
- [ ] SSL certificate obtained (for HTTPS)
- [ ] Domain name configured
- [ ] Error monitoring set up (Sentry, LogRocket)
- [ ] Backups configured
- [ ] Security headers configured

---

## 🌐 Deployment Options

### Option 1: Heroku (Easiest)

Heroku is the simplest way to deploy without managing servers.

#### Prerequisites

- Heroku account: https://heroku.com
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

#### Step 1: Create Heroku App

```bash
heroku login
heroku create your-ticket-agent
```

#### Step 2: Create Procfile

In project root, create `Procfile`:

```
web: cd backend && uvicorn main_simple:app --host 0.0.0.0 --port $PORT
release: python -m pip install -r requirements.txt
```

#### Step 3: Create runtime.txt

```
python-3.11.7
```

#### Step 4: Deploy

```bash
git push heroku main
```

#### Step 5: View Logs

```bash
heroku logs --tail
```

#### Access App

```
https://your-ticket-agent.herokuapp.com
```

---

### Option 2: Docker + AWS EC2

Deploy containerized app on AWS.

#### Prerequisites

- AWS account
- Docker installed
- EC2 instance running Ubuntu

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy frontend
COPY frontend/ ./frontend/

EXPOSE 5000

CMD ["uvicorn", "backend.main_simple:app", "--host", "0.0.0.0", "--port", "5000"]
```

#### Step 2: Create Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEBUG=False
      - HOST=0.0.0.0
      - PORT=5000
    volumes:
      - ./backend:/app/backend

  frontend:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - api
```

#### Step 3: Build and Push to Registry

```bash
docker build -t ticket-agent:latest .
docker tag ticket-agent:latest your-registry/ticket-agent:latest
docker push your-registry/ticket-agent:latest
```

#### Step 4: SSH into EC2 and Pull

```bash
ssh -i key.pem ec2-user@your-instance-ip
docker pull your-registry/ticket-agent:latest
docker run -d -p 5000:5000 your-registry/ticket-agent:latest
```

---

### Option 3: DigitalOcean App Platform

Simple deployment without Docker management.

#### Step 1: Push to GitHub

```bash
git remote add origin https://github.com/your-repo/ticket-agent.git
git push -u origin main
```

#### Step 2: Connect DigitalOcean

1. Go to DigitalOcean > App Platform
2. Click "Create App"
3. Select GitHub repository
4. Select branch: `main`
5. Add environment variables
6. Deploy

#### Step 3: Configure

Add environment variables in DigitalOcean dashboard:

```
DEBUG=False
HOST=0.0.0.0
PORT=8080
ALLOW_ORIGINS=https://yourdomain.com
```

---

### Option 4: Railway

Simple deployment with automatic scaling.

#### Step 1: Connect GitHub

1. Go to railway.app
2. Connect GitHub account
3. Select repository

#### Step 2: Configure

1. Add `railway.json`:

```json
{
  "build": {
    "builder": "dockerfile"
  }
}
```

2. Add environment variables in Railway dashboard
3. Deploy

---

### Option 5: Manual VPS (Advanced)

For full control using Nginx, Gunicorn, and Supervisor.

#### Prerequisites

- Linux VPS (Ubuntu 20.04+)
- SSH access
- Domain name

#### Step 1: Connect via SSH

```bash
ssh root@your-vps-ip
```

#### Step 2: Install Dependencies

```bash
apt-get update
apt-get install -y python3 python3-pip nginx supervisor certbot python3-certbot-nginx
```

#### Step 3: Deploy Code

```bash
cd /var/www
git clone https://github.com/your-repo/ticket-agent.git
cd ticket-agent/backend
pip install -r requirements.txt
```

#### Step 4: Create Gunicorn Service

Create `/etc/systemd/system/ticket-agent.service`:

```ini
[Unit]
Description=Ticket Agent API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ticket-agent/backend
ExecStart=/usr/bin/python3 -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker main_simple:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable ticket-agent
systemctl start ticket-agent
```

#### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/ticket-agent`:

```nginx
upstream ticket_agent {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://ticket_agent;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/ticket-agent/frontend;
    }
}
```

Enable site:

```bash
ln -s /etc/nginx/sites-available/ticket-agent /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### Step 6: Enable HTTPS

```bash
certbot --nginx -d your-domain.com
```

---

## 🔐 Production Configuration

### Environment Variables

Create `.env` file with production values:

```
# API Configuration
DEBUG=False
HOST=0.0.0.0
PORT=5000

# Database
MONGODB_URL=mongodb://user:password@mongo-host:27017/ticket-agent
DATABASE_NAME=ticket_agent

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security
SECRET_KEY=your-very-long-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CORS
ALLOW_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-key@sentry.io/project-id
```

### Security Headers

Configure Nginx to add security headers:

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### CORS Configuration

Update `backend/main_simple.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Database Setup

### MongoDB Atlas (Managed)

#### Step 1: Create Cluster

1. Go to mongodb.com/cloud
2. Create account
3. Create cluster
4. Configure network access

#### Step 2: Get Connection String

```
mongodb+srv://username:password@cluster.mongodb.net/ticket-agent?retryWrites=true
```

#### Step 3: Update Environment

```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ticket-agent
```

#### Step 4: Update Backend

In `backend/main_simple.py`:

```python
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["ticket_agent"]

@app.post("/tickets")
async def create_ticket(ticket: TicketCreate):
    # Save to MongoDB instead of in-memory
    result = await db.tickets.insert_one(ticket.dict())
    # ...
```

---

## 📈 Monitoring & Logging

### Sentry (Error Tracking)

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)
```

### Prometheus (Metrics)

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Access metrics at: `http://localhost:5000/metrics`

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      
      - name: Run tests
        run: pytest backend/tests/
      
      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git push heroku main
```

---

## 🔄 Scaling

### Horizontal Scaling

Use load balancer:

```nginx
upstream backend {
    server 10.0.1.1:5000;
    server 10.0.1.2:5000;
    server 10.0.1.3:5000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### Vertical Scaling

Increase resources:
- CPU cores
- RAM
- Disk space
- Database connections

### Database Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

---

## 🔒 SSL/HTTPS

### Let's Encrypt (Free)

```bash
certbot certonly --webroot -w /var/www/ticket-agent/frontend -d yourdomain.com
```

Nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of config
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

---

## 📊 Backup Strategy

### Database Backups

```bash
# Backup MongoDB
mongodump --uri "mongodb://user:password@host/ticket-agent" --out /backups/

# Restore MongoDB
mongorestore --uri "mongodb://user:password@host/ticket-agent" /backups/
```

### Automated Daily Backups

```bash
# Add to crontab
0 2 * * * /usr/local/bin/backup-ticket-agent.sh
```

---

## 📞 Post-Deployment

### Verify Deployment

```bash
# Check health
curl https://yourdomain.com/health

# Check API docs
curl https://yourdomain.com/docs

# Test login
curl -X POST https://yourdomain.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### Setup Monitoring

1. Setup uptime monitoring (UptimeRobot, Pingdom)
2. Setup error tracking (Sentry)
3. Setup log aggregation (CloudWatch, ELK)
4. Setup performance monitoring (New Relic)

### Configure Alerts

- CPU > 80%
- Memory > 80%
- Errors > 10 per minute
- Response time > 1s

---

## 🚨 Troubleshooting Deployment

### App Won't Start

Check logs:
```bash
heroku logs --tail
```

Or for VPS:
```bash
journalctl -u ticket-agent -n 50
```

### CORS Errors

Verify `ALLOW_ORIGINS` environment variable is set correctly.

### Database Connection Failed

1. Check connection string
2. Verify network access is allowed
3. Check credentials

### High Memory Usage

1. Check for memory leaks
2. Reduce worker count
3. Enable caching

---

## 🎯 Performance Optimization

### Frontend

```bash
# Minify CSS/JS
npm install -g csso-cli terser
csso frontend/css/style.css -o frontend/css/style.min.css
terser frontend/js/app.js -o frontend/js/app.min.js

# Enable gzip compression
gzip -9 frontend/index.html
```

### Backend

```python
# Use uvicorn with workers
uvicorn main_simple:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Use connection pooling
# See database section above
```

---

## 📋 Deployment Checklist

- [ ] Code reviewed and tested
- [ ] No secrets in repository
- [ ] Environment variables configured
- [ ] Database connected
- [ ] Backups configured
- [ ] SSL certificate installed
- [ ] Monitoring/logging setup
- [ ] CI/CD pipeline working
- [ ] Health checks passing
- [ ] Performance acceptable
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Alerts configured
- [ ] Runbook created

---

## 📞 Support

For deployment issues:
1. Check logs
2. Verify environment variables
3. Test endpoints manually
4. Check documentation

---

Version 1.0.0 | Last Updated: January 2025
