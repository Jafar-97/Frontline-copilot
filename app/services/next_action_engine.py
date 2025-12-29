def decide_next_action(
    employee_message: str,
    risk_level: str,
    guardrail_triggered: bool
) -> tuple[str, str | None]:

    msg = employee_message.lower()

    if guardrail_triggered:
        return (
            "Escalate to supervisor or security team",
            None
        )

    if any(word in msg for word in ["fraud", "scam", "unauthorized", "stolen"]):
        return (
            "Escalate to fraud team",
            "Which account and when did the suspicious activity start?"
        )

    if any(word in msg for word in ["dispute", "refund", "wrong charge"]):
        return (
            "Start dispute intake process",
            "Which transaction is the customer disputing?"
        )

    if len(msg) < 15:
        return (
            "Ask a clarifying question",
            "Can you clarify what the customer needs help with?"
        )

    return (
        "Proceed with standard support flow",
        "What product is this related to?"
    )
