##### DOCUMENT AND CHUNK SCHEMAS #####

### FIELD           ### DESCRIPTION
source_id	        Unique document identifier
title	            Document title
version	            Document version
effective_date	    Date document becomes active
document_type	    Procedure, Guide, Matrix etc.
access_label	    Internal, Restricted
filename	        Physical file name
checksum	        Detect document changes
ingestion_date	    Date added to KB


### VALIDATION RULES:
•	source_id cannot be empty
•	source_id must be unique
•	version is mandatory
•	effective_date must be a valid date
•	access_label must be Internal or Restricted
•	filename must exist
•	checksum must be generated


### CHUNK FIELDS:
### FIELD           ### DESCRIPTION
chunk_id            Unique chunk identifier
source_id           Original document ID
section_name        Document heading
sequence_number     Position in document
text                Chunk content
access_label        Security label
version             Source version
