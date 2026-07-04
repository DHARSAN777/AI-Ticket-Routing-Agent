from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional, List
from models.ticket import (
    TicketCreate, 
    TicketStatusUpdate, 
    TicketCategory, 
    TicketPriority, 
    TicketStatus
)
from datetime import datetime


router = APIRouter()


@router.post("")
async def create_ticket(ticket: TicketCreate, request: Request):
    """Create a new support ticket with AI analysis"""
    try:
        mongo = request.app.state.mongo
        gemini = request.app.state.gemini
        vector = request.app.state.vector
        
        # Get AI analysis
        ai_analysis = await gemini.analyze_ticket(
            title=ticket.title,
            description=ticket.description,
            customer_type=getattr(ticket, 'customer_type', 'Free'),
            ticket_id=getattr(ticket, 'ticket_id', '')
        )
        
        # Use AI detected category/priority if not provided
        category = ticket.category or ai_analysis.get("category", "GENERAL")
        priority = ticket.priority or ai_analysis.get("priority", "MEDIUM")
        
        # Create ticket document
        ticket_doc = {
            "title": ticket.title,
            "description": ticket.description,
            "submitter_name": ticket.submitter_name,
            "submitter_email": ticket.submitter_email,
            "category": category,
            "priority": priority,
            "status": TicketStatus.OPEN,
            "ai_analysis": ai_analysis,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Save to MongoDB
        ticket_id = await mongo.create_ticket(ticket_doc)
        ticket_doc["id"] = str(ticket_id)
        
        # Store in vector DB for similarity search
        await vector.add_ticket(
            ticket_id=str(ticket_id),
            text=f"{ticket.title}\n\n{ticket.description}",
            metadata={
                "category": category,
                "priority": priority
            }
        )
        
        return {
            "id": str(ticket_id),
            "category": category,
            "priority": priority,
            "status": TicketStatus.OPEN,
            "ai_analysis": ai_analysis,
            "message": "Ticket created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def get_tickets(
    request: Request,
    submitter_email: Optional[str] = Query(None),
    status: Optional[TicketStatus] = Query(None),
    category: Optional[TicketCategory] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all tickets with optional filters"""
    try:
        mongo = request.app.state.mongo
        
        filters = {}
        if submitter_email:
            filters["submitter_email"] = submitter_email
        if status:
            filters["status"] = status
        if category:
            filters["category"] = category
        
        tickets = await mongo.get_tickets(filters, skip, limit)
        return tickets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str, request: Request):
    """Get a specific ticket by ID"""
    try:
        mongo = request.app.state.mongo
        ticket = await mongo.get_ticket_by_id(ticket_id)
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return ticket
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: str, 
    status_update: TicketStatusUpdate, 
    request: Request
):
    """Update ticket status"""
    try:
        mongo = request.app.state.mongo
        
        update_data = {
            "status": status_update.status,
            "updated_at": datetime.utcnow()
        }
        
        if status_update.resolution_note:
            update_data["resolution_note"] = status_update.resolution_note
        
        success = await mongo.update_ticket(ticket_id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {"message": "Ticket status updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticket_id}/similar")
async def find_similar_tickets(ticket_id: str, request: Request, limit: int = 5):
    """Find similar tickets using vector search"""
    try:
        mongo = request.app.state.mongo
        vector = request.app.state.vector
        
        ticket = await mongo.get_ticket_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        query_text = f"{ticket['title']}\n\n{ticket['description']}"
        similar = await vector.search_similar(query_text, limit)
        
        return {"similar_tickets": similar}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
