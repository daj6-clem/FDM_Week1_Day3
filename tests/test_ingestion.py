import os
import unittest
import tempfile

from src.rag.ingestion_service import validate_manifest

# [
#   {
#     "case": "valid_manifest",
#     "expected": "accept"
#   },
#   {
#     "case": "unlisted_file",
#     "expected": "reject"
#   },
#   {
#     "case": "duplicate_source_id",
#     "expected": "reject"
#   },
#   {
#     "case": "missing_effective_date",
#     "expected": "reject"
#   }
# ]

class TestManifestValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_file(self, filename):

        file_path = os.path.join(
            self.directory_path,
            filename
        )

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            file.write("Test document")

        return file_path

    def create_manifest_row(
        self,
        source_id="DOC001",
        relative_path="document1.docx",
        effective_date="2026-01-01"
    ):

        return {
            "source_id": source_id,
            "relative_path": relative_path,
            "version": "1.0",
            "effective_date": effective_date,
            "status": "approved"
        }

    # Test 1: Valid manifest
    def test_valid_manifest(self):

        self.create_file("document1.docx")

        manifest_docs = [
            self.create_manifest_row()
        ]

        validated_docs, counts = validate_manifest(
            self.directory_path,
            manifest_docs
        )

        self.assertEqual(len(validated_docs), 1)
        self.assertEqual(counts["accepted"], 1)
        self.assertEqual(counts["rejected"], 0)

    # Test 2: Unlisted file
    def test_unlisted_file(self):

        self.create_file("document1.docx")
        self.create_file("unlisted.docx")

        manifest_docs = [
            self.create_manifest_row()
        ]

        validated_docs, counts = validate_manifest(
            self.directory_path,
            manifest_docs
        )

        self.assertEqual(counts["accepted"], 1)
        self.assertEqual(counts["rejected"], 1)

    # Test 3: Duplicate source ID
    def test_duplicate_source_id(self):

        self.create_file("document1.docx")
        self.create_file("document2.docx")

        manifest_docs = [
            self.create_manifest_row(
                source_id="DOC001",
                relative_path="document1.docx"
            ),
            self.create_manifest_row(
                source_id="DOC001",
                relative_path="document2.docx"
            )
        ]

        validated_docs, counts = validate_manifest(
            self.directory_path,
            manifest_docs
        )

        self.assertEqual(len(validated_docs), 0)
        self.assertEqual(counts["accepted"], 0)
        self.assertEqual(counts["rejected"], 2)

    # Test 4: Missing effective date
    def test_missing_effective_date(self):

        self.create_file("document1.docx")

        manifest_docs = [
            self.create_manifest_row(
                effective_date=""
            )
        ]

        validated_docs, counts = validate_manifest(
            self.directory_path,
            manifest_docs
        )

        self.assertEqual(len(validated_docs), 0)
        self.assertEqual(counts["accepted"], 0)
        self.assertEqual(counts["rejected"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)