from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ConversationState:
    messages: List[str] = field(default_factory=list)
    escalation_count: int = 0
    confusion_count: int = 0


# Simple in-memory store (demo only)
STATE_STORE: Dict[str, ConversationState] = {}


def get_state(context_id: str) -> ConversationState:
    if context_id not in STATE_STORE:
        STATE_STORE[context_id] = ConversationState()
    return STATE_STORE[context_id]


def update_state(context_id: str, employee_message: str, escalation_required: bool) -> ConversationState:
    state = get_state(context_id)
    state.messages.append(employee_message)

    # If employee keeps sending unclear/short messages, we bump confusion
    msg = (employee_message or "").strip().lower()
    if len(msg) < 15 or any(k in msg for k in ["not sure", "unclear", "confused", "i don't know"]):
        state.confusion_count += 1

    if escalation_required:
        state.escalation_count += 1

    return state
