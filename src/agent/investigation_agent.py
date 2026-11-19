from typing import TypedDict, NotRequired, Literal # Defined dictionaries
from langchain_openai import ChatOpenAI
from langgraph.types import interrupt
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.services.complaint_service import ComplaintService
from src.config import BASE_URL, OPENAI_API_KEY
from datetime import date, datetime, timezone
from src.agent.tools import AgentTools
import json
from pathlib import Path

class EvidencePackage(TypedDict):
    operational_facts: list[dict]
    policy_chunks: list[dict]
    missing_items: list[str]
    contradictions: list[str]

class Classification(BaseModel):
    category: Literal[
        "Fee Dispute",
        "Service Delay",
        "Card Issue",
        "Customer Service",
        "Transaction Error",
        "Online Banking",
        "Fraud Claim"
    ]
    confidence: float

class CaseSummary(TypedDict):
    verified_facts: list[str]
    policy_evidence: list[str]
    analysis: str

class ProposedAction(TypedDict):
    action: str
    rationale: str
    approval_required: bool

class CaseSummaryOutput(BaseModel):
    verified_facts: list[str]
    policy_evidence: list[str]
    analysis: str

class ProposedActionOutput(BaseModel):
    action: str
    rationale: str
    approval_required: bool

class InvestigationState(TypedDict):
    complaint_id: str

    complaint_data: NotRequired[dict]

    complaint_category: NotRequired[str]
    classification: NotRequired[Classification]

    evidence: NotRequired[EvidencePackage]

    case_summary: NotRequired[CaseSummary]

    proposed_action: NotRequired[ProposedAction]

    recommendation_id: NotRequired[str]

    approval_request_id: NotRequired[str]
    approval_status: NotRequired[str]

    supervisor_feedback: NotRequired[str]
    rework_count: NotRequired[int]

    final_status: NotRequired[str]

class InvestigationAgent:
    def __init__(self, tools:AgentTools, llm:ChatOpenAI):
        self.tools = tools
        self.llm = llm
        self.trace_events = []
        self.trace_file = (Path(__file__).resolve().parents[0] / "agent_traces.json")
        self.graph = self.build_graph()

    # Needs complaint narrative, customer id, account id, existing complaint status
    def load_complaint(self, state: InvestigationState):
        complaint = self.tools.get_complaint(complaint_id = state["complaint_id"])
        return {
            "complaint_data": complaint
        }

    def classify_issue(self, state: InvestigationState):
        classifier = self.llm.with_structured_output(Classification)

        prompt = f"""
            Classify this complaint.

            Allowed categories:

            - Fee Dispute
            - Service Delay
            - Card Issue
            - Customer Service
            - Transaction Error
            - Online Banking
            - Fraud Claim

            Complaint:

            {state["complaint_data"]["details"]}
            """
        
        result = classifier.invoke(prompt)

        return {
            "classification": result.model_dump()
        }


    # Will call tools (getters for evidence)
    def gather_operational_evidence(self, state: InvestigationState):
        complaint = state["complaint_data"]
        customer = self.tools.get_customer(
            customer_id = complaint["customer_id"]
        )

        accounts = self.tools.get_accounts(
            customer_id = complaint["customer_id"]
        )

        operational_facts = [
            {
                "type": "customer",
                "data": customer
            },
            {
                "type": "accounts",
                "data": accounts
            }
        ]

        return {
            "evidence": {
                "operational_facts": operational_facts,
                "policy_chunks": [],
                "missing_items": [],
                "contradictions": []
            }
        }

    # Will call search_policy()
    def retrieve_policy_evidence(self, state: InvestigationState):
        category = state["classification"]["category"]

        query_map = {
            "Fee Dispute": "fee refund fee reversal overdraft fee policy",
            "Service Delay": "service level complaint escalation policy",
            "Card Issue": "card dispute card replacement policy",
            "Customer Service": "customer complaint resolution policy",
            "Transaction Error": "transaction error correction policy",
            "Online Banking": "online banking access issue policy",
            "Fraud Claim": "fraud investigation reimbursement policy"
        }

        policy_results = self.tools.search_policy(
            query=query_map.get(category, "customer complaint policy"),
            filters={},
            top_k = 5
        )

        evidence = state["evidence"]

        return {
            "evidence": {
                **evidence,
                "policy_chunks": policy_results
            }
        }

    def validate_evidence(self, state:InvestigationState):
        evidence = state["evidence"]
        missing = []
        contradictions = []

        if not evidence["policy_chunks"]:
            missing.append("policy")

        return {
            "evidence": {
                **evidence,
                "missing_items": missing,
                "contradictions": contradictions
            }
        }

    # Will generate gase summary using complaint narrative, operational facts, and policy chunks
    def create_case_summary(self, state: InvestigationState):
        summarizer = self.llm.with_structured_output(CaseSummaryOutput)

        supervisor_feedback = state.get(
            "supervisor_feedback",
            ""
        )

        result = summarizer.invoke(
            f"""
            Complaint:
            {state["complaint_data"]}

            Operational Facts:
            {state["evidence"]["operational_facts"]}

            Policy:
            {state["evidence"]["policy_chunks"]}

            Missing Evidence:
            {state["evidence"]["missing_items"]}

            Contradictions:
            {state["evidence"]["contradictions"]}

            Supervisor Feedback:
            {supervisor_feedback}

            Generate:
            - verified facts
            - policy evidence
            - analysis

            Address the supervisor's requested changes, if there are any.
            Do not present unverified information as fact.
            """
        )

        return {
            "case_summary": result.model_dump()
        }

    # Will return proposed action dict
    def propose_action(self, state: InvestigationState):
        recommender = self.llm.with_structured_output(
            ProposedActionOutput
        )

        result = recommender.invoke(
            f"""
            Case Summary:
            {state["case_summary"]}

            Supervisor Feedback:
            {state.get("supervisor_feedback", "")}

            Recommend next action.

            Address the supervisor's requested changes.
            Explain the rationale.
            Identify whether supervisor approval is required.
            """        
        )

        return {
            "proposed_action": result.model_dump()
        }

    def save_recommendation(self, state:InvestigationState):
        recommendation_text = f"""
            Action: {state["proposed_action"]["action"]}

            Rationale:
            {state["proposed_action"]["rationale"]}

            Approval Required:
            {state["proposed_action"]["approval_required"]}
            """
        recommendation = self.tools.create_recommendation(
            investigation_id = state["complaint_id"],
            recommendation_text = recommendation_text,
            confidence_score = state["classification"]["confidence"]
        )

        return {
            "recommendation_id": recommendation["recommendation_id"]
        }

    # Will call request_approval from tools
    def request_supervisor_review(self, state: InvestigationState):
        approval = self.tools.request_approval(
            complaint_id = state["complaint_id"],
            action = state["proposed_action"]["action"],
            parameters = {},
            evidence_refs = []
        )

        return {
            "approval_request_id": approval["approval_id"]
        }

    def wait_for_approval(self, state: InvestigationState):
        response = interrupt({
            "approval_request_id": state["approval_request_id"],
            "proposed_action": state["proposed_action"]
        })

        if isinstance(response, dict):
            decision = response["decision"]
            feedback = response.get("feedback", "")
        else:
            decision = response
            feedback = ""

        return {
            "approval_status": decision,
            "supervisor_feedback": feedback
        }

    def finalize_case(self, state:InvestigationState):
        self.tools.update_complaint_status(
            complaint_id = state["complaint_id"],
            target_status = "Closed",
            reason = "Investigation complete"
        )
        self.tools.close_complaint(
            complaint_id = state["complaint_id"],
            resolution = state["proposed_action"]["action"],
            communication_date = date.today().isoformat(),
            evidence_refs = []
        )
        return {
            "final_status": "Closed"
        }

    def rework_case(self, state:InvestigationState):
        feedback = state.get("supervisor_feedback", "")

        rework_count = state.get("rework_count", 0) + 1

        return {
            "rework_count": rework_count,
            "supervisor_feedback": feedback
        }

    def record_supervisor_decision(self, state: InvestigationState):
        decision = state["approval_status"]

        reason = (
            state.get("supervisor_feedback")
            or f"Supervisor decision: {decision}"
        )

        self.tools.record_approval_decision(
            approval_id = state["approval_request_id"],
            decision = decision,
            reason = reason
        )

        return {}

    def approval_router(self, state: InvestigationState):
        if state["proposed_action"]["approval_required"]:
            return "request_review"

        return "finalize_case"

    def supervisor_router(self, state):
        decision = state["approval_status"]
        if decision == "approved":
            return "finalize_case"

        if decision == "rejected":
            return "rejected"

        if decision == "changes_requested":
            return "rework"

        raise ValueError(
            f"Unsupported supervisor decision: {decision}"
        )

    def build_graph(self):
        graph = StateGraph(InvestigationState)

        graph.set_entry_point("load_complaint")

        graph.add_node("load_complaint", self._trace_node("load_complaint", self.load_complaint))
        graph.add_node("classify_issue", self._trace_node("classify_issue", self.classify_issue))
        graph.add_node("gather_evidence", self._trace_node("gather_operational_evidence", self.gather_operational_evidence))
        graph.add_node("retrieve_policy", self._trace_node("retrieve_policy_evidence", self.retrieve_policy_evidence))
        graph.add_node("validate_evidence", self._trace_node("validate_evidence", self.validate_evidence))
        graph.add_node("create_summary", self._trace_node("create_case_summary", self.create_case_summary))
        graph.add_node("propose_action", self._trace_node("propose_action", self.propose_action))
        graph.add_node("save_recommendation", self._trace_node("save_recommendation", self.save_recommendation))
        graph.add_node("request_review", self._trace_node("request_supervisor_review", self.request_supervisor_review))
        graph.add_node("wait_for_approval", self._trace_node("wait_for_approval", self.wait_for_approval))

        graph.add_node("record_supervisor_decision", self._trace_node("record_supervisor_decision", self.record_supervisor_decision))
        graph.add_node("rework", self._trace_node("rework_case", self.rework_case))
        graph.add_node("finalize_case", self._trace_node("finalize_case", self.finalize_case))

        graph.add_edge("load_complaint", "classify_issue")
        graph.add_edge("classify_issue", "gather_evidence")
        graph.add_edge("gather_evidence", "retrieve_policy")
        graph.add_edge("retrieve_policy", "validate_evidence")
        graph.add_edge("validate_evidence", "create_summary")
        graph.add_edge("create_summary", "propose_action")
        graph.add_edge("propose_action", "save_recommendation")
        graph.add_conditional_edges("save_recommendation", self.approval_router,
                                    {
                                        "request_review": "request_review",
                                        "finalize_case": "finalize_case"
                                    })
        graph.add_edge("request_review", "wait_for_approval")
        graph.add_edge("wait_for_approval", "record_supervisor_decision")
        graph.add_conditional_edges("record_supervisor_decision", self.supervisor_router,
                                    {
                                        "finalize_case": "finalize_case",
                                        "rejected": END,
                                        "rework": "rework"
                                    })
        graph.add_edge("rework", "create_summary")
        graph.add_edge("finalize_case", END)

        return graph.compile()

    def investigate(self, complaint_id: str):
        self.trace_events = []

        self.trace_file.write_text(
            "[]",
            encoding="utf-8"
        )

        return self.graph.invoke({"complaint_id": complaint_id})

    def _json_safe(self, value):

        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")

        if isinstance(value, dict):
            return {
                key: self._json_safe(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [self._json_safe(item) for item in value]

        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        return str(value)

    def _trace_node(self, node_name, node_function):
        """Wrap a graph node and record its execution."""

        def traced_function(state):
            started_at = datetime.now(timezone.utc)

            event = {
                "node": node_name,
                "started_at": started_at.isoformat(),
                "input": self._json_safe(state),
                "status": "success"
            }

            try:
                result = node_function(state)

                event["output"] = self._json_safe(result)

                return result

            except Exception as exc:
                event["status"] = "error"
                event["error"] = str(exc)
                raise

            finally:
                event["finished_at"] = datetime.now(
                    timezone.utc
                ).isoformat()

                self.trace_events.append(event)

                self.trace_file.write_text(
                    json.dumps(
                        self.trace_events,
                        indent=4
                    ),
                    encoding="utf-8"
                )

        return traced_function