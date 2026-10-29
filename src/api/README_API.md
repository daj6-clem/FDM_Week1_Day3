The virtual environment can be created with "pip install -r requirements.txt"
All requirements/installed packages are in requirements.txt folder

Run Commands:
- For normal runs, use "uvicorn src.api.main:app --reload"
- For easy editing/reviewing changes, use "fastapi dev src/api/main.py"


EXISTING URLS:
/health/live
/health/ready

/customers
/customers/{customer_id} e.g. /customers/CUS001

/complaints
/complaints/{complaint_id} e.g. /complaints/CMP001
/complaints/customers/{customer_id} e.g. /complaints/customers/CUS001
