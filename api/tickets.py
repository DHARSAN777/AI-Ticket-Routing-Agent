from http.server import BaseHTTPRequestHandler
import json
import uuid
from datetime import datetime

# In-memory storage for demo
tickets = []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "tickets": tickets,
            "count": len(tickets)
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Create new ticket
            ticket = {
                "id": f"TKT-{len(tickets) + 1:06d}",
                "subject": data.get("subject", ""),
                "description": data.get("description", ""),
                "customer_email": data.get("customer_email", ""),
                "customer_name": data.get("customer_name", ""),
                "customer_type": data.get("customer_type", "Regular"),
                "priority": data.get("priority", "Medium"),
                "status": "Open",
                "created_at": datetime.now().isoformat(),
                "category": self.analyze_category(data.get("subject", "") + " " + data.get("description", ""))
            }
            
            tickets.append(ticket)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "Ticket created successfully",
                "ticket": ticket,
                "analysis": {
                    "category": ticket["category"],
                    "confidence": 0.85
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def analyze_category(self, text):
        """Simple keyword-based categorization"""
        text_lower = text.lower()
        
        billing_keywords = ["payment", "billing", "invoice", "charge", "refund", "subscription", "price", "cost"]
        technical_keywords = ["error", "bug", "crash", "not working", "technical", "server", "api", "code"]
        account_keywords = ["account", "login", "password", "profile", "settings", "access", "permission"]
        
        if any(keyword in text_lower for keyword in billing_keywords):
            return "Billing"
        elif any(keyword in text_lower for keyword in technical_keywords):
            return "Technical"
        elif any(keyword in text_lower for keyword in account_keywords):
            return "Account"
        else:
            return "General"