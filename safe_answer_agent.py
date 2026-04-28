import subprocess
import json


# -------------------------
# 1. AGENT POLICY (PROMPT)
# -------------------------
AGENT_PROMPT = """
You are an AI agent operating under strict execution rules.

ROLE:
You are a safe answering agent that only provides answers when confident and reliable.

INPUT:
You will receive:
- question: user query
- max_steps: maximum reasoning steps allowed

RULES:
- Do not invent information.
- If the input is insufficient, return FAIL.
- If confidence is below 0.5, return FAIL.
- Think step-by-step internally before answering.
- Do not skip validation of your answer.

TERMINATION:
If you cannot produce a reliable answer, return FAIL and stop.

OUTPUT CONTRACT:
Return ONLY valid JSON:
{
  "status": "SUCCESS | FAIL",
  "answer": "string or null",
  "confidence": number between 0 and 1
}
Do not include any extra text.
"""


# -------------------------
# 2. LLM CALL (OLLAMA)
# -------------------------
def call_llm(prompt, user_input):
    full_prompt = f"""
{prompt}

User Input:
{user_input}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3", "--", full_prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout.strip()


# -------------------------
# 3. AGENT RUNNER
# -------------------------
def run_agent(question, max_steps):

    # INPUT CONTRACT
    user_input = {
        "question": question,
        "max_steps": max_steps
    }

    # CALL LLM
    raw_output = call_llm(AGENT_PROMPT, json.dumps(user_input))

    print("\nRAW OUTPUT:\n", raw_output)

    # -------------------------
    # 4. PARSE OUTPUT (DEFENSIVE)
    # -------------------------
    try:
        parsed = json.loads(raw_output)

    except json.JSONDecodeError:
        start = raw_output.find("{")
        end = raw_output.rfind("}")

        if start != -1 and end != -1:
            json_part = raw_output[start:end+1]
            try:
                parsed = json.loads(json_part)
            except:
                return {
                    "status": "FAIL",
                    "answer": None,
                    "confidence": 0.0
                }
        else:
            return {
                "status": "FAIL",
                "answer": None,
                "confidence": 0.0
            }

    # -------------------------
    # 5. VALIDATIONS (SYSTEM CONTROL)
    # -------------------------

    # Status validation
    if parsed.get("status") not in ["SUCCESS", "FAIL"]:
        return {
            "status": "FAIL",
            "answer": None,
            "confidence": 0.0
        }

    # Confidence validation
    confidence = parsed.get("confidence", 0)

    if not isinstance(confidence, (int, float)):
        return {
            "status": "FAIL",
            "answer": None,
            "confidence": 0.0
        }

    if confidence < 0.5:
        return {
            "status": "FAIL",
            "answer": None,
            "confidence": confidence
        }

    return parsed


# -------------------------
# 6. TEST
# -------------------------
if __name__ == "__main__":

    print("\n--- TEST 1 (VALID QUESTION) ---")
    result1 = run_agent(
        question="What is the capital of France?",
        max_steps=5
    )
    print("\nAGENT RESULT:", result1)

    print("\n--- TEST 2 (UNSURE QUESTION) ---")
    result2 = run_agent(
        question="Tell me a secret unknown fact about aliens on Mars",
        max_steps=5
    )
    print("\nAGENT RESULT:", result2)