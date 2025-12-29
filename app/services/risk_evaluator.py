class RiskEvaluator:
    def evaluate(self, message: str) -> str:
        msg = message.lower()

        fraud_words = [
            "unauthorized",
            "fraud",
            "scam",
            "hacked",
            "stolen",
            "chargeback"
        ]

        for word in fraud_words:
            if word in msg:
                return "HIGH"

        return "LOW"
