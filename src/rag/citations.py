import logging
from typing import Any


class CitationFormatter:
    logger = logging.getLogger(__name__)

    def format_citations(self, evidence_ids, chunks):
        chunk_lookup = {
            chunk["chunk_id"]: chunk
            for chunk in chunks
        }

        citations = []

        for chunk_id in evidence_ids:
            chunk = chunk_lookup[chunk_id]
            metadata = chunk["metadata"]

            citations.append({
                "chunk_id": chunk_id,
                "document_id": metadata.get("document_id"),
                "title": metadata.get("title"),
                "source_file": metadata.get("source_file"),
                "section": metadata.get("section"),
                "version": metadata.get("version"),
                "effective_date": metadata.get("effective_date")
            })

        return citations