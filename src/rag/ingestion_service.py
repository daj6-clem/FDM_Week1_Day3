#===================================================
import os
import time
import csv
import json
import hashlib
from dotenv import load_dotenv
import chromadb
from docx import Document
from google import genai
from chromadb.utils import embedding_functions
from collections import Counter

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
        relative_path = row["relative_path"]
        version = row["version"]
        effective_date = row["effective_date"]
        status = row["status"]

        file_path = os.path.join(directory_path, relative_path)

        doc = Document(file_path)

        current_section = "Introduction"
        current_content = []

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()

            if not text:
                continue

            if paragraph.style.name.startswith("Heading"):
                if current_content:
                    content = "\n".join(current_content)
                    documents.append(
                        {
                            "document_id": document_id,
                            "source_file": relative_path,
                            "section": current_section,
                            "content": content,
                            "checksum": calculate_checksum(content),
                            "version": version,
                            "effective_date": effective_date,
                            "status":status
                        }
                    )

                current_section = text
                current_content = []
            else:
                current_content.append(text)
        if current_content:
            content = "\n".join(current_content)
            documents.append(
                {
                    "document_id": document_id,
                    "source_file": relative_path,
                    "section": current_section,
                    "content": content,
                    "checksum": calculate_checksum(content),
                    "version": version,
                    "effective_date": effective_date,
                    "status":status
                }
            )

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


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    PROJ_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

    directory_path = os.path.join(
        PROJ_ROOT,
        "docs",
        "design",
        "rag_docs"
    )

    manifests, counts = load_manifest(directory_path)
    docs = extract_structured_content(directory_path, manifests)
    create_documents_jsonl(docs, counts)

if __name__ == "__main__":
    main()