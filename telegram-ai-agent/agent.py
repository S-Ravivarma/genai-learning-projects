import requests

def process_message(user_message: str):

    prompt = f"""
You are an AI assistant for an ice cream shop.

Menu:
- Chocolate Cone – ₹40
- Vanilla Cup – ₹50
- Strawberry Cone – ₹45

User message: {user_message}

Reply naturally and clearly.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]