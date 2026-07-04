# 📡 Ticket Agent - API Reference

Complete REST API documentation for Ticket Agent backend.

---

## 🌐 Base URL

```
http://localhost:5000
```

All endpoints are relative to this base URL.

---

## 🔐 Authentication

### Authentication Method: Email + Password

All protected endpoints require an `Authorization` header with a Bearer token.

**Get Token:**
1. Call `POST /auth/login` with email and password
2. Receive `access_token` in response
3. Include in all subsequent requests

**Header Format:**
```
Authorization: Bearer {access_token}
```

### Example

```bash
curl -H "Authorization: Bearer your-token-here" \
  http://localhost:5000/auth/me
```

---

## 📚 API Endpoints

### 🔑 Authentication Endpoints

#### POST /auth/login
Login and get access token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

---

#### GET /auth/me
Get current user information

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "name": "User Name"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid token"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/auth/me \
  -H "Authorization: Bearer your-token-here"
```

---

### 🎫 Ticket Endpoints

#### POST /tickets
Create a new support ticket with AI analysis

**Request:**
```json
{
  "title": "Cannot login after update",
  "description": "After the latest update I cannot log into my account. It keeps showing 'authentication failed'. I'm an Enterprise customer and this is blocking my whole team.",
  "submitter_name": "John Doe",
  "submitter_email": "john@example.com",
  "customer_type": "Enterprise",
  "category": null,
  "priority": null,
  "ticket_id": "TKT-ABC123"
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | ✅ Yes | Ticket subject (max 200 chars) |
| description | string | ✅ Yes | Detailed description (min 10 chars) |
| submitter_name | string | ✅ Yes | Customer name (min 2 chars) |
| submitter_email | string | ✅ Yes | Customer email (valid email format) |
| customer_type | string | ✅ Yes | Free / Premium / Enterprise |
| category | string | ❌ No | Auto-detected if null (see categories below) |
| priority | string | ❌ No | Auto-detected if null (Critical/High/Medium/Low) |
| ticket_id | string | ❌ No | Will auto-generate if not provided |

**Response (200 OK):**
```json
{
  "id": "TKT-ABC123",
  "category": "Login Issue",
  "priority": "High",
  "status": "OPEN",
  "ai_analysis": {
    "category": "Login Issue",
    "priority": "High",
    "sentiment": "Frustrated",
    "assigned_team": "Technical Support",
    "support_queue": "AUTHENTICATION",
    "summary": "Enterprise customer blocked from login after update.",
    "tags": ["login", "authentication", "enterprise", "urgent"],
    "requires_human_review": false,
    "confidence_score": 0.97,
    "suggested_response": "Thank you for reporting this. Our Technical Support team will assist you immediately.",
    "estimated_resolution_time": "4 hours"
  },
  "message": "Ticket created successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Validation error: title too short"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cannot login",
    "description": "After update I cannot log in",
    "submitter_name": "John Doe",
    "submitter_email": "john@example.com",
    "customer_type": "Enterprise"
  }'
```

---

#### GET /tickets
Get all tickets with optional filtering

**Query Parameters:**

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| email | string | ✅ Yes | Filter by submitter email |
| status | string | ✅ Yes | Filter by status (OPEN/CLOSED/IN_PROGRESS) |

**Response (200 OK):**
```json
[
  {
    "id": "TKT-ABC123",
    "title": "Cannot login after update",
    "description": "After the latest update...",
    "submitter_name": "John Doe",
    "submitter_email": "john@example.com",
    "category": "Login Issue",
    "priority": "High",
    "status": "OPEN",
    "ai_analysis": { ... },
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  { ... more tickets ... }
]
```

**cURL Examples:**
```bash
# Get all tickets
curl http://localhost:5000/tickets

# Filter by email
curl http://localhost:5000/tickets?email=john@example.com

# Filter by status
curl http://localhost:5000/tickets?status=OPEN

# Combine filters
curl http://localhost:5000/tickets?email=john@example.com&status=OPEN
```

---

#### GET /tickets/{ticket_id}
Get a single ticket by ID

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticket_id | string | Ticket ID (e.g., TKT-ABC123) |

**Response (200 OK):**
```json
{
  "id": "TKT-ABC123",
  "title": "Cannot login after update",
  "description": "After the latest update...",
  "submitter_name": "John Doe",
  "submitter_email": "john@example.com",
  "category": "Login Issue",
  "priority": "High",
  "status": "OPEN",
  "ai_analysis": {
    "category": "Login Issue",
    "priority": "High",
    "sentiment": "Frustrated",
    "assigned_team": "Technical Support",
    "support_queue": "AUTHENTICATION",
    "summary": "Enterprise customer blocked from login after update.",
    "tags": ["login", "authentication"],
    "requires_human_review": false,
    "confidence_score": 0.97
  },
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Ticket not found"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/tickets/TKT-ABC123
```

---

#### PATCH /tickets/{ticket_id}/status
Update ticket status

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticket_id | string | Ticket ID (e.g., TKT-ABC123) |

**Request:**
```json
{
  "status": "CLOSED"
}
```

**Valid Status Values:**
- `OPEN` - New ticket
- `IN_PROGRESS` - Being worked on
- `CLOSED` - Resolved

**Response (200 OK):**
```json
{
  "message": "Ticket updated"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Ticket not found"
}
```

**cURL Example:**
```bash
curl -X PATCH http://localhost:5000/tickets/TKT-ABC123/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "CLOSED"
  }'
```

---

### 🔧 System Endpoints

#### GET /
API information and status

**Response (200 OK):**
```json
{
  "message": "Ticket Agent API",
  "version": "1.0.0",
  "status": "running"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/
```

---

#### GET /health
Health check endpoint

**Response (200 OK):**
```json
{
  "status": "healthy",
  "tickets": 42
}
```

**Usage:** Monitor API health and get ticket count

---

#### GET /docs
Interactive API documentation (Swagger UI)

**URL:** http://localhost:5000/docs

Try all endpoints interactively with built-in forms.

---

#### GET /redoc
Alternative API documentation (ReDoc)

**URL:** http://localhost:5000/redoc

View API documentation in different format.

---

## 🤖 AI Analysis Categories

### Ticket Categories (15+)

| Category | Keywords | Assigned Team |
|----------|----------|---------------|
| Billing | payment, charge, refund, invoice, bill, card, double charged | Billing Team |
| Technical Support | error, crash, bug, not working, broken, failed, network, slow | Technical Support |
| Login Issue | login, password, access, locked, signin, auth, authentication | Technical Support |
| Security | security, hack, breach, unauthorized, virus, hacked, compromised | Security Team |
| Shipping | shipping, delivery, package, courier, tracking, shipped | Logistics Team |
| General Inquiry | help, question, how, what, info, assistance | General Support |
| Refund | refund, money back, return | Finance Team |
| Subscription | subscription, billing cycle, renewal, cancel | Customer Success |
| Feature Request | add, feature, request, suggestion, idea | Product Team |
| Product Bug | bug, error, crash, issue, broken | Engineering |
| Sales | sales, pricing, quote, discount | Sales Team |
| Support | support, help, assist | Customer Support |
| Complaint | complaint, dissatisfied, unhappy, terrible | Customer Support |
| Return | return, RMA, exchange | Returns Team |
| Escalation | escalate, urgent, manager, supervisor | Escalation Team |

---

### Priority Levels

| Level | Keywords | SLA |
|-------|----------|-----|
| Critical | urgent, critical, emergency, asap, immediately, down, outage, breach | 1 hour |
| High | important, high, fast, quickly, blocks, prevents | 4 hours |
| Medium | (default) | 24 hours |
| Low | low, minor, simple, documentation | 72 hours |

---

### Sentiment Analysis

| Sentiment | Keywords | Indicates |
|-----------|----------|-----------|
| Angry | angry, furious, hate, terrible, disgusted | Severe frustration |
| Frustrated | frustrated, annoyed, upset, unhappy, disappointed | Frustration |
| Neutral | (default) | Calm, informative |
| Happy | happy, great, excellent, satisfied, love | Satisfaction |
| Concerned | worried, concerned, anxious, scared | Worry/Fear |
| Confused | confused, unclear, lost, how, why | Confusion |

---

## 🔄 Request/Response Examples

### Complete Workflow Example

**Step 1: Login**
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "email": "admin@example.com",
    "name": "Admin User"
  }
}
```

**Step 2: Create Ticket**
```bash
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Payment processing failed",
    "description": "My payment failed but I was still charged. I need a refund.",
    "submitter_name": "Jane Smith",
    "submitter_email": "jane@example.com",
    "customer_type": "Premium"
  }'
```

Response:
```json
{
  "id": "TKT-XYZ789",
  "category": "Billing",
  "priority": "High",
  "status": "OPEN",
  "ai_analysis": {
    "category": "Billing",
    "priority": "High",
    "sentiment": "Frustrated",
    "assigned_team": "Billing Team",
    "support_queue": "BILLING",
    "tags": ["payment", "refund", "urgent"],
    "confidence_score": 0.94
  }
}
```

**Step 3: Get Ticket**
```bash
curl http://localhost:5000/tickets/TKT-XYZ789
```

**Step 4: Update Status**
```bash
curl -X PATCH http://localhost:5000/tickets/TKT-XYZ789/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "CLOSED"
  }'
```

---

## 📊 Data Models

### Ticket Model

```json
{
  "id": "string (ticket ID)",
  "title": "string (subject)",
  "description": "string (details)",
  "submitter_name": "string",
  "submitter_email": "string (email format)",
  "category": "string (auto-detected)",
  "priority": "string (Critical/High/Medium/Low)",
  "status": "string (OPEN/IN_PROGRESS/CLOSED)",
  "ai_analysis": {
    "category": "string",
    "priority": "string",
    "sentiment": "string",
    "assigned_team": "string",
    "support_queue": "string",
    "summary": "string",
    "tags": ["string"],
    "requires_human_review": "boolean",
    "confidence_score": "number (0-1)",
    "suggested_response": "string",
    "estimated_resolution_time": "string"
  },
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

### User Model

```json
{
  "email": "string",
  "name": "string",
  "password": "string (hashed, not returned)"
}
```

---

## 🔢 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request succeeded | Ticket created |
| 400 | Bad Request - Invalid input | Missing required field |
| 401 | Unauthorized - Auth failed | Wrong password |
| 404 | Not Found - Resource missing | Ticket doesn't exist |
| 500 | Server Error - Backend error | Database connection failed |

---

## 🛡️ Rate Limiting

Currently: **No rate limiting**

For production, implement:
- Max 100 requests per minute per IP
- Max 10 tickets per minute per user
- Max 5 login attempts per minute

---

## 🔗 CORS Configuration

**Allowed Origins:** `*` (all origins)

For production, restrict to your domain:

```python
allow_origins=["https://yourdomain.com"]
```

---

## 📝 Error Handling

All errors return JSON in this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Examples:**

Invalid email:
```json
{
  "detail": "Invalid email format"
}
```

Missing field:
```json
{
  "detail": "Field 'title' is required"
}
```

Authentication failed:
```json
{
  "detail": "Invalid credentials"
}
```

---

## 🔐 Security Headers

Consider adding in production:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 🧪 Testing Endpoints

### Using curl

```bash
# Health check
curl http://localhost:5000/health

# Get all tickets
curl http://localhost:5000/tickets

# Create ticket
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Testing","submitter_name":"Test","submitter_email":"test@example.com","customer_type":"Free"}'
```

### Using Postman

1. Import these endpoints
2. Set base URL: `http://localhost:5000`
3. Add header: `Content-Type: application/json`
4. Test each endpoint

### Using the Interactive Docs

Visit: http://localhost:5000/docs

- Try endpoints directly
- See response formats
- Check required parameters

---

## 📚 Integration Examples

### Python

```python
import requests

# Login
response = requests.post('http://localhost:5000/auth/login', json={
  'email': 'admin@example.com',
  'password': 'admin123'
})
token = response.json()['access_token']

# Create ticket
response = requests.post('http://localhost:5000/tickets', json={
  'title': 'Issue',
  'description': 'Details',
  'submitter_name': 'Name',
  'submitter_email': 'email@example.com',
  'customer_type': 'Free'
})
print(response.json())
```

### JavaScript

```javascript
// Login
const response = await fetch('http://localhost:5000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin@example.com',
    password: 'admin123'
  })
});
const { access_token } = await response.json();

// Create ticket
const ticketResponse = await fetch('http://localhost:5000/tickets', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Issue',
    description: 'Details',
    submitter_name: 'Name',
    submitter_email: 'email@example.com',
    customer_type: 'Free'
  })
});
const ticket = await ticketResponse.json();
console.log(ticket);
```

---

## 📖 OpenAPI Specification

Full OpenAPI spec available at:
```
http://localhost:5000/openapi.json
```

---

## 🚀 Version

**API Version:** 1.0.0  
**Last Updated:** January 2025

---

## 📞 Support

- View interactive docs: http://localhost:5000/docs
- Check backend README: `backend/README.md`
- Review code comments: `backend/main_simple.py`

---

**Happy API-ing!** 🚀
