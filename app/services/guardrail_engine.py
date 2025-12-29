class GuardrailEngine:
    def check(self, message: str) -> bool:
        msg = message.lower()

        unsafe_phrases = [
            "bypass verification",
            "skip verification",
            "no id required",
            "reset password without",
            "give pin",
            "share otp",
            "share password"
        ]

        for phrase in unsafe_phrases:
            if phrase in msg:
                return True

        return False
