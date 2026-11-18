from __future__ import annotations

import datetime as dt
import json
import re
import uuid
from typing import Any, Iterable, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from data.connection import SessionLocal
from src.dependencies import get_retrieval_service
from src.rag.retrieval_service import RetrievalService
from src.rag.answer_service import AnswerService
from src.services.complaint_service import ComplaintService
from src.services.customer_service import CustomerService
from src.services.account_service import AccountService
from data.repositories.complaint_note_repository import ComplaintNoteRepository
from data.repositories.recommendation_repository import RecommendationRepository
from data.repositories.review_decision_repository import ReviewDecisionRepository
from data.repositories.review_request_repository import ReviewRequestRepository
from data.repositories.audit_log_repository import AuditLogRepository
from src.models.models import AuditLog, Recommendation, ComplaintNote, ComplaintStatus, ComplaintStatusHistory, Complaint, ReviewDecision, ReviewRequest

###
# Tools should have one bounded purpose
# Inputs and outputs should be typed and validated
# Authorization should be enforced by tool boundary, not trusted to the model
# Sensitive actions require explicit approval
# Tool Failures return controlled errors and do not fabricate data
# Every action produces audit evidence
###

class AgentTools:

    def __init__ (self, db:Session, audit_log_repository: AuditLogRepository, complaint_note_repository:ComplaintNoteRepository, recommendation_repository: RecommendationRepository, review_decision_repository:ReviewDecisionRepository, review_request_repository:ReviewRequestRepository, complaint_service: ComplaintService, account_service:AccountService, customer_service:CustomerService, retrieval_service: RetrievalService, answer_service: AnswerService):
        self.complaint_service = complaint_service
        self.account_service = account_service
        self.customer_service = customer_service
        self.retrieval_service = retrieval_service
        self.answer_service = answer_service
        self.complaint_note_repository = complaint_note_repository
        self.recommendation_repository = recommendation_repository
        self.review_decision_repository = review_decision_repository
        self.review_request_repository = review_request_repository
        self.audit_log_repository = audit_log_repository
        self.db = db

    def success(self, data):
        return {
            "success": True,
            "data": data,
            "error": None
        }

    def error(self, code, message):
        return {
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message
            }
        }

    # outputs customer record or not_found
    # Read only; BR-004/027
    # analyst/supervisor
    def get_customer(self, customer_id: str):
        print("getting customer")
        return self.customer_service.get_by_id(customer_id)

    # outputs account summaries
    # Read only, minimize fields
    # analyst/supervisor
    def get_accounts(self, customer_id: str):
        print("getting accounts")
        return self.account_service.get_for_customer(customer_id)

    # outputs complaint details/history
    # Read only
    # analyst/supervisor
    def get_complaint(self, customer_id: str):
        print("getting complaint")
        return self.complaint_service.get_for_customer(customer_id)

    # outputs ranked evidence with metadata
    # Current version/access filters
    # analyst/supervisor
    def search_policy(self, query: str, filters: object, top_k: int):
        print("searching policy")
        # RAG database, go through RAG pipeline
        # Retrieve approved Policy Chunks
        chunks = self.retrieval_service.retrieve(
            query, 
            top_k, 
            document_type = filters.document_type, 
            version = filters.version,
            access_label = filters.access_label,
            rerank = True
        )

        return chunks

    # outputs note ID/audit event
    # Parameterized, no secrets
    # Analyst, Supervisor
    def create_case_note(self, complaint_id: str, note: str, evidence_refs:list[str]):
        print("creating case note")
        # verify case exists
        # create note
        # Create audit event
        # return note id
        # sqlalchemy row create

        complaint = self.complaint_service.get_by_id(complaint_id)
        if not complaint:
            return self.error(
                "COMPLAINT_NOT_FOUND", f"Complaint {complaint_id} not found"
            )

        case_note = ComplaintNote(
            note_id=str(uuid.uuid4()),
            complaint_id=complaint_id,
            note_text = note,
            evidence_refs = json.dumps(evidence_refs),
            created_at = dt.datetime.utcnow()
        )

        self.complaint_note_repository.create(case_note)

        # Do an audit create here
        audit_log = AuditLog(
            entity_name = "COMPLAINT",
            entity_id = complaint_id,
            action_type = "CASE_NOTE_CREATED",
            performed_by = complaint.assigned_analyst_id,
            event_timestamp = dt.datetime.utcnow(),
            details = f"Created note {case_note.note_id}"
        )

        self.audit_log_repository.create(audit_log)

        return self.success({
            "note_id": case_note.note_id,
            "audit_id": audit_log.audit_id
        })

    # Outputs approval request ID/status
    # Case-specific; BR-029
    # Analyst
    def request_approval(self, complaint_id: str, action: str, parameters: list, evidence_refs:list[str]):
        print("requesting approval")
        # unsure how this is meant to work
        # Request approval for current proposed action
        # sqlalchemy create?
        # THIS MAPS TO TABLE REVIEW REQUEST

        recommendation = Recommendation(
            recommendation_id = str(uuid.uuid4()),
            investigation_id = "TEMP",
            recommendation_text = action,
            confidence_score = 1.0
        )

        recommendation = self.recommendation_repository.create(recommendation)

        complaint = self.complaint_service.get_by_id(complaint_id)
        if not complaint:
            return self.error(
                "COMPLAINT_NOT_FOUND",
                f"Complaint {complaint_id} was not found."
            )

        review_request = ReviewRequest(
            review_request_id = str(uuid.uuid4()),
            complaint_id = complaint_id,
            recommendation_id = recommendation.recommendation_id,
            reviewer_id = complaint.assigned_analyst_id,
            requested_at = dt.datetime.utcnow(),
            status = "PENDING"
        )

        self.review_request_repository.create(review_request)

        return self.success({
            "review_request_id": review_request.review_request_id,
            "status": review_request.status
        })


    # Outputs decision/audit event
    # Human Only
    # Supervisor
    def record_approval_decision(self, approval_id: str, decision: str, reason: str):
        print("recording approval decision")
        # unsure
        # approve/reject request
        # sqlalchemy update
        # THIS MAPS WELL TO TABLE REVIEW_DECISION
        review_decision = ReviewDecision(
            decision_id = str(uuid.uuid4()),
            review_request_id = approval_id,
            decision = decision,
            decision_reason = reason,
            decision_date = dt.datetime.utcnow()
        )

        self.review_decision_repository.create(review_decision)

        review_request = (self.review_request_repository.get_by_id(approval_id))
        if review_request:
            review_request.status = decision
            self.review_request_repository.update(review_request)


        # Insert Audit Log Create statement here
        audit_log = AuditLog(
            entity_name = "REVIEW_DECISION",
            entity_id = review_decision.decision_id,
            action_type = "UPDATE",
            event_timestamp = dt.datetime.utcnow(),
            details = f"Decision {review_decision.decision_id}"
        )

        self.audit_log_repository.create(audit_log)

        return self.success({
            "decision_id": review_decision.decision_id,
            "audit_id": audit_log.audit_id
        })


    # Outputs new status/audit event
    # Transition validation
    # Authorized role
    def update_complaint_status(self, complaint_id: str, target_status: str, reason: str):
        print("updating complaints status")
        # sqlalchemy update
        # apply allowed status transition

        complaint = self.complaint_service.change_status(self.db, complaint_id, target_status)

        #audit create statement
        audit_log = AuditLog(
            entity_name = "COMPLAINT",
            entity_id = complaint.complaint_id,
            action_type = "UPDATE",
            performed_by = complaint.assigned_analyst_id,
            event_timestamp = dt.datetime.utcnow(),
            details = f"Updated complaint status to {complaint.status}"
        )

        self.audit_log_repository.create(audit_log)

        return {
            "status": complaint.status,
            "audit_id": audit_log.audit_id
        }

    # Outputs closed case/audit event
    # Sensitive; BR-018/038
    # Supervisor
    def close_complaint(self, complaint_id: str, resolution: str, communication_date: str, evidence_refs:list[str]):
        print("closing complaint")
        # sqlalchemy update
        # close case after evidence/approval validation

        complaint = self.complaint_service.change_status(self.db, complaint_id, ComplaintStatus.CLOSED)

        # Audit Create statement
        audit_log = AuditLog(
            entity_name = "COMPLAINT",
            entity_id = complaint.complaint_id,
            action_type = "CLOSE",
            event_timestamp = dt.datetime.utcnow(),
            details = f"Closed complaint {complaint.complaint_id}"
        )

        self.audit_log_repository.create(audit_log)

        return self.success({
            "complaint_id": complaint_id,
            "status": "Closed",
            "audit_id": audit_log.audit_id
        })