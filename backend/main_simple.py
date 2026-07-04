from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import base64
import json

class UserLogin(BaseModel):
    email: str
    password: str

class TicketCreate(BaseModel):
    title: str
    description: str
    submitter_name: str
    submitter_email: str
    category: Optional[str] = None
    priority: Optional[str] = None
    customer_type: Optional[str] = "Free"
    ticket_id: Optional[str] = None

tickets_db = {}
users_db = {
    "admin@example.com": {"password": "admin123", "name": "Admin User"},
    "support@example.com": {"password": "support123", "name": "Support Agent"},
    "user@example.com": {"password": "user123", "name": "Test User"},
    "dharsanramesh05@gmail.com": {"password": "admin123", "name": "Dharsan Ramesh"},
}
tokens_db = {}

def analyze_ticket_mock(title: str, description: str, customer_type: str = "Free") -> dict:
    text = (title + " " + description).lower()
    
    categories = {
        "Billing": ["payment", "charge", "refund", "invoice", "bill", "card", "charged", "double"],
        "Technical Support": ["error", "crash", "bug", "not working", "broken", "failed", "network", "slow"],
        "Login Issue": ["login", "password", "access", "locked", "signin", "auth"],
        "Security": ["security", "hack", "breach", "unauthorized", "virus", "hacked"],
        "Shipping": ["shipping", "delivery", "package", "courier", "tracking"],
        "General Inquiry": ["help", "question", "how", "what", "info"],
    }
    
    category = "General Inquiry"
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            category = cat
            break
    
    priority = "Medium"
    if any(w in text for w in ["urgent", "critical", "emergency", "asap", "immediately", "down"]):
        priority = "Critical"
    elif any(w in text for w in ["important", "high", "fast", "quickly"]):
        priority = "High"
    elif any(w in text for w in ["low", "minor", "simple"]):
        priority = "Low"
    
    sentiment = "Neutral"
    if any(w in text for w in ["angry", "furious", "hate", "terrible"]):
        sentiment = "Angry"
    elif any(w in text for w in ["frustrated", "annoyed", "upset", "unhappy"]):
        sentiment = "Frustrated"
    elif any(w in text for w in ["happy", "great", "excellent"]):
        sentiment = "Happy"
    
    team_map = {
        "Billing": "Billing Team",
        "Technical Support": "Technical Support",
        "Login Issue": "Technical Support",
        "Security": "Security Team",
        "Shipping": "Logistics Team",
        "General Inquiry": "General Support"
    }
    
    team = team_map.get(category, "General Support")
    
    tags = []
    if "payment" in text: tags.append("payment")
    if "urgent" in text: tags.append("urgent")
    if category: tags.append(category.lower().replace(" ", "-"))
    tags = tags[:4]
    
    confidence = 0.75 + (min(len(description), 500) / 500) * 0.2
    
    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "assigned_team": team,
        "support_queue": category.upper().replace(" ", "-"),
        "summary": f"Customer reported: {title[:80]}",
        "tags": tags,
        "requires_human_review": confidence < 0.75,
        "confidence_score": round(confidence, 2),
        "suggested_response": f"Thank you for contacting us. Our {team} will assist you shortly.",
        "estimated_resolution_time": "24 hours" if priority != "Critical" else "1 hour"
    }

app = FastAPI(title="Ticket Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.post("/auth/login")
async def login(credentials: UserLogin):
    user = users_db.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {
        "email": credentials.email,
        "name": user["name"],
        "exp": datetime.now().isoformat()
    }
    token = base64.b64encode(json.dumps(token_data).encode()).decode()
    tokens_db[token] = token_data
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": credentials.email,
            "name": user["name"]
        }
    }

@app.get("/auth/me")
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    data = tokens_db[token]
    return {
        "email": data["email"],
        "name": data["name"]
    }

@app.post("/tickets")
async def create_ticket(ticket: TicketCreate):
    try:
        ai_analysis = analyze_ticket_mock(
            ticket.title,
            ticket.description,
            ticket.customer_type or "Free"
        )
        
        ticket_id = ticket.ticket_id or f"TKT-{str(uuid.uuid4())[:8].upper()}"
        now = datetime.now().isoformat()
        
        ticket_doc = {
            "id": ticket_id,
            "title": ticket.title,
            "description": ticket.description,
            "submitter_name": ticket.submitter_name,
            "submitter_email": ticket.submitter_email,
            "category": ai_analysis["category"],
            "priority": ai_analysis["priority"],
            "status": "OPEN",
            "ai_analysis": ai_analysis,
            "created_at": now,
            "updated_at": now
        }
        
        tickets_db[ticket_id] = ticket_doc
        
        return {
            "id": ticket_id,
            "category": ai_analysis["category"],
            "priority": ai_analysis["priority"],
            "status": "OPEN",
            "ai_analysis": ai_analysis,
            "message": "Ticket created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tickets")
async def get_tickets(email: Optional[str] = None, status: Optional[str] = None):
    tickets = list(tickets_db.values())
    
    if email:
        tickets = [t for t in tickets if t["submitter_email"] == email]
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    
    return tickets

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    if ticket_id not in tickets_db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return tickets_db[ticket_id]

@app.patch("/tickets/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, status_update: dict):
    if ticket_id not in tickets_db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    tickets_db[ticket_id]["status"] = status_update.get("status", "OPEN")
    tickets_db[ticket_id]["updated_at"] = datetime.now().isoformat()
    
    return {"message": "Ticket updated"}

@app.get("/")
async def root():
    return {
        "message": "Ticket Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "tickets": len(tickets_db)}
