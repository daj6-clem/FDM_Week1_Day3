
import pytest
from unittest.mock import Mock
import json

from src.agent.investigation_agent import InvestigationAgent


@pytest.fixture
def mock_tools():
    return Mock()


@pytest.fixture
def mock_llm():
    return Mock()


@pytest.fixture
def agent(mock_tools, mock_llm):
    return InvestigationAgent(
        tools=mock_tools,
        llm=mock_llm
    )


def test_load_complaint(agent):
    agent.tools.get_complaint.return_value = {
        "complaint_id": "CMP-001",
        "customer_id": "CUS-001",
        "details": "Customer claims an unauthorized fee was charged.",
        "account_id": "ACC-001"
    }

    state = {
        "complaint_id": "CMP-001"
    }

    result = agent.load_complaint(state)

    agent.tools.get_complaint.assert_called_once_with(
        complaint_id="CMP-001"
    )

    assert isinstance(result, dict)
    assert "complaint_data" in result
    assert result["complaint_data"]["complaint_id"] == "CMP-001"
    assert result["complaint_data"]["customer_id"] == "CUS-001"


def test_classify_issue(agent):
    classification = Mock()
    classification.model_dump.return_value = {
        "category": "Fee Dispute",
        "confidence": 0.95
    }

    agent.llm.with_structured_output.return_value.invoke.return_value = (
        classification
    )

    state = {
        "complaint_id": "CMP-001",
        "complaint_data": {
            "details": "Customer claims an unauthorized fee was charged."
        }
    }

    result = agent.classify_issue(state)

    agent.llm.with_structured_output.assert_called_once()
    agent.llm.with_structured_output.return_value.invoke.assert_called_once()

    assert isinstance(result, dict)
    assert "classification" in result
    assert result["classification"]["category"] == "Fee Dispute"
    assert result["classification"]["confidence"] == 0.95


def test_gather_operational_evidence(agent):
    agent.tools.get_customer.return_value = {
        "customer_id": "CUS-001",
        "name": "Test Customer"
    }

    agent.tools.get_accounts.return_value = [
        {"account_id": "ACC-001"}
    ]

    state = {
        "complaint_id": "CMP-001",
        "complaint_data": {
            "complaint_id": "CMP-001",
            "customer_id": "CUS-001",
            "account_id": "ACC-001"
        }
    }

    result = agent.gather_operational_evidence(state)

    agent.tools.get_customer.assert_called_once_with(
        customer_id="CUS-001"
    )

    agent.tools.get_accounts.assert_called_once_with(
        customer_id="CUS-001"
    )

    assert isinstance(result, dict)
    assert "evidence" in result

    evidence = result["evidence"]

    assert len(evidence["operational_facts"]) == 2
    assert evidence["operational_facts"][0]["type"] == "customer"
    assert evidence["operational_facts"][1]["type"] == "accounts"

    assert evidence["policy_chunks"] == []
    assert evidence["missing_items"] == []
    assert evidence["contradictions"] == []


def test_workflow_happy_path():
    tools = Mock()
    llm = Mock()

    tools.get_complaint.return_value = {
        "complaint_id": "CMP-001",
        "customer_id": "CUS-001",
        "details": "Customer claims an unauthorized fee was charged.",
        "account_id": "ACC-001"
    }

    tools.get_customer.return_value = {
        "customer_id": "CUS-001",
        "name": "Test Customer"
    }

    tools.get_accounts.return_value = [
        {"account_id": "ACC-001"}
    ]

    classification = Mock()
    classification.model_dump.return_value = {
        "category": "Fee Dispute",
        "confidence": 0.95
    }

    llm.with_structured_output.return_value.invoke.return_value = (
        classification
    )

    agent = InvestigationAgent(
        tools=tools,
        llm=llm
    )

    state = {
        "complaint_id": "CMP-001"
    }

    # Load complaint
    state.update(agent.load_complaint(state))

    # Classify complaint
    state.update(agent.classify_issue(state))

    # Gather operational evidence
    state.update(agent.gather_operational_evidence(state))

    # Verify final state
    assert state["complaint_data"]["complaint_id"] == "CMP-001"
    assert state["complaint_data"]["customer_id"] == "CUS-001"

    assert state["classification"]["category"] == "Fee Dispute"
    assert state["classification"]["confidence"] == 0.95

    assert len(state["evidence"]["operational_facts"]) == 2

    assert state["evidence"]["operational_facts"][0]["type"] == "customer"
    assert state["evidence"]["operational_facts"][1]["type"] == "accounts"

    tools.get_complaint.assert_called_once_with(
        complaint_id="CMP-001"
    )

    tools.get_customer.assert_called_once_with(
        customer_id="CUS-001"
    )

    tools.get_accounts.assert_called_once_with(
        customer_id="CUS-001"
    )


# --------------------------------------------------
# Policy retrieval tests
# --------------------------------------------------

def test_retrieve_policy_evidence(agent):
    policy_chunks = [
        {
            "chunk_id": "KB-001",
            "text": "Fees may be reversed under approved circumstances."
        }
    ]

    agent.tools.search_policy.return_value = policy_chunks

    state = {
        "classification": {
            "category": "Fee Dispute",
            "confidence": 0.95
        },
        "evidence": {
            "operational_facts": [],
            "policy_chunks": [],
            "missing_items": [],
            "contradictions": []
        }
    }

    result = agent.retrieve_policy_evidence(state)

    agent.tools.search_policy.assert_called_once_with(
        query="fee refund fee reversal overdraft fee policy",
        filters={},
        top_k=5
    )

    assert "evidence" in result
    assert result["evidence"]["policy_chunks"] == policy_chunks
    assert result["evidence"]["operational_facts"] == []


# --------------------------------------------------
# Evidence validation tests
# --------------------------------------------------

def test_validate_evidence_with_policy(agent):
    state = {
        "evidence": {
            "operational_facts": [],
            "policy_chunks": [
                {"chunk_id": "KB-001"}
            ],
            "missing_items": [],
            "contradictions": []
        }
    }

    result = agent.validate_evidence(state)

    assert result["evidence"]["missing_items"] == []
    assert result["evidence"]["contradictions"] == []
    assert len(result["evidence"]["policy_chunks"]) == 1


def test_validate_evidence_without_policy(agent):
    state = {
        "evidence": {
            "operational_facts": [],
            "policy_chunks": [],
            "missing_items": [],
            "contradictions": []
        }
    }

    result = agent.validate_evidence(state)

    assert "policy" in result["evidence"]["missing_items"]
    assert result["evidence"]["contradictions"] == []


# --------------------------------------------------
# Case summary tests
# --------------------------------------------------

def test_create_case_summary(agent):
    summary = Mock()

    summary.model_dump.return_value = {
        "verified_facts": [
            "Customer reported an unauthorized fee."
        ],
        "policy_evidence": [
            "Policy permits fee reversals under certain conditions."
        ],
        "analysis": "The complaint requires further review."
    }

    agent.llm.with_structured_output.return_value.invoke.return_value = (
        summary
    )

    state = {
        "complaint_data": {
            "complaint_id": "CMP-001",
            "details": "Customer claims an unauthorized fee."
        },
        "evidence": {
            "operational_facts": [
                {"type": "customer", "data": {"customer_id": "CUS-001"}}
            ],
            "policy_chunks": [
                {"chunk_id": "KB-001"}
            ],
            "missing_items": [],
            "contradictions": []
        }
    }

    result = agent.create_case_summary(state)

    agent.llm.with_structured_output.assert_called_once()
    agent.llm.with_structured_output.return_value.invoke.assert_called_once()

    assert "case_summary" in result
    assert result["case_summary"]["verified_facts"] == [
        "Customer reported an unauthorized fee."
    ]
    assert result["case_summary"]["analysis"] == (
        "The complaint requires further review."
    )


# --------------------------------------------------
# Proposed action tests
# --------------------------------------------------

def test_propose_action(agent):
    proposed_action = Mock()

    proposed_action.model_dump.return_value = {
        "action": "Reverse the disputed fee.",
        "rationale": "The fee appears inconsistent with policy.",
        "approval_required": True
    }

    agent.llm.with_structured_output.return_value.invoke.return_value = (
        proposed_action
    )

    state = {
        "case_summary": {
            "verified_facts": ["Customer reported an unauthorized fee."],
            "policy_evidence": ["Fee reversal policy applies."],
            "analysis": "The fee should be reviewed."
        }
    }

    result = agent.propose_action(state)

    agent.llm.with_structured_output.assert_called_once()
    agent.llm.with_structured_output.return_value.invoke.assert_called_once()

    assert "proposed_action" in result
    assert result["proposed_action"]["action"] == (
        "Reverse the disputed fee."
    )
    assert result["proposed_action"]["approval_required"] is True


# --------------------------------------------------
# Recommendation persistence tests
# --------------------------------------------------

def test_save_recommendation(agent):
    agent.tools.create_recommendation.return_value = {
        "recommendation_id": "REC-001"
    }

    state = {
        "complaint_id": "CMP-001",
        "classification": {
            "category": "Fee Dispute",
            "confidence": 0.95
        },
        "proposed_action": {
            "action": "Reverse the disputed fee.",
            "rationale": "The fee appears inconsistent with policy.",
            "approval_required": True
        }
    }

    result = agent.save_recommendation(state)

    agent.tools.create_recommendation.assert_called_once()

    call_args = agent.tools.create_recommendation.call_args.kwargs

    assert call_args["investigation_id"] == "CMP-001"
    assert "Reverse the disputed fee." in call_args["recommendation_text"]
    assert "The fee appears inconsistent with policy." in (
        call_args["recommendation_text"]
    )
    assert call_args["confidence_score"] == 0.95

    assert result["recommendation_id"] == "REC-001"


# --------------------------------------------------
# Supervisor approval request tests
# --------------------------------------------------

def test_request_supervisor_review(agent):
    agent.tools.request_approval.return_value = {
        "approval_id": "APR-001"
    }

    state = {
        "complaint_id": "CMP-001",
        "proposed_action": {
            "action": "Reverse the disputed fee.",
            "rationale": "The fee appears inconsistent with policy.",
            "approval_required": True
        }
    }

    result = agent.request_supervisor_review(state)

    agent.tools.request_approval.assert_called_once_with(
        complaint_id="CMP-001",
        action="Reverse the disputed fee.",
        parameters={},
        evidence_refs=[]
    )

    assert result["approval_request_id"] == "APR-001"


# --------------------------------------------------
# Approval interruption test
# --------------------------------------------------

def test_wait_for_approval(agent, monkeypatch):
    import src.agent.investigation_agent as investigation_module

    monkeypatch.setattr(
        investigation_module,
        "interrupt",
        lambda payload: "approved"
    )

    state = {
        "approval_request_id": "APR-001",
        "proposed_action": {
            "action": "Reverse the disputed fee."
        }
    }

    result = agent.wait_for_approval(state)

    assert result["approval_status"] == "approved"
    assert result["supervisor_feedback"] == ""

def test_wait_for_approval_changes_requested(agent, monkeypatch):
    import src.agent.investigation_agent as investigation_module

    supervisor_response = {
        "decision": "changes_requested",
        "feedback": "Provide additional transaction evidence."
    }

    monkeypatch.setattr(
        investigation_module,
        "interrupt",
        lambda payload: supervisor_response
    )

    state = {
        "approval_request_id": "APR-001",
        "proposed_action": {
            "action": "Reverse the disputed fee."
        }
    }

    result = agent.wait_for_approval(state)

    assert result["approval_status"] == "changes_requested"
    assert result["supervisor_feedback"] == (
        "Provide additional transaction evidence."
    )


# --------------------------------------------------
# Case finalization tests
# --------------------------------------------------

def test_finalize_case(agent):
    state = {
        "complaint_id": "CMP-001",
        "proposed_action": {
            "action": "Reverse the disputed fee.",
            "rationale": "The fee appears inconsistent with policy.",
            "approval_required": True
        }
    }

    result = agent.finalize_case(state)

    agent.tools.update_complaint_status.assert_called_once_with(
        complaint_id="CMP-001",
        target_status="Closed",
        reason="Investigation complete"
    )

    agent.tools.close_complaint.assert_called_once_with(
        complaint_id = "CMP-001",
        resolution = "Reverse the disputed fee.",
        communication_date = agent.tools.close_complaint.call_args.kwargs[
            "communication_date"
        ], evidence_refs = []
    )

    agent.tools.record_approval_decision.assert_not_called()

    assert result["final_status"] == "Closed"


# --------------------------------------------------
# Approval routing tests
# --------------------------------------------------

def test_approval_router_requires_review(agent):
    state = {
        "proposed_action": {
            "approval_required": True
        }
    }

    assert agent.approval_router(state) == "request_review"


def test_approval_router_does_not_require_review(agent):
    state = {
        "proposed_action": {
            "approval_required": False
        }
    }

    assert agent.approval_router(state) == "finalize_case"


def test_supervisor_router_approved(agent):
    state = {
        "approval_status": "approved"
    }

    assert agent.supervisor_router(state) == "finalize_case"


def test_supervisor_router_rejected(agent):
    state = {
        "approval_status": "rejected"
    }

    assert agent.supervisor_router(state) == "rejected"


def test_supervisor_router_changes_requested(agent):
    state = {
        "approval_status": "changes_requested"
    }

    assert agent.supervisor_router(state) == "rework"


# --------------------------------------------------
# Investigation entry-point test
# --------------------------------------------------

def test_investigate(agent):
    expected_result = {
        "complaint_id": "CMP-001",
        "final_status": "Closed"
    }

    agent.graph = Mock()
    agent.graph.invoke.return_value = expected_result

    result = agent.investigate("CMP-001")

    agent.graph.invoke.assert_called_once_with({
        "complaint_id": "CMP-001"
    })

    assert result == expected_result


def test_record_supervisor_decision(agent):
    state = {
        "approval_request_id": "APR-001",
        "approval_status": "changes_requested",
        "supervisor_feedback": "Provide additional transaction evidence."
    }

    result = agent.record_supervisor_decision(state)

    agent.tools.record_approval_decision.assert_called_once_with(
        approval_id = "APR-001",
        decision = "changes_requested",
        reason = "Provide additional transaction evidence."
    )

    assert result == {}

def test_record_supervisor_decision_without_feedback(agent):
    state = {
        "approval_request_id": "APR-001",
        "approval_status": "approved"
    }

    agent.record_supervisor_decision(state)

    agent.tools.record_approval_decision.assert_called_once_with(
        approval_id = "APR-001",
        decision = "approved",
        reason = "Supervisor decision: approved"
    )

def test_reword_case(agent):
    state = {
        "supervisor_feedback": "Provide additional transaction evidence.",
        "rework_count": 1
    }

    result = agent.rework_case(state)

    assert result["supervisor_feedback"] == (
        "Provide additional transaction evidence."
    )

    assert result["rework_count"] == 2

def test_rework_case_initial_count(agent):
    state = {
        "supervisor_feedback": "Clarify the policy evidence."
    }

    result = agent.rework_case(state)

    assert result["supervisor_feedback"] == (
        "Clarify the policy evidence."
    )

    assert result["rework_count"] == 1

def test_supervisor_router_invalid_decision(agent):
    state = {"approval_status": "pending"}

    with pytest.raises(ValueError, match="Unsupported supervisor decision"):
        agent.supervisor_router(state)

def test_workflow_rework_loop(agent, monkeypatch):
    import src.agent.investigation_agent as investigation_module

    # --------------------------------------------------
    # Mock complaint and operational evidence
    # --------------------------------------------------

    agent.tools.get_complaint.return_value = {
        "complaint_id": "CMP-001",
        "customer_id": "CUS-001",
        "account_id": "ACC-001",
        "details": "Customer disputes an overdraft fee."
    }

    agent.tools.get_customer.return_value = {
        "customer_id": "CUS-001",
        "name": "Test Customer"
    }

    agent.tools.get_accounts.return_value = [
        {"account_id": "ACC-001", "status": "Active"}
    ]

    agent.tools.search_policy.return_value = [
        {
            "chunk_id": "KB-002",
            "text": "Fee reversals require supervisor approval."
        }
    ]

    # --------------------------------------------------
    # Mock structured LLM responses
    # --------------------------------------------------

    llm_prompts = []

    def structured_chain(payload):
        model_result = Mock()
        model_result.model_dump.return_value = payload

        chain = Mock()

        def capture_prompt(prompt):
            llm_prompts.append(prompt)
            return model_result

        chain.invoke.side_effect = capture_prompt

        return chain

    classification = {
        "category": "Fee Dispute",
        "confidence": 0.75
    }

    initial_summary = {
        "verified_facts": [
            "Customer disputes an overdraft fee."
        ],
        "policy_evidence": [
            "Fee reversals require supervisor approval."
        ],
        "analysis": "Additional transaction evidence should be reviewed."
    }

    initial_action = {
        "action": "Review the disputed overdraft fee.",
        "rationale": "The available evidence requires further review.",
        "approval_required": True
    }

    revised_summary = {
        "verified_facts": [
            "Customer disputes an overdraft fee.",
            "Additional transaction evidence was reviewed."
        ],
        "policy_evidence": [
            "Fee reversals require supervisor approval."
        ],
        "analysis": "The revised evidence supports a fee reversal."
    }

    revised_action = {
        "action": "Reverse the disputed overdraft fee.",
        "rationale": "The revised evidence supports reversing the fee.",
        "approval_required": True
    }

    agent.llm.with_structured_output.side_effect = [
        structured_chain(classification),
        structured_chain(initial_summary),
        structured_chain(initial_action),
        structured_chain(revised_summary),
        structured_chain(revised_action)
    ]

    # --------------------------------------------------
    # Mock persistence tools
    # --------------------------------------------------

    agent.tools.create_recommendation.side_effect = [
        {"recommendation_id": "REC-001"},
        {"recommendation_id": "REC-002"}
    ]

    agent.tools.request_approval.side_effect = [
        {"approval_id": "APR-001"},
        {"approval_id": "APR-002"}
    ]

    # --------------------------------------------------
    # Simulate supervisor responses
    # --------------------------------------------------

    supervisor_responses = iter([
        {
            "decision": "changes_requested",
            "feedback": "Provide additional transaction evidence."
        },
        {
            "decision": "approved",
            "feedback": ""
        }
    ])

    interrupt_payloads = []

    def mock_interrupt(payload):
        interrupt_payloads.append(payload)
        return next(supervisor_responses)

    monkeypatch.setattr(
        investigation_module,
        "interrupt",
        mock_interrupt
    )

    # --------------------------------------------------
    # Execute the actual LangGraph workflow
    # --------------------------------------------------

    result = agent.graph.invoke({
        "complaint_id": "CMP-001"
    })

    # --------------------------------------------------
    # Verify the workflow completed
    # --------------------------------------------------

    assert result["final_status"] == "Closed"

    # One rework cycle occurred.
    assert result["rework_count"] == 1

    # --------------------------------------------------
    # Verify two recommendations were created
    # --------------------------------------------------

    assert agent.tools.create_recommendation.call_count == 2

    # --------------------------------------------------
    # Verify two supervisor requests were created
    # --------------------------------------------------

    assert agent.tools.request_approval.call_count == 2

    approval_calls = agent.tools.request_approval.call_args_list

    assert approval_calls[0].kwargs["complaint_id"] == "CMP-001"
    assert approval_calls[1].kwargs["complaint_id"] == "CMP-001"

    # --------------------------------------------------
    # Verify both supervisor decisions were recorded
    # --------------------------------------------------

    assert agent.tools.record_approval_decision.call_count == 2

    decisions = [
        call.kwargs["decision"]
        for call in agent.tools.record_approval_decision.call_args_list
    ]

    assert decisions == [
        "changes_requested",
        "approved"
    ]

    # --------------------------------------------------
    # Verify supervisor feedback reached the revised LLM prompts
    # --------------------------------------------------

    feedback = "Provide additional transaction evidence."

    assert len(llm_prompts) == 5

    assert feedback in llm_prompts[3]  # Revised summary
    assert feedback in llm_prompts[4]  # Revised action

    # --------------------------------------------------
    # Verify the workflow finalized the complaint
    # --------------------------------------------------

    agent.tools.update_complaint_status.assert_called_once()

    agent.tools.close_complaint.assert_called_once()

    # Two supervisor interruptions occurred.
    assert len(interrupt_payloads) == 2

    assert agent.trace_file.exists()

    with open(agent.trace_file, "r", encoding="utf-8") as file:
        traces = json.load(file)

    assert len(traces) > 0

    assert any(
        event["node"] == "load_complaint"
        for event in traces
    )