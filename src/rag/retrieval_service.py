import logging
from typing import Any
from openai import OpenAI
from src.rag.vector_store import VectorStoreService
from src.rag.embedding_service import EmbeddingService
import chromadb
# # RETURNS DICTIONARY OF TYPE:
#  {
#     "text": "Example text goes here...",
#     "score": 0.99,
#     "metadata": {
#        "source": "handbook.pdf",
#        "section": "Leave policy",
#        "version": "1.0"
#     }
#  }

class RetrievalError(Exception):
    """Raised when policy retrieval fails"""
    print("Retrieval Error")

class RetrievalService:
    logger = logging.getLogger(__name__)

    def __init__(self, vector_store:VectorStoreService, embedding_service:EmbeddingService):
        self.vector_store = vector_store
        self.collection = vector_store.collection

        self.embedding_service = embedding_service

        self.logger = logging.getLogger(__name__)

    def rerank_chunks(self, query, results):
        query_words = set(query.lower().split())
        
        for r in results:
            text_words = set(r["text"].lower().split())
        
            overlap = len(query_words & text_words)
        
            r["rerank_score"] = overlap
        
        return sorted(results, key=lambda x: x["rerank_score"], reverse=True)


    def retrieve(self, query: str, top_k: int = 5, document_type: str | None = None, version: str | None = None, access_label: str | None = None, rerank: bool = False) -> list[dict[str, Any]]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        if (not isinstance(top_k, int) or top_k < 1):
            raise ValueError("top_k must be a positive integer.")

        # Filter:
        filters = []
        if document_type is not None:
            filters.append({"document_type": {"$eq": document_type}})

        if version is not None:
                    filters.append({"version": {"$eq": version}})

        if access_label is not None:
                    filters.append({"access_label": {"$eq": access_label}})

        where = None

        if len(filters) == 1:
             where = filters[0]

        elif len(filters) > 1:
             where = {"$and": filters}

        try:
            question_embedding = self.embedding_service.embed_query(query.strip())

            if len(question_embedding) != self.embedding_service.dimensions:
                raise RetrievalError("Unexpected query embedding dimensions.")

            # explicitly define cos
            results = self.collection.query(
                query_embeddings = [question_embedding], 
                n_results = top_k,
                where = where, 
                include = [
                    "documents",
                    "distances",
                    "metadatas"
                ]
            )

            ids = results["ids"][0]
            documents = results["documents"][0]
            distances = results["distances"][0]
            metadatas = results["metadatas"][0]

            retrieved_chunks = []

            for chunk_id, document, distance, metadata in zip(ids, documents, distances, metadatas):
                if document is None or distance is None:
                    continue

                score = 1.0 - float(distance)

                retrieved_chunks.append({
                     "chunk_id": chunk_id,
                    "text": document,
                    "score": score,
                    "metadata": metadata or {}
                })

            self.logger.info(f"Successfully retrieved {len(retrieved_chunks)} policy chunks.")

            if rerank:
                 retrieved_chunks = self.rerank_chunks(query, retrieved_chunks)

            return retrieved_chunks

        except RetrievalError:
            raise

        except Exception as exc:
            self.logger.exception("Policy retrieval failed.")

            raise RetrievalError("Vector store unavailable.") from exc