import re

# 1. Confidence-based escalation
def should_escalate_confidence(confidence: float, threshold: float = 0.5) -> bool:
    return confidence < threshold

# 2. User-requested escalation
USER_ESCALATION_PHRASES = [
    "talk to a human", "this isn't helping", "i need hr", "human please", "escalate", "real person"
]
def should_escalate_user_request(user_input: str) -> bool:
    return any(phrase in user_input.lower() for phrase in USER_ESCALATION_PHRASES)

# 3. Repeated fallback
def should_escalate_fallback(fallback_count: int, threshold: int = 2) -> bool:
    return fallback_count >= threshold

# 4. Sensitive topic detection
SENSITIVE_KEYWORDS = [
    "payroll error", "harassment", "termination", "medical leave", "discrimination", "bullying"
]
def should_escalate_sensitive_topic(user_input: str) -> bool:
    return any(keyword in user_input.lower() for keyword in SENSITIVE_KEYWORDS)

# 5. Repeated form failure
def should_escalate_form_failure(form_fail_count: int, threshold: int = 2) -> bool:
    return form_fail_count > threshold

# 6. Negative sentiment (stub, replace with real classifier)
def should_escalate_sentiment(sentiment: str) -> bool:
    return sentiment in ["frustrated", "angry", "negative"]

# 7. Loop detection
def should_escalate_loop(repeated_intent_count: int, threshold: int = 3) -> bool:
    return repeated_intent_count >= threshold

# Main escalation decision function
def should_escalate(
    confidence: float,
    user_input: str,
    fallback_count: int,
    form_fail_count: int,
    sentiment: str,
    repeated_intent_count: int
) -> bool:
    return (
        should_escalate_confidence(confidence) or
        should_escalate_user_request(user_input) or
        should_escalate_fallback(fallback_count) or
        should_escalate_sensitive_topic(user_input) or
        should_escalate_form_failure(form_fail_count) or
        should_escalate_sentiment(sentiment) or
        should_escalate_loop(repeated_intent_count)
    )

# Example escalation message
def escalation_message():
    return (
        "Let me connect you to an HR specialist for further help. "
        "You will receive a response soon."
    ) 