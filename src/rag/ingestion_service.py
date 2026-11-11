#===================================================
import os
import time
import re
import csv
import json
import argparse
import hashlib
from dotenv import load_dotenv
import chromadb
from src.rag.vector_store import VectorStoreService
from src.rag.retrieval_service import RetrievalService
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from google import genai
from chromadb.utils import embedding_functions
from collections import Counter
from src.rag.chunking import fixed_chunking, retrieval_spot_test, smart_chunking, validate_chunks
from src.rag.embedding_service import EmbeddingService

#==========================================================
# Manifest Validation
#==========================================================
def validate_manifest(directory_path, manifest_docs):

    counts = {
        "accepted": 0,
        "rejected": 0,
        "warnings": 0
    }

    # Check duplicate source IDs
    source_ids = Counter(
        row["source_id"].strip()
        for row in manifest_docs
    )

    validated_docs = []

    for row in manifest_docs:

        relative_path = row["relative_path"].strip()
        source_id = row["source_id"].strip()
        effective_date = row.get("effective_date", "").strip()

        full_path = os.path.join(directory_path, relative_path)

        # Test 1: Missing file
        if not os.path.isfile(full_path):
            print(f"REJECTED - Missing file: {relative_path}")
            counts["rejected"] += 1
            continue

        # Test 2: Duplicate source ID
        if source_ids[source_id] > 1:
            print(f"REJECTED - Duplicate source ID: {source_id}")
            counts["rejected"] += 1
            continue

        # Test 3: Missing effective date
        if not effective_date:
            print(f"REJECTED - Missing effective date: {relative_path}")
            counts["rejected"] += 1
            continue

        validated_docs.append(row)
        counts["accepted"] += 1

    # Identify files that are not listed in the manifest
    listed_files = {
        os.path.normpath(row["relative_path"].strip())
        for row in manifest_docs
    }

    for root, _, files in os.walk(directory_path):

        for filename in files:

            if not filename.endswith(".docx"):
                continue

            relative_file = os.path.normpath(
                os.path.relpath(
                    os.path.join(root, filename),
                    directory_path
                )
            )

            if relative_file not in listed_files:
                print(f"REJECTED - Unlisted file: {relative_file}")
                counts["rejected"] += 1

    return validated_docs, counts

#==========================================================
# Load Manifest
#==========================================================
def load_manifest(directory_path):

    print("==== Checking Manifest ====")

    file_path = os.path.join(
        directory_path,
        "knowledge_base_manifest.csv"
    )

    manifest_docs = []

    with open(file_path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            manifest_docs.append(row)

    validated_docs, counts = validate_manifest(
        directory_path,
        manifest_docs
    )

    print("\n========== VALIDATION SUMMARY ==========")

    print(f"Files accepted: {counts['accepted']}")
    print(f"Files rejected: {counts['rejected']}")
    print(f"File warnings:  {counts['warnings']}")

    print("========================================")

    return validated_docs, counts

#==========================================================
# Calculate Checksum
#==========================================================
def calculate_checksum(content):
    return hashlib.sha256(content.encode()).hexdigest()
    

#==========================================================
# Extract Normalized Documents
#==========================================================
def extract_structured_content(directory_path, validated_docs):

    documents = []

    for row in validated_docs:

        document_id = row["source_id"]
        title = row["title"]
        document_type = row["document_type"]
        relative_path = row["relative_path"]
        version = row["version"]
        effective_date = row["effective_date"]
        access_label = row["access_label"]
        status = row["status"]

        file_path = os.path.join(directory_path, relative_path)

        doc = Document(file_path)

        current_section = "Introduction"
        current_content = []

        def save_section():
            if not current_content:
                return

            content = "\n\n".join(current_content)

            documents.append({
                "document_id": document_id,
                "title": title,
                "document_type": document_type,
                "source_file": relative_path,
                "section": current_section,
                "content": content,
                "checksum": calculate_checksum(content),
                "version": version,
                "effective_date": effective_date,
                "access_label": access_label,
                "status": status
            })

        for block in doc.iter_inner_content():

            # Process paragraphs
            if isinstance(block, Paragraph):

                text = block.text.strip()

                if not text:
                    continue

                style_name = block.style.name

                # Heading 1 defines a new section
                if style_name == "Heading 1":

                    save_section()

                    current_section = text
                    current_content = []

                else:
                    current_content.append(text)

            # Process tables
            elif isinstance(block, Table):

                for table_row in block.rows:

                    row_text = [
                        cell.text.strip()
                        for cell in table_row.cells
                    ]

                    current_content.append(
                        " | ".join(row_text)
                    )

        # Save final section
        save_section()

    return documents

#==========================================================
# Generate documents.jsonl
#==========================================================
def create_documents_jsonl(documents, counts):
    # write documents to documents.jsonl
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJ_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))  

    output_path = os.path.join(PROJ_ROOT, "data", "processed", "documents.jsonl")

    with open(output_path, "w", encoding="utf-8") as file:
        for document in documents:
            json.dump(document, file, ensure_ascii = False)
            file.write("\n")

    output_path = os.path.join(PROJ_ROOT, "data", "processed", "ingestion_run_log.json")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(counts, file, ensure_ascii = False)
        file.write("\n")

def retriever(question, n_results=8):
    print("==== Querying Chroma ====")

    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "metadatas"]
    )

    relevant_chunks = []

    for documents, metadatas in zip(
            results["documents"],
            results["metadatas"]
        ):

            for content, metadata in zip(documents, metadatas):

                relevant_chunks.append({
                    "document_id": metadata["document_id"],
                    "section": metadata["section"],
                    "source_file": metadata["source_file"],
                    "content": content
                })

    return relevant_chunks

def generate_response(
    question,
    relevant_chunks,
):
    context = "\n\n".join(chunk["content"] for chunk in relevant_chunks)

    prompt = f"""
You are a helpful assistant.

Use the supplied context to answer the question.

If the answer is not found in the context, say you don't know.

Keep the answer concise.

Context:
{context}

Question:
{question}
"""

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as exc:
            error_text = str(exc)

            is_retryable = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            )

            if not is_retryable or attempt == max_attempts:
                return (
                    "I could not generate an answer right now because "
                    "the Gemini API is temporarily unavailable. "
                    "Please try again in a few moments.\n\n"
                    f"Technical details: {exc}"
                )

            wait_seconds = 2 ** attempt

            print(
                f"Gemini temporarily unavailable "
                f"(attempt {attempt}/{max_attempts}). "
                f"Retrying in {wait_seconds}s..."
            )

            time.sleep(wait_seconds)


def load_chunks_into_chroma(chunks):

    all_ids = collection.get()["ids"]

    if all_ids:
        collection.delete(ids=all_ids)

    collection.upsert(
        ids=[doc["chunk_id"] for doc in chunks],
        documents=[doc["content"] for doc in chunks],
        metadatas=[
            {
                "document_id": doc["document_id"],
                "source_file": doc["source_file"],
                "section": doc["section"],
                "checksum": doc["checksum"],
                "version": doc["version"],
                "effective_date": doc["effective_date"],
                "status": doc["status"]
            }
            for doc in chunks
        ]
    )

def chunkingTest():

    #==========================================================
    # Load Environment Variables
    #==========================================================
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    #==========================================================
    # Gemini Client
    #==========================================================
    client = genai.Client(api_key=GOOGLE_API_KEY)

    #==========================================================
    # ChromaDB Setup
    #==========================================================
    chroma_client = chromadb.PersistentClient(
        path="chroma_persistent_storage"
    )

    hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    collection = chroma_client.get_or_create_collection(
        name="document_qa_collection",
        embedding_function=hf_ef
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    PROJ_ROOT = os.path.dirname(
        os.path.dirname(BASE_DIR)
    )

    directory_path = os.path.join(
        PROJ_ROOT,
        "docs",
        "design",
        "rag_docs"
    )

    manifests, counts = load_manifest(
        directory_path
    )

    docs = extract_structured_content(
        directory_path,
        manifests
    )

    print("\n===== EXTRACTED SECTIONS =====")

    for doc in docs:

        print(
            doc["document_id"],
            "|",
            doc["section"]
        )

    fixed_chunks = []
    smart_chunks = []

    for doc in docs:

        fixed_chunks.extend(
            fixed_chunking(
                doc["content"],
                metadata=doc
            )
        )

        smart_chunks.extend(
            smart_chunking(
                doc["content"],
                max_chunk_size=500,
                metadata=doc
            )
        )

    print("\n===== CHUNK STATISTICS =====")

    print(
        f"Fixed chunk count: "
        f"{len(fixed_chunks)}"
    )

    print(
        f"Smart chunk count: "
        f"{len(smart_chunks)}"
    )

    validate_chunks(fixed_chunks)
    validate_chunks(smart_chunks)

    with open(
        os.path.join(
            PROJ_ROOT,
            "tests",
            "chunking_experiment_cases.json"
        ),
        "r",
        encoding="utf-8"
    ) as file:

        test_cases = json.load(file)

    # =====================================
    # Fixed Chunking Test
    # =====================================

    print("\n=================================")
    print("TESTING FIXED CHUNKING")
    print("=================================")

    load_chunks_into_chroma(
        fixed_chunks
    )

    fixed_results = retrieval_spot_test(
        retriever,
        test_cases
    )

    fixed_passes = sum(
        result["passed"]
        for result in fixed_results
    )

    print(
        f"\nFixed Chunking Score: "
        f"{fixed_passes}/{len(fixed_results)}"
    )

    # =====================================
    # Smart Chunking Test
    # =====================================

    print("\n=================================")
    print("TESTING SMART CHUNKING")
    print("=================================")

    load_chunks_into_chroma(
        smart_chunks
    )

    smart_results = retrieval_spot_test(
        retriever,
        test_cases
    )

    smart_passes = sum(
        result["passed"]
        for result in smart_results
    )

    print(
        f"\nSmart Chunking Score: "
        f"{smart_passes}/{len(smart_results)}"
    )

    # =====================================
    # Comparison
    # =====================================

    print("\n=================================")
    print("FINAL COMPARISON")
    print("=================================")

    print(
        f"Fixed : "
        f"{fixed_passes}/{len(fixed_results)}"
    )

    print(
        f"Smart : "
        f"{smart_passes}/{len(smart_results)}"
    )

    all_ids = collection.get()["ids"]

    if all_ids:
        collection.delete(ids=all_ids)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the entire vector index"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    load_dotenv(override=True)

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    PROJ_ROOT = os.path.dirname(
        os.path.dirname(BASE_DIR)
    )

    directory_path = os.path.join(
        PROJ_ROOT,
        "docs",
        "design",
        "rag_docs"
    )

    manifests, counts = load_manifest(
        directory_path
    )

    docs = extract_structured_content(
        directory_path,
        manifests
    )

    print("\n===== EXTRACTED SECTIONS =====")

    for doc in docs:

        print(
            doc["document_id"],
            "|",
            doc["section"]
        )

    smart_chunks = []

    for doc in docs:

        smart_chunks.extend(
            smart_chunking(
                doc["content"],
                max_chunk_size=500,
                metadata=doc
            )
        )

    print("\n===== CHUNK STATISTICS =====")

    print(
        f"Smart chunk count: "
        f"{len(smart_chunks)}"
    )

    validate_chunks(smart_chunks)

    # =====================================
    # Embedding Stage
    # =====================================
    embedding_service = EmbeddingService(
        config_path=os.path.join(
            BASE_DIR,
            "embedding_config.json"
        ),
        api_key=OPENAI_API_KEY
    )

    embedded_chunks = (
        embedding_service.embed_chunks(
            smart_chunks
        )
    )

    print(
        f"\nEmbedded "
        f"{len(embedded_chunks)} chunks"
    )

    expected_ids = {
        chunk["chunk_id"]
        for chunk in smart_chunks
    }

    embedded_ids = {
        chunk["chunk_id"]
        for chunk in embedded_chunks
    }

    missing_ids = expected_ids - embedded_ids

    print("\n===== EMBEDDING VALIDATION =====")

    print(f"Expected chunks: {len(expected_ids)}")
    print(f"Embedded chunks: {len(embedded_ids)}")
    print(f"Missing chunks: {len(missing_ids)}")

    if missing_ids:
        print("Missing chunk IDs:", missing_ids)

    # ============================
    # Vector Store Stage
    # ============================

    vector_store = VectorStoreService(
        persist_directory=os.path.join(
            PROJ_ROOT,
            "vector_db",
            "chroma"
        ),
        collection_name="document_chunks"
    )

    if args.rebuild:
        if len(embedded_chunks) != len(smart_chunks):
            raise RuntimeError(
                "Full rebuild aborted:"
                "Not all chunks were successfully embedded."
            )
        vector_store.rebuild()

    vector_store.persist(embedded_records=embedded_chunks, batch_size = 500)

    print(
        f"\nTotal vectors in database:"
        f"{vector_store.get_collection_count()}"
    )

    print("\n================= INGESTION COMPLETE ==================")

    # =================================
    # Vector Index Validation
    # =================================

    validation_report = vector_store.validate_index(
        expected_chunks=smart_chunks,
        output_path=os.path.join(
            PROJ_ROOT,
            "data",
            "processed",
            "vector_index_validation.json"
        ),
        expected_dimensions=1536
    )

    if validation_report["status"] != "PASS":

        raise RuntimeError(
            "Vector index validation failed."
        )

    print("\n===== VECTOR INDEX VALIDATION PASSED =====")

    # ==================================
    # RETRIEVAL SERVICE
    # ==================================

    retrieval_service = RetrievalService(
        vector_store = vector_store,
        embedding_service = embedding_service
    )

    results = retrieval_service.retrieve(
        query="Should dates be reset to disguise age?",
        top_k = 5,
        document_type = "Policy",
        version = "2.0",
        access_label = "Internal",
        rerank = True
    )

    for result in results:
        print("Original score:", result["score"],
              "Rerank score:", result["rerank_score"])
        print(result["text"])

if __name__ == "__main__":
    main()