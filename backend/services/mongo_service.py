from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING
from config import settings
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class MongoService:
    def __init__(self, database):
        self.db = database

    # ── CRUD ─────────────────────────────────────────────────

    async def create_ticket(self, ticket_data: dict) -> str:
        result = await self.db.tickets.insert_one(ticket_data.copy())
        return str(result.inserted_id)

    async def get_tickets(self, filters: dict = None, skip: int = 0, limit: int = 100) -> List[dict]:
        if filters is None:
            filters = {}
        cursor = (
            self.db.tickets.find(filters)
            .sort("created_at", DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        tickets = await cursor.to_list(length=limit)
        for t in tickets:
            t["id"] = str(t.pop("_id"))
        return tickets

    async def get_ticket_by_id(self, ticket_id: str) -> Optional[dict]:
        from bson import ObjectId
        try:
            ticket = await self.db.tickets.find_one({"_id": ObjectId(ticket_id)})
            if ticket:
                ticket["id"] = str(ticket.pop("_id"))
            return ticket
        except:
            return None

    async def update_ticket(self, ticket_id: str, update_data: dict) -> bool:
        from bson import ObjectId
        try:
            result = await self.db.tickets.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_ticket(self, ticket_id: str) -> bool:
        from bson import ObjectId
        try:
            result = await self.db.tickets.delete_one({"_id": ObjectId(ticket_id)})
            return result.deleted_count > 0
        except:
            return False

    # ── Analytics ────────────────────────────────────────────

    async def get_stats(self) -> dict:
        total = await self.db.tickets.count_documents({})
        open_c = await self.db.tickets.count_documents({"status": "OPEN"})
        in_prog = await self.db.tickets.count_documents({"status": "IN_PROGRESS"})
        resolved = await self.db.tickets.count_documents({"status": "RESOLVED"})
        closed = await self.db.tickets.count_documents({"status": "CLOSED"})

        categories = {}
        for cat in ["TECHNICAL", "BILLING", "ACCOUNT", "GENERAL"]:
            categories[cat] = await self.db.tickets.count_documents({"category": cat})

        priorities = {}
        for pri in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            priorities[pri] = await self.db.tickets.count_documents({"priority": pri})

        return {
            "total": total,
            "open": open_c,
            "in_progress": in_prog,
            "resolved": resolved,
            "closed": closed,
            "by_category": categories,
            "by_priority": priorities,
        }
