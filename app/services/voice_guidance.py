def get_voice_guidance(employee_message: str):
    msg = employee_message.lower()

    distress_keywords = [
        "panic", "crying", "angry", "furious",
        "help me", "right now", "immediately"
    ]

    if any(word in msg for word in distress_keywords):
        return [
            "Speak slowly and calmly",
            "Acknowledge the customer's emotion",
            "Reassure them that help is available",
            "Focus on securing the account first",
            "Escalate to a supervisor if needed"
        ]

    return [
        "Keep responses short and clear",
        "Confirm details verbally",
        "Avoid making promises"
    ]
