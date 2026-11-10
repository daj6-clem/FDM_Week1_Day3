import os
import json
import time
import logging
from openai import OpenAI

# Embed selected chunks in batches
# Handle failures and retries without duplicating records

class EmbeddingService:
    # batch size 10
    # create an example log, i.e.
    # "Loaded 120 chunks", "Batch 1 processed, Batch 2 processed..."

    def __init__(self, config_path, api_key):
        self.client = OpenAI(api_key=api_key)

        with open(config_path, "r", encoding = "utf-8") as file:
            self.config = json.load(file)

        self.model = self.config["model"]
        self.batch_size = self.config["batch_size"]
        self.normalize = self.config["normalize"]
        self.dimensions = self.config["dimensions"]

        logging.basicConfig(
            level = logging.INFO,
            format="%(asctime)s - %(message)s"
        )

    def embed_chunks(self, chunks, max_retries = 3):
        logging.info(f"Loaded {len(chunks)} chunks")

        embedded_records = []

        processed_ids = set()

        batches = [chunks[i:i + self.batch_size]
                   for i in range(0, len(chunks), self.batch_size)
        ]

        for batch_num, batch in enumerate(batches, start = 1):
            pending_batch = [chunk for chunk in batch if chunk["chunk_id"] not in processed_ids]

            if not pending_batch:
                continue

            texts = [
                chunk["content"]
                for chunk in pending_batch
            ]

            for attempt in range(1, max_retries + 1):
                try:
                    response = (
                        self.client.embeddings.create(
                            model = self.model,
                            input = texts,
                            dimensions = self.dimensions
                            
                        )
                    )

                    returned_count = len(response.data)

                    logging.info(
                        f"Batch {batch_num}:"
                        f"Sent {len(pending_batch)}, "
                        f"Received {returned_count}"
                    )

                    if returned_count != len(pending_batch):
                        raise ValueError(
                            f"Expected {len(pending_batch)} embeddings, "
                            f"received {returned_count}"
                        )

                    embeddings_by_index = sorted(
                        response.data,
                        key = lambda item: item.index
                    )

                    for chunk, embedding in zip(pending_batch, embeddings_by_index):
                        embedded_records.append(
                            {
                                "chunk_id":chunk["chunk_id"],
                                "embedding":embedding.embedding,
                                "document_id":chunk["document_id"],
                                "source_file":chunk["source_file"],
                                "section":chunk["section"],
                                "content":chunk["content"],
                                "checksum":chunk["checksum"],
                                "version":chunk["version"],
                                "effective_date":chunk["effective_date"],
                                "status":chunk["status"]
                            }
                        )

                        processed_ids.add(chunk["chunk_id"])

                    logging.info(f"Batch {batch_num} processed"
                                 f"({returned_count} embeddings)")

                    break

                except Exception as exc:
                    logging.warning(f"Batch {batch_num} failed."
                                    f"(attempt {attempt} / {max_retries}): {exc}")

                    if attempt == max_retries:
                        logging.error(f"Batch {batch_num} skipped")

                    else:
                        time.sleep(
                            2 ** attempt
                        )

        logging.info(f"Embedded {len(embedded_records)} chunks")

        return embedded_records