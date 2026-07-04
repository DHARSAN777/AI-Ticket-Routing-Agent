import google.generativeai as genai
import json
import re
import logging
from config import settings

logger = logging.getLogger(__name__)

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.warning(f"Gemini configuration error: {e}")

# ─────────────────────────────────────────────────────────────
# Mock AI Analysis (No external API required for demo)
# ─────────────────────────────────────────────────────────────

def mock_analyze_ticket(title: str, description: str, customer_type: str = "Free") -> dict:
    """Mock ticket analysis using rules instead of API calls"""
    
    lower_text = (title + " " + description).lower()
    
    # Category detection
    category_map = {
        "billing": ["payment", "charge", "refund", "invoice", "bill", "card", "charged", "double charge"],
        "Technical Support": ["error", "crash", "bug", "not working", "broken", "failed", "network", "slow", "lag"],
        "Login Issue": ["login", "password", "access", "locked", "signin", "authentication", "unauthorized"],
        "Security": ["security", "hack", "breach", "unauthorized", "virus", "malware", "suspicious", "hacked"],
        "Refund Request": ["refund", "money back", "return", "chargeback", "reimburs"],
        "Subscription": ["subscription", "cancel", "downgrade", "upgrade", "plan", "billing cycle"],
        "Product Bug": ["bug", "glitch", "malfunction", "issue", "problem", "defect"],
        "Shipping": ["shipping", "delivery", "package", "courier", "tracking", "shipment", "order"],
        "Account Management": ["account", "profile", "setting", "email", "username", "two-factor"],
        "General Inquiry": ["help", "question", "how", "what", "where", "when", "info"],
    }
    
    category = "General Inquiry"
    for cat, keywords in category_map.items():
        if any(keyword in lower_text for keyword in keywords):
            category = cat
            break
    
    # Priority detection
    priority = "Medium"
    if any(word in lower_text for word in ["urgent", "critical", "emergency", "asap", "immediately", "down", "outage"]):
        priority = "Critical"
    elif any(word in lower_text for word in ["important", "high", "fast", "quickly", "soon"]):
        priority = "High"
    elif any(word in lower_text for word in ["low", "minor", "simple", "basic", "small"]):
        priority = "Low"
    
    # Sentiment detection
    sentiment = "Neutral"
    if any(word in lower_text for word in ["angry", "furious", "hate", "terrible", "worst"]):
        sentiment = "Angry"
    elif any(word in lower_text for word in ["frustrated", "annoyed", "upset", "unhappy", "disappointed"]):
        sentiment = "Frustrated"
    elif any(word in lower_text for word in ["happy", "great", "excellent", "wonderful", "love"]):
        sentiment = "Happy"
    elif any(word in lower_text for word in ["confused", "confused", "unclear", "uncertain", "puzzled"]):
        sentiment = "Confused"
    
    # Team assignment
    team_map = {
        "Billing": "Billing Team",
        "Technical Support": "Technical Support",
        "Login Issue": "Technical Support",
        "Security": "Security Team",
        "Refund Request": "Finance Team",
        "Subscription": "Customer Success",
        "Product Bug": "Engineering",
        "Shipping": "Logistics",
        "Account Management": "Account Management",
        "General Inquiry": "General Support"
    }
    
    assigned_team = team_map.get(category, "General Support")
    
    # Tags extraction
    tags = []
    if "payment" in lower_text or "charge" in lower_text:
        tags.append("payment")
    if "network" in lower_text or "internet" in lower_text:
        tags.append("network")
    if "urgent" in lower_text:
        tags.append("urgent")
    if category:
        tags.append(category.lower().replace(" ", "-"))
    
    tags = tags[:4]  # Limit to 4 tags
    
    # Confidence score based on text length and clarity
    confidence = 0.75 + (min(len(description), 500) / 500) * 0.2
    
    return {
        "ticket_id": "TKT-DEMO",
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "assigned_team": assigned_team,
        "support_queue": category.upper().replace(" ", "-"),
        "summary": f"Customer reported: {title[:100]}",
        "tags": tags,
        "requires_human_review": confidence < 0.75,
        "confidence_score": round(confidence, 2),
        "suggested_response": f"Thank you for contacting us regarding your {category.lower()} issue. Our {assigned_team} team will review your request and get back to you within 24 hours.",
        "estimated_resolution_time": "24 hours" if priority != "Critical" else "1 hour"
    }


# ─────────────────────────────────────────────────────────────
# Service Class
# ─────────────────────────────────────────────────────────────

class GeminiService:
    def __init__(self, api_key: str):
        try:
            genai.configure(api_key=api_key)
            self.model = None
            self.chat_model = None
        except Exception as e:
            logger.warning(f"Gemini initialization warning: {e}")

    async def analyze_ticket(self, title: str, description: str, customer_type: str = "Free", ticket_id: str = "") -> dict:
        """Analyze a support ticket - uses mock analysis"""
        try:
            # Use mock analysis (faster and more reliable for demo)
            return mock_analyze_ticket(title, description, customer_type)
        except Exception as e:
            logger.warning(f"Analysis error: {e}")
            return mock_analyze_ticket(title, description, customer_type)

    async def chat(self, message: str, history: list) -> str:
        """Handle a conversational chat turn"""
        # Simple mock response for demo
        responses = {
            "help": "I'm here to help! What issue are you experiencing?",
            "login": "For login issues, try clearing your browser cache and resetting your password.",
            "payment": "For billing questions, please check your invoice or contact our billing team.",
            "bug": "Thank you for reporting this issue. Our engineering team will investigate.",
            "default": "I understand your concern. Let me connect you with the right team to assist you."
        }
        
        lower_msg = message.lower()
        for key, response in responses.items():
            if key in lower_msg:
                return response
        return responses["default"]

    async def suggest_response(self, ticket: dict) -> str:
        """Generate a polished response suggestion for an admin"""
        category = ticket.get("category", "GENERAL")
        priority = ticket.get("priority", "MEDIUM")
        
        return f"Thank you for your {category.lower()} request. We appreciate your patience. Our team will prioritize this as {priority} and provide an update soon."


# Service instance will be created by main.py
