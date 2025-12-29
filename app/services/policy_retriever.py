from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

POLICY_DIR = Path(__file__).resolve().parents[1] / "policies"


@dataclass
class PolicyCitation:
    policy_name: str
    snippet: str


def _read_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")


def _make_snippet(text: str, max_chars: int = 220) -> str:
    cleaned = " ".join(text.strip().split())
    return cleaned[:max_chars] + ("..." if len(cleaned) > max_chars else "")


def retrieve_policy(employee_message: str, channel: str, escalation_reason: str) -> Optional[PolicyCitation]:
    msg = (employee_message or "").lower()
    reason = (escalation_reason or "").lower()

    # Simple keyword routing
    if any(k in msg for k in ["fraud", "unauthorized", "stolen", "scam", "hacked"]):
        p = POLICY_DIR / "fraud_policy.txt"
        text = _read_text(p)
        return PolicyCitation("fraud_policy.txt", _make_snippet(text))

    if any(k in msg for k in ["dispute", "refund", "wrong charge", "chargeback", "not received"]):
        p = POLICY_DIR / "dispute_policy.txt"
        text = _read_text(p)
        return PolicyCitation("dispute_policy.txt", _make_snippet(text))

    if channel == "voice" and ("distress" in reason or any(k in msg for k in ["crying", "panic", "panicking", "angry", "yelling"])):
        p = POLICY_DIR / "voice_distress_policy.txt"
        text = _read_text(p)
        return PolicyCitation("voice_distress_policy.txt", _make_snippet(text))

    return None
