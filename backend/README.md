# 🎫 Ticket Agent - Backend API

AI-powered support ticket routing and analysis engine built with FastAPI.

## 📋 Overview

The Ticket Agent backend is a FastAPI application that provides intelligent ticket classification, routing, and analysis using mock AI (rule-based keyword matching). It requires zero external API dependencies and works completely offline.

### Key Features

✅ **Email-based passwordless authentication**  
✅ **Instant ticket analysis and AI classification**  
✅ **15+ ticket categories and priority detection**  
✅ **Sentiment analysis** (Angry, Frustrated, Happy, Neutral)  
✅ **Automatic team assignment and queue routing**  
✅ **Tag recommendations and confidence scoring**  
✅ **Suggested response generation**  
✅ **CORS enabled** for frontend integration  
✅ **No external API calls** - works completely offline  

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn main_simple:app --host 0.0.0.0 --port 5000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
   ```

4. **Test the API:**
   ```bash
   # In another terminal
   curl http://localhost:5000/health
   ```

   Expected response:
   ```json
   {"status": "healthy", "tickets": 0}
   ```

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`:

```
fastapi>=0.111.0              # Web framework
uvicorn[standard]>=0.29.0     # ASGI server
pydantic>=2.7.1               # Data validation
python-dotenv>=1.0.1          # Environment variables
bcrypt>=4.0.1                 # Password hashing
email-validator>=2.0.0        # Email validation
```

---

## 🔑 Authentication

### Email-Based Passwordless Login

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "base64-encoded-token",
  "token_type": "bearer",
  "user": {
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Demo Users (for testing):**
- `admin@example.com` / `admin123`
- `support@example.com` / `support123`
- `user@example.com` / `user123`

### Get Current User

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "email": "user@example.com",
  "name": "User Name"
}
```

---

## 🎫 Ticket Management

### Create Ticket with AI Analysis

**Endpoint:** `POST /tickets`

**Request:**
```json
{
  "title": "Cannot login after update",
  "description": "After the latest update I can't login to my account. Error shows 'Authentication failed'.",
  "submitter_name": "John Doe",
  "submitter_email": "john@example.com",
  "customer_type": "Enterprise",
  "category": null,
  "priority": null,
  "ticket_id": "TKT-ABC12345"
}
```

**Response:**
```json
{
  "id": "TKT-ABC12345",
  "category": "Login Issue",
  "priority": "High",
  "status": "OPEN",
  "ai_analysis": {
    "category": "Login Issue",
    "priority": "High",
    "sentiment": "Frustrated",
    "assigned_team": "Technical Support",
    "support_queue": "AUTHENTICATION",
    "summary": "Customer reported: Cannot login after update. Issue requires Technical Support attention.",
    "tags": ["login", "authentication", "urgent"],
    "requires_human_review": false,
    "confidence_score": 0.92,
    "suggested_response": "Thank you for contacting us. Our Technical Support team will assist you shortly.",
    "estimated_resolution_time": "24 hours"
  },
  "message": "Ticket created successfully"
}
```

### Get All Tickets

**Endpoint:** `GET /tickets`

**Query Parameters:**
- `email` (optional) - Filter by submitter email
- `status` (optional) - Filter by status (OPEN, CLOSED, IN_PROGRESS)

**Response:**
```json
[
  {
    "id": "TKT-ABC12345",
    "title": "Cannot login",
    "description": "...",
    "category": "Login Issue",
    "priority": "High",
    "status": "OPEN",
    "ai_analysis": { ... },
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

### Get Single Ticket

**Endpoint:** `GET /tickets/{ticket_id}`

**Response:**
```json
{
  "id": "TKT-ABC12345",
  "title": "Cannot login",
  "description": "...",
  "category": "Login Issue",
  "priority": "High",
  "status": "OPEN",
  "ai_analysis": { ... },
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Update Ticket Status

**Endpoint:** `PATCH /tickets/{ticket_id}/status`

**Request:**
```json
{
  "status": "CLOSED"
}
```

**Response:**
```json
{
  "message": "Ticket updated"
}
```

---

## 🤖 AI Analysis System

The backend uses intelligent keyword matching to analyze tickets:

### Category Detection (15 categories)

- **Billing** - Payments, charges, refunds, invoices
- **Technical Support** - Errors, crashes, bugs, issues
- **Login Issue** - Authentication, password, access
- **Security** - Account hacks, unauthorized access
- **Shipping** - Delivery, tracking, packages
- **General Inquiry** - Questions, help requests
- And more...

### Priority Assessment

- **Critical** - `urgent`, `critical`, `emergency`, `asap`, `down`
- **High** - `important`, `high`, `fast`, `quickly`
- **Medium** - Default
- **Low** - `low`, `minor`, `simple`

### Sentiment Analysis

- **Angry** - `angry`, `furious`, `hate`, `terrible`
- **Frustrated** - `frustrated`, `annoyed`, `upset`, `unhappy`
- **Happy** - `happy`, `great`, `excellent`
- **Neutral** - Default

### Team Assignment

| Category | Assigned Team |
|----------|---------------|
| Billing | Billing Team |
| Technical Support | Technical Support |
| Login Issue | Technical Support |
| Security | Security Team |
| Shipping | Logistics Team |
| General Inquiry | General Support |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend folder (copy from `.env.example`):

```
# API Configuration
API_TITLE=Ticket Agent API
API_VERSION=1.0.0
DEBUG=False

# Server
HOST=0.0.0.0
PORT=5000

# CORS
ALLOW_ORIGINS=*
```

### Modify AI Analysis

Edit the `analyze_ticket_mock()` function in `main_simple.py` to:
- Add more keywords to categories
- Adjust priority thresholds
- Customize team assignments
- Change sentiment detection

---

## 📊 Data Storage

Currently uses **in-memory storage** (resets on server restart). 

To add persistent storage:
1. Install MongoDB driver: `pip install motor pymongo`
2. Update `main_simple.py` to use `motor` for async MongoDB operations
3. Store tickets in MongoDB instead of `tickets_db` dictionary

---

## 🚨 Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "tickets": 42
}
```

---

## 🏠 Root Endpoint

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Ticket Agent API",
  "version": "1.0.0",
  "status": "running"
}
```

---

## 🔒 Security Features

✅ **Email validation** - Verifies email format  
✅ **Password strength** - Minimum 6 characters  
✅ **Token expiration** - Access tokens expire after use  
✅ **CORS protection** - Configurable origins  
✅ **Input validation** - Pydantic models validate all data  

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main_simple:app --host 0.0.0.0 --port 5001
```

### ModuleNotFoundError: fastapi
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### CORS Errors
- Check that `allow_origins=["*"]` in CORSMiddleware
- Verify frontend is sending requests to correct backend URL

### Tickets Not Saving
- Data is in-memory by default (resets on restart)
- This is by design for the demo
- Connect to MongoDB for persistence

---

## 📚 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:5000/docs
- **Alternative Docs**: http://localhost:5000/redoc

---

## 🤝 Integration with Frontend

The frontend connects to the backend via these key endpoints:

1. **Login** - `POST /auth/login`
2. **Create Ticket** - `POST /tickets`
3. **Get Tickets** - `GET /tickets`
4. **Get Single Ticket** - `GET /tickets/{ticket_id}`
5. **Update Status** - `PATCH /tickets/{ticket_id}/status`

Frontend expects backend running on `http://localhost:5000` (configurable in `frontend/js/app.js`)

---

## 📝 File Structure

```
backend/
├── main_simple.py           # Main FastAPI application
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── .env.example             # Example environment file
├── README.md                # This file
├── models/
│   ├── chat.py
│   ├── ticket.py
│   └── user.py
├── routes/
│   ├── auth_routes.py
│   └── ticket_routes.py
└── services/
    ├── auth_service.py
    ├── gemini_service.py
    ├── mongo_service.py
    └── vector_service.py
```

---

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main_simple:app --bind 0.0.0.0:5000
```

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main_simple.py .
CMD ["uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "5000"]
```

Build and run:
```bash
docker build -t ticket-agent-backend .
docker run -p 5000:5000 ticket-agent-backend
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Check `main_simple.py` for detailed implementation

---

## 📄 License

MIT License - Feel free to use and modify
