from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


class TicketCategory(str, Enum):
    TECHNICAL = "TECHNICAL"
    BILLING = "BILLING"
    ACCOUNT = "ACCOUNT"
    GENERAL = "GENERAL"


class TicketPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    submitter_name: str = Field(..., min_length=2, max_length=100)
    submitter_email: str = Field(...)
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    customer_type: Optional[str] = "Free"
    ticket_id: Optional[str] = None


class AIAnalysis(BaseModel):
    category: str
    priority: str
    summary: str
    reasoning: Optional[str] = ""
    suggested_response: str
    tags: List[str] = []
    estimated_resolution_time: Optional[str] = "24 hours"
    confidence: float = 0.8


class TicketStatusUpdate(BaseModel):
    status: TicketStatus
    resolution_note: Optional[str] = None
