import os

from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from src.config import DB_PATH, BASE_URL, OPENAI_API_KEY, BASE_DIR, PROJECT_ROOT
from openai import OpenAI

from data.connection import SessionLocal

from data.repositories.complaint_repository import ComplaintRepository
from data.repositories.customer_repository import CustomerRepository
from data.repositories.account_repository import AccountRepository
from data.repositories.complaint_status_history_repository import (
    ComplaintStatusHistoryRepository
)

from src.services.complaint_service import ComplaintService
from src.services.customer_service import CustomerService
from src.services.account_service import AccountService

from src.rag.ingestion_service import IngestionService
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStoreService
from src.rag.retrieval_service import RetrievalService
from src.rag.answer_service import AnswerService
from src.rag.citations import CitationFormatter


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_complaint_service():
    complaint_repo = ComplaintRepository()
    customer_repo = CustomerRepository()
    csh_repo = ComplaintStatusHistoryRepository()

    return ComplaintService(
        complaint_repo = complaint_repo,
        customer_repo = customer_repo,
        csh_repo = csh_repo
    )

def get_customer_service():
    repository = CustomerRepository()
    return CustomerService(repository = repository)

def get_account_service():
    repository = AccountRepository()
    return AccountService(repository = repository)

@lru_cache
def get_openai_client():

    return OpenAI(
        base_url = BASE_URL,
        api_key=OPENAI_API_KEY
    )

@lru_cache
def get_embedding_service():

    return EmbeddingService(
        config_path=BASE_DIR / "rag" / "embedding_config.json",
        client = get_openai_client()
    )

@lru_cache
def get_vector_store():

    return VectorStoreService(
        persist_directory=PROJECT_ROOT / "vector_db" / "chroma",
        collection_name="document_chunks"
    )

@lru_cache
def get_ingestion_service():
    return IngestionService(embedding_service = get_embedding_service(),
                            vector_store = get_vector_store())

@lru_cache
def get_retrieval_service():

    return RetrievalService(
        vector_store=get_vector_store(),
        embedding_service=get_embedding_service()
    )

@lru_cache
def get_citation_formatter():

    return CitationFormatter()

@lru_cache
def get_answer_service():

    return AnswerService(
        client=get_openai_client(),
        model="qwen2.5:3b",
        citation_formatter=get_citation_formatter()
    )