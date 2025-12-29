from typing import Literal

RiskLevel = Literal["LOW", "HIGH"]
Channel = Literal["chat", "voice"]

VOICE_DISTRESS_KEYWORDS = [
    "panic", "panicking", "scared", "crying",
    "angry", "furious", "yelling", "shouting",
    "help me", "right now", "immediately"
]

def detect_voice_distress(message: str) -> bool:
    msg = message.lower()
    return any(keyword in msg for keyword in VOICE_DISTRESS_KEYWORDS)


def decide_escalation(
    risk_level: RiskLevel,
    guardrail_triggered: bool,
    channel: Channel,
    employee_message: str
) -> tuple[bool, str]:
    # Guardrail → always escalate
    if guardrail_triggered:
        return True, "Unsafe request detected by guardrails"

    # High risk → escalate
    if risk_level == "HIGH":
        return True, "High risk detected"

    # Voice distress → escalate earlier
    if channel == "voice" and detect_voice_distress(employee_message):
        return True, "Customer distress detected during voice interaction"

    return False, "No escalation needed"
