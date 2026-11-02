Boundary note - Complaint and Initial Status event form one transaction
- This occurs in the complaint create() function in complaint_service, as it is a business rule.
- The two events are within the same try block, with the commit occuring after both
- There are no commits in the repositories, only in the service layer

DATABASE INSPECTION
- Upon forcing a failure for the second write, I expect to see that the database holds neither the complaint nor the complaint_status_history
- I will be testing with the values below, and forcing an exception to be raised within self.sch_repo.create()
- the code for doing so is the following: "raise Exception("simulate history write failure")"
- If my code was written properly, it will rollback before the commit
- If my code was not written properly, the test value will be the last value in the Complaint and Complaint_Status_History tables

TEST: CMP035
{
  "customer_id": "CUS002",
  "account_id": "ACC002",
  "channel": "Phone",
  "category": "Fee Dispute",
  "complaint_text": "Forced Failure on Second Write",
  "priority": "Low",
  "status": "Open",
  "received_at": "2026-10-30T19:19:43.125Z",
  "assigned_analyst_id": "string"
}

OUTPUT:
Exception: simulate history write failure

COMPLAINT_STATUS_HISTORY LAST ENTRY:
  {
    "new_status": "Under Review",
    "history_id": 34,
    "changed_at": "2026-10-30T16:01:53.698949",
    "changed_by": "EMP002",
    "complaint_id": "CMP002",
    "old_status": "In Progress",
    "comments": null
  }


GET COMPLAINT CMP035:
{
  "detail": "No complaint with id = CMP035."
}



IDEMPOTENCY CONSIDERATION
- The POST /complaints call is not idempotent. Duplicate requests will result in duplicate complaints. And since a customer can submit multiple complaints, it is likely to occur.