### INDEX AND FILTER DESIGN ###

### Vector Index:
Purpose - Semantic Similarity search against chunk embeddings
Fields:
- chunk_text

### Text Index:
Purpose - Keyword Search
Fields:
- title
- section_name

### Metadata Index:
Purpose - Filtering and Compliance
Fields:
- source_id
- version
- effective_date
- access_label
- document_type

### Access Filtering:
EX: access_label == user_access_level -> Can access/cite
access_label != user_access_level -> Cannot access/cite

### Citation Mapping:
source_id
section
answer
source

