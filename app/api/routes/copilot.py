from fastapi import APIRouter

from app.models.schemas import CopilotRequest, CopilotResponse
from app.services.risk_evaluator import RiskEvaluator
from app.services.guardrail_engine import GuardrailEngine
from app.services.escalation_engine import decide_escalation
from app.services.next_action_engine import decide_next_action
from app.services.voice_guidance import get_voice_guidance

# NEW
from app.services.policy_retriever import retrieve_policy
from app.services.conversation_state import update_state

router = APIRouter()

risk_evaluator = RiskEvaluator()
guardrail_engine = GuardrailEngine()


@router.post("/respond", response_model=CopilotResponse)
def respond(payload: CopilotRequest):
    # 1) Risk + guardrail checks
    risk = risk_evaluator.evaluate(payload.employee_message)
    guardrail_triggered = guardrail_engine.check(payload.employee_message)

    # 2) Escalation decision
    escalation_required, escalation_reason = decide_escalation(
        risk_level=risk,
        guardrail_triggered=guardrail_triggered,
        channel=payload.channel,
        employee_message=payload.employee_message
    )

    # 3) Suggested next action
    suggested_action, follow_up_question = decide_next_action(
        employee_message=payload.employee_message,
        risk_level=risk,
        guardrail_triggered=guardrail_triggered
    )

    # If escalation is required, make action match escalation
    if escalation_required and not guardrail_triggered:
        suggested_action = "Escalate to a supervisor or appropriate internal team"

    # 4) Voice guidance (only for voice)
    voice_guidance = None
    if payload.channel == "voice":
        voice_guidance = get_voice_guidance(payload.employee_message)

    # 5) Update conversation state (context-aware behavior)
    state = update_state(
        context_id=payload.context_id,
        employee_message=payload.employee_message,
        escalation_required=escalation_required
    )

    # If repeated confusion (same context_id), force better follow-up
    if state.confusion_count >= 2 and not escalation_required:
        suggested_action = "Ask a clarifying question"
        follow_up_question = (
            "I’m seeing repeated confusion—what exact outcome does the customer want, "
            "and what have you already tried?"
        )

    # 6) Policy retrieval + citation
    citation = retrieve_policy(
        employee_message=payload.employee_message,
        channel=payload.channel,
        escalation_reason=escalation_reason
    )
    policy_name = citation.policy_name if citation else None
    policy_snippet = citation.snippet if citation else None

    # 7) Answer text
    if guardrail_triggered:
        answer = "This request is unsafe for AI to handle and must be escalated."
    elif escalation_required:
        answer = "This request requires escalation. Follow the recommended next steps."
    else:
        answer = "This request can be handled using standard procedures."

    # 8) Structured response
    return CopilotResponse(
        answer=answer,
        suggested_action=suggested_action,
        risk_level=risk,
        escalation_required=escalation_required,
        guardrail_triggered=guardrail_triggered,
        reasoning=escalation_reason,
        follow_up_question=follow_up_question,
        voice_guidance=voice_guidance,
        policy_name=policy_name,
        policy_snippet=policy_snippet
    )
