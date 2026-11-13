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
class IngestionService:

    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStoreService, max_chunk_size = 500):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.max_chunk_size = max_chunk_size

    def validate_manifest(self, directory_path, manifest_docs):

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
    def load_manifest(self, directory_path):

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

        validated_docs, counts = self.validate_manifest(
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
    def calculate_checksum(self, content):
        return hashlib.sha256(content.encode()).hexdigest()
    

    #==========================================================
    # Extract Normalized Documents
    #==========================================================
    def extract_structured_content(self, directory_path, validated_docs):

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
                    "checksum": self.calculate_checksum(content),
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
                    heading_match = re.match(r"Heading\s+\d+", style_name)

                
                    # Heading 1 defines a new section
                    if heading_match:

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
    def create_documents_jsonl(self, documents, counts):
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

    def parse_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--rebuild",
            action="store_true",
            help="Rebuild the entire vector index"
        )

        return parser.parse_args()

    def chunk_documents(self, documents):

        chunked_documents = []

        for document in documents:

            chunks = smart_chunking(
                text=document["content"],
                max_chunk_size=self.max_chunk_size,
                metadata=document
            )

            chunked_documents.extend(chunks)

        # Validate all generated chunks
        validate_chunks(chunked_documents)

        return chunked_documents

    def ingest(self, directory_path):

        validated_docs, counts = self.load_manifest(directory_path)

        documents = self.extract_structured_content(
            directory_path,
            validated_docs
        )

        chunks = self.chunk_documents(documents)

        self.create_documents_jsonl(chunks, counts)

        return chunks

    def ingest_to_vector_store(self, directory_path):
        chunks = self.ingest(directory_path)

        embeddings = self.embedding_service.embed_chunks(chunks)

        self.vector_store.persist(
            embeddings
        )

        return len(chunks)