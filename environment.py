import random

def generate_disaster_event():
    events = [
        ("LOW", "Minor damage detected"),
        ("MEDIUM", "Buildings partially damaged"),
        ("HIGH", "Severe destruction detected")
    ]

    return random.choice(events)