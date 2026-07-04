import chromadb
from chromadb.config import Settings as ChromaSettings
import google.generativeai as genai
from config import settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)


class VectorService:
    """ChromaDB-backed vector store using Google text-embedding-004."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.client = chromadb.PersistentClient(
            path="./chroma_data",
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="tickets",
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("ChromaDB initialised ✓  (collection count: %d)", self.collection.count())

    # ── Embeddings ───────────────────────────────────────────

    async def _embed(self, text: str) -> List[float]:
        """Fetch a Google text-embedding-004 vector for a string."""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]

    # ── Vector CRUD ──────────────────────────────────────────

    async def add_ticket(self, ticket_id: str, text: str, metadata: dict):
        """Embed and store a ticket in ChromaDB."""
        embedding = await self._embed(text)
        try:
            self.collection.add(
                ids=[ticket_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "ticket_id": ticket_id,
                    "category": metadata.get("category", "GENERAL"),
                    "priority": metadata.get("priority", "MEDIUM"),
                    "status": metadata.get("status", "OPEN"),
                }],
            )
        except Exception as exc:
            # Duplicate id: update instead
            logger.warning("ChromaDB add failed (%s) — attempting upsert", exc)
            self.collection.update(
                ids=[ticket_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "ticket_id": ticket_id,
                    "category": metadata.get("category", "GENERAL"),
                    "priority": metadata.get("priority", "MEDIUM"),
                    "status": metadata.get("status", "OPEN"),
                }],
            )

    async def search_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """Return the top-N most semantically similar tickets."""
        count = self.collection.count()
        if count == 0:
            return []

        query_embedding = await self._embed(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            include=["documents", "metadatas", "distances"],
        )

        similar = []
        if results["ids"] and results["ids"][0]:
            for i, ticket_id in enumerate(results["ids"][0]):
                similar.append({
                    "ticket_id": ticket_id,
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                })
        return similar

    async def delete_ticket(self, ticket_id: str):
        try:
            self.collection.delete(ids=[ticket_id])
        except Exception as exc:
            logger.error("ChromaDB delete error: %s", exc)


# Service instance will be created by main.py
