import os
import time
import csv
import json
import hashlib
import re
from dotenv import load_dotenv
import chromadb
from docx import Document
from google import genai
from chromadb.utils import embedding_functions
from collections import Counter

def split_fixed(text, chunk_size = 800, overlap = 150):
    if overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk size.")

    chunks = []
    start = 0

    while start < len(text):
        end = start+chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def fixed_chunking(text, chunk_size=500, overlap = 50, metadata = None):
    text_chunks = split_fixed(text, chunk_size, overlap)

    chunked_documents = []

    for i, chunk in enumerate(text_chunks, start = 1):
        chunked_documents.append(
            {
                "chunk_id": f"{metadata["document_id"]}_{metadata["section"]}_chunk_{i:03d}",
                "document_id": metadata["document_id"],
                "source_file": metadata["source_file"],
                "section": metadata["section"],
                "content": chunk,
                "checksum": metadata["checksum"],
                "version": metadata["version"],
                "effective_date": metadata["effective_date"],
                "status": metadata["status"]
            }
        )

    return chunked_documents

def smart_chunking(text, max_chunk_size, metadata = None):
    # Use document structure to separate chunks
    # This could be headings, paragraphs, bullet lists, numbers, exception section

    chunks = []

    paragraphs = []
    current_block = []
    in_list = False

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        is_bullet = line.startswith(("-", "*", "•"))
        is_numbered = re.match(
            r"^\d+[\.\)]\s*",
            line
        )
        # Bullet List item
        if is_bullet or is_numbered:
            if not in_list and current_block:
                paragraphs.append("\n".join(current_block))
                current_block = []

            current_block.append(line)
            in_list = True

        # Exception/Warning/Notes
        elif line.lower().startswith(
            (
                "exception",
                "exceptions",
                "warning",
                "warnings",
                "note",
                "notes",
                "notice"
            )
        ):
            if current_block:
                paragraphs.append("\n".join(current_block))
                current_block = []

            paragraphs.append(line)
            in_list = False

        else:
            if in_list and current_block:
                paragraphs.append("\n".join(current_block))
                current_block = []

            current_block.append(line)
            in_list = False

    if current_block:
        paragraphs.append("\n".join(current_block))

    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:
            if current_chunk:
                chunks.append(current_chunk)

            if len(paragraph) > max_chunk_size:
                chunks.extend(
                    split_fixed(
                        paragraph,
                        chunk_size=max_chunk_size, 
                        overlap=50
                    )
                )
                current_chunk = ""
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    chunked_documents = []

    for i, chunk in enumerate(chunks, start = 1):
        chunked_documents.append(
            {
                "chunk_id": f"{metadata['document_id']}_{metadata['section']}_chunk_{i:03d}",
                "document_id": metadata["document_id"],
                "title": metadata["title"],
                "document_type": metadata["document_type"],
                "source_file": metadata["source_file"],
                "section": metadata["section"],
                "content": (f"{metadata['section']}\n\n" 
                            f"{chunk}"
                            ),
                "checksum": metadata["checksum"],
                "version": metadata["version"],
                "effective_date": metadata["effective_date"],
                "access_label": metadata["access_label"],
                "status": metadata["status"]
            }
        )

    chunk_lengths = [len(chunk["content"]) for chunk in chunked_documents]

    print(f"Average: {sum(chunk_lengths)/len(chunk_lengths):.0f}")
    print(f"Max: {max(chunk_lengths)}")
    print(f"Min: {min(chunk_lengths)}")

    return chunked_documents



def validate_chunks(chunks):
    # Unique IDs (Does every chunk have a unique ID?)
    # Source Lineage (Can they be traced back to source doc?)
    # No Empty Chunks
    # Excessively Sized Chunks (Flag chunks above, say, 1000 tokens)
    # Retrival Spot Test (Use queries from chunking_experiment_cases.json)
    #       See which of the two models spots exceptions to rules

    errors = []
    warnings = []

    seen_ids = set()

    for chunk in chunks:
        chunk_id = chunk["chunk_id"]

        if chunk_id in seen_ids:
            errors.append(f"Duplicate chunk_id found: {chunk_id}")
        else:
            seen_ids.add(chunk_id)

    for chunk in chunks:
        if not chunk.get("source_file"):
            errors.append(
                f"Chunk {chunk["chunk_id"]} is missing source_file"
            )

        if not chunk.get("document_id"):
            errors.append(
                f"Chunk {chunk["chunk_id"]} is missing document_id"
            )

    for chunk in chunks:
        content = chunk.get("content", "")
        if not content.strip():
            errors.append(
                f"Chunk {chunk["chunk_id"]} has empty content"
            )

    for chunk in chunks:
        word_count = len(chunk["content"].split())

        if word_count > 1000:
            warnings.append(
                f"Chunk {chunk["chunk_id"]} exceeds 1000 words ({word_count})"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def retrieval_spot_test(retriever, test_cases):

    results = []

    for case in test_cases:

        # Temporarily retrieve more results
        retrieved = retriever(case["query"], n_results=10)

        source_match = any(
            chunk["document_id"] == case["expected_source"]
            for chunk in retrieved
        )

        section_match = any(
            chunk["document_id"] == case["expected_source"]
            and chunk["section"] == case["expected_section"]
            for chunk in retrieved
        )

        print(f"\n========== {case['case_id']} ==========")
        print(f"Query: {case['query']}")

        print(
            f"Expected: {case['expected_source']} | "
            f"{case['expected_section']}"
        )

        print("\nACTUAL RETRIEVED RESULTS:")

        for i, chunk in enumerate(retrieved, start=1):

            print(
                f"{i}. {chunk['document_id']} | "
                f"{chunk['section']}"
            )

        print(f"\nSource match: {source_match}")
        print(f"Section match: {section_match}")

        results.append({
            "case_id": case["case_id"],
            "query": case["query"],
            "expected_source": case["expected_source"],
            "expected_section": case["expected_section"],
            "source_match": source_match,
            "passed": section_match
        })

    return results