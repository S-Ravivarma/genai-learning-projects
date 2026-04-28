import subprocess
import json


# -------------------------
# 1. AGENT POLICY (PROMPT)
# -------------------------
AGENT_PROMPT = """
You are a controlled AI agent.

You will receive:
- task_description (string)
- max_steps (integer)

Rules:
- Reason internally step by step.
- Do not exceed max_steps.
- Do not invent information.
- If unsure, return FAIL.

Output format (STRICT JSON ONLY):
{
  "status": "SUCCESS | FAIL",
  "answer": "string or null",
  "confidence": number between 0 and 1
}
"""


# -------------------------
# 2. LLM CALL (OLLAMA SAFE)
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
def run_agent(task_description, max_steps):

    user_input = {
        "task_description": task_description,
        "max_steps": max_steps
    }

    raw_output = call_llm(AGENT_PROMPT, json.dumps(user_input))

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

    return parsed


# -------------------------
# 4. TEST EXECUTION
# -------------------------
if __name__ == "__main__":

    result = run_agent(
        task_description="Explain why uncontrolled AI agents are dangerous.",
        max_steps=5
    )

    print("\nAGENT RESULT:")
    print(result)