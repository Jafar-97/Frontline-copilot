from typing import Literal, Optional, List
from pydantic import BaseModel

class CopilotRequest(BaseModel):
    employee_message: str
    context_id: str
    channel: Literal["chat", "voice"]

class CopilotResponse(BaseModel):
    answer: str
    suggested_action: str
    risk_level: Literal["LOW", "HIGH"]
    escalation_required: bool
    guardrail_triggered: bool
    reasoning: str
    follow_up_question: Optional[str] = None
    voice_guidance: Optional[List[str]] = None

    # ✅ NEW: policy citation fields
    policy_name: Optional[str] = None
    policy_snippet: Optional[str] = None
