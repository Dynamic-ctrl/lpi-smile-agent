import sys
import json
import subprocess
import re
import requests

# Change this path to point to your dist/src/index.js file
LPI_SERVER_PATH = "/Users/MacA/Documents/internship 26/lpi/lpi-developer-kit"
OLLAMA_URL = "http://localhost:11434/api/generate"

def sanitize_input(text):
    # Security: Strip out special characters to prevent prompt injection
    clean = re.sub(r'[^\w\s\-\.\?]', '', text)
    return clean.strip()[:200]

def call_mcp_tool(tool_name, args=None):
    if args is None:
        args = {}

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }

    try:
        process = subprocess.Popen(
            ["node", LPI_SERVER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # The newline is required so the node server knows the JSON string is complete
        stdout, _ = process.communicate(input=json.dumps(request) + "\n")

        for line in stdout.split('\n'):
            if line.strip().startswith('{'):
                response = json.loads(line)
                if 'result' in response:
                    return response['result']['content'][0]['text']

        return "Error: MCP returned empty or invalid data."
    except Exception as e:
        return f"System error during tool call: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py '<describe your project>'")
        sys.exit(1)

    raw_input = sys.argv[1]
    user_query = sanitize_input(raw_input)

    if not user_query:
        print("Error: Input is empty or invalid.")
        sys.exit(1)

    print(f"[System] Starting agent for scenario: {user_query}")

    print("[System] Calling tool 1: smile_overview...")
    overview = call_mcp_tool("smile_overview")

    print("[System] Calling tool 2: get_insights...")
    insights = call_mcp_tool("get_insights", {"scenario": "smart city", "tier": "enterprise"})

    prompt = f"""
    You are an AI assistant helping plan a digital twin using the SMILE framework.
    Rule: You MUST cite your sources exactly using [Tool: smile_overview] or [Tool: get_insights] when you use the context below.

    Context 1: {overview[:800]}
    Context 2: {insights[:800]}

    User Scenario: {user_query}
    """

    print("[System] Generating response with local LLM (qwen2.5:1.5b)...")

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        })

        if res.status_code == 200:
            print("\n--- Agent Response ---")
            print(res.json().get("response", "No response text found."))
            print("----------------------\n")
        else:
            print(f"LLM Error: Status {res.status_code}")
    except requests.exceptions.RequestException:
        print("Error: Could not connect to Ollama. Make sure it is running.")

if __name__ == "__main__":
    main()