import os
import logging
import chromadb
import json

class VectorStoreService:

    approved_metadata = {
        "document_id",
        "source_file",
        "section",
        "checksum",
        "version",
        "effective_date",
        "status"
    }

    def __init__(self, persist_directory, collection_name = "document_chunks"):
        os.makedirs(persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(path = persist_directory)

        self.collection_name = collection_name

        self.collection = self.client.get_or_create_collection(
            name = collection_name, metadata={"hnsw:space":"cosine"}
        )

        logging.basicConfig(level = logging.INFO, format="%(asctime)s - %(message)s")

    def prepare_metadata(self, record):
        metadata = {
            key:record[key]
            for key in self.approved_metadata
            if key in record and record[key] is not None
        }

        for key, value in metadata.items():
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError(
                    f"Invalid metadata value: {key}"
                )

        return metadata

    def rebuild(self):
        logging.warning("Starting full vector index rebuild")

        try:
            self.client.delete_colelction(name = self.collection_name)

        except Exception:
            pass

        self.collection = self.client.create_collection(
            name = self.collection_name,
            metadata = {"hnsw:space":"cosine"}
        )

        logging.info("Vector collection recreated")

    def persist(self, embedded_records, batch_size = 500):
        logging.info(f"Persisting {len(embedded_records)} embedded chunks")

        if not embedded_records:
            logging.warning("No records to persist")

            return

        processed = 0

        for start in range(0, len(embedded_records), batch_size):
            batch = embedded_records[start:start + batch_size]
            ids = [record["chunk_id"] for record in batch]
            documents = [record["content"] for record in batch]
            embeddings = [record["embedding"] for record in batch]
            metadatas = [self.prepare_metadata(record) for record in batch]

            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate chunk IDs found in batch")

            if any(not embedding for embedding in embeddings):
                raise ValueError("Empty embedding detected")

            dimensions = {len(embedding) for embedding in embeddings}

            if len(dimensions) != 1:
                raise ValueError("Inconsistent embedding dimensions")

            self.collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

            processed += len(batch)

            logging.info(f"Vector batch processed: "
                        f"{processed}/{len(embedded_records)}")
        logging.info(f"Successfully persisted {processed} vectors")

    def get_collection_count(self):
        return self.collection.count()

    def validate_index(self, expected_chunks, expected_dimensions=1536, batch_size=500, output_path="data/processed/vector_index_validation.json"):
        logging.info("Starting vector index validation.")

        # Expected chunk count

        chunk_ids = [chunk["chunk_id"] for chunk in expected_chunks]

        chunk_count = len(chunk_ids)

        duplicate_chunk_ids = (len(chunk_ids) != len(set(chunk_ids)))

        # Vector Count
        vector_count = self.collection.count()
        logging.info(f"Chunk count: {chunk_count}")
        logging.info(f"Vector count: {vector_count}")

        # Initialize validation counters

        dimension_errors = 0
        missing_metadata = 0
        stored_ids = []

        required_metadata = {
            "source_file"
        }

        # Read Stored vectors in batches
        offset = 0

        while offset < vector_count:
            results = self.collection.get(
                limit=batch_size,
                offset=offset,
                include=[
                    "embeddings",
                    "metadatas"
                ]
            )

            ids = results["ids"]
            embeddings = results["embeddings"]
            metadatas = results["metadatas"]

            for i, chunk_id in enumerate(ids):
                stored_ids.append(chunk_id)

                # check vector dimensions

                vector = embeddings[i]

                if (vector is None or len(vector) != expected_dimensions):
                    dimension_errors += 1

                # check metadata

                metadata = metadatas[i] or {}

                missing_fields = {
                    key for key in required_metadata
                    if not metadata.get(key)
                }

                # chunk_id is stored as the ChromaDB ID
                if not chunk_id:
                    missing_fields.add("chunk_id")

                missing_metadata += len(missing_fields)

            offset += len(ids)

            if not ids:
                break

        # Test 1: Vector Count
        test_1 = (chunk_count == vector_count)

        # Test 2 vector dimensions
        test_2 = (dimension_errors == 0)

        # Test 3 rebuild integ
        duplicate_stored_ids = (len(stored_ids) != len(set(stored_ids)))

        test_3 = (missing_metadata == 0 and not duplicate_chunk_ids and not duplicate_stored_ids)

        # Overall status
        status = (
            "PASS"
            if all([test_1, test_2, test_3])
            else "FAIL"
        )

        # Generate Report
        report = {
            "chunk_count": chunk_count,
            "vector_count": vector_count,
            "dimensions": expected_dimensions,
            "missing_metadata": missing_metadata,
            "status": status
        }

        # Save
        os.makedirs(
            os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent = 4)

        logging.info("===== VECTOR INDEX VALIDATION =====")

        logging.info(
            f"vector_count_matches_chunks: "
            f"{'PASS' if test_1 else 'FAIL'}"
        )

        logging.info(
            f"all_vectors_have_source_id: "
            f"{'PASS' if test_2 else 'FAIL'}"
        )

        logging.info(
            f"rebuild_has_no_duplicates: "
            f"{'PASS' if test_3 else 'FAIL'}"
        )

        logging.info(f"Overall status: {status}")

        logging.info(
            f"Validation report saved: {output_path}"
        )

        return report