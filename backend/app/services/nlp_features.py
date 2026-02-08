# backend/app/services/nlp_features.py

def urgency_score(text: str) -> float:
    urgent_words = [
        "immediate", "urgent", "apply fast",
        "limited slots", "joining immediately"
    ]
    text = text.lower()
    count = sum(1 for w in urgent_words if w in text)
    return count / len(urgent_words)


def emotion_score(text: str) -> float:
    emotion_words = [
        "life changing", "dream opportunity",
        "don't miss", "once in a lifetime"
    ]
    text = text.lower()
    count = sum(1 for w in emotion_words if w in text)
    return count / len(emotion_words)


def grammar_score(text: str) -> float:
    # simple rule: many ALL CAPS or !!!
    if text.count("!") > 3 or text.isupper():
        return 1.0
    return 0.0
