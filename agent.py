"""
Agent Builder Track — LPI Level 3 Submission (V2)
Author: Aditi Mehta
Agent: SMILE Gap Analyzer (The Critic Agent)

Description:
Unlike agents that just answer questions, this agent acts as a Senior Systems Architect. 
It ingests a user's digital twin concept, sanitizes the input to prevent prompt injection, 
queries 4 different LPI MCP tools, and audits the concept against the SMILE framework 
to generate a "Missing Reality Report" (finding the gaps in their logic).
"""

import subprocess
import json
import sys
import re

# ── CONFIG ────────────────────────────────────────────────────────
# Update this path to point exactly to where your lpi-developer-kit is located
LPI_SERVER_PATH = "../lpi-developer-kit/dist/src/index.js" 
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:1.5b" # Change this to whatever model you have pulled

# ── SECURITY LAYER ────────────────────────────────────────────────
def sanitize_input(user_input: str) -> str:
    """Regex-based sanitization to prevent prompt injection/special char breaking."""
    try:
        # Only allow alphanumeric and basic punctuation
        clean = re.sub(r'[^a-zA-Z0-9\s.,?-]', '', user_input)
        return clean.strip()
    except Exception as e:
        print(f"Sanitization Error: {e}")
        return "default secure query"

# ── STATELESS MCP BRIDGE ──────────────────────────────────────────
def call_lpi_tool(tool_name: str, arguments: dict) -> dict:
    """
    Stateless subprocess.communicate() bridge.
    Solves the BrokenPipeError found in persistent stdio streams by cleanly 
    opening, executing, and closing the Node process for every call.
    """
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }) + "\n"

    try:
        proc = subprocess.Popen(
            ["node", LPI_SERVER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=request, timeout=15)
        
        if proc.returncode != 0:
            return {"error": stderr.strip()}

        for line in stdout.strip().splitlines():
            try:
                data = json.loads(line)
                if data.get("id") == 1:
                    content = data.get("result", {}).get("content", [{}])
                    return {"result": content[0].get("text", "") if content else ""}
            except json.JSONDecodeError:
                continue
                
        return {"error": "Failed to parse LPI response."}
        
    except subprocess.TimeoutExpired:
        proc.kill()
        return {"error": "LPI tool timed out."}
    except Exception as e:
        return {"error": str(e)}

# ── ORCHESTRATION ─────────────────────────────────────────────────
def audit_architecture(raw_concept: str):
    concept = sanitize_input(raw_concept)
    print(f"\n🔍 Auditing Architecture Concept: '{concept}'\n")
    
    context_data = {}

    # Tool 1: Get Framework Baseline
    print("⏳ [1/4] Querying LPI: smile_overview...")
    try:
        res = call_lpi_tool("smile_overview", {})
        context_data["overview"] = res.get("result", "")[:500]
    except Exception as e:
        print(f"Error calling overview: {e}")

    # Tool 2: Search specific knowledge
    print("⏳ [2/4] Querying LPI: query_knowledge...")
    try:
        res = call_lpi_tool("query_knowledge", {"query": concept})
        context_data["knowledge"] = res.get("result", "")[:500]
    except Exception as e:
        print(f"Error calling knowledge: {e}")

    # Tool 3: Get Case Studies
    print("⏳ [3/4] Querying LPI: get_case_studies...")
    try:
        res = call_lpi_tool("get_case_studies", {"industry": "general"})
        context_data["cases"] = res.get("result", "")[:500]
    except Exception as e:
         print(f"Error calling case studies: {e}")

    # Tool 4: Deep Dive Reality Emulation Phase
    print("⏳ [4/4] Querying LPI: smile_phase_detail...")
    try:
        res = call_lpi_tool("smile_phase_detail", {"phase": "reality_emulation"})
        context_data["phase"] = res.get("result", "")[:500]
    except Exception as e:
         print(f"Error calling phase detail: {e}")

    # ── LLM GENERATION ──────────────────────────────────────────────
    print("\n🧠 Generating Missing Reality Report via LLM...\n")
    
    prompt = f"""
    SYSTEM: You are a strict, senior Digital Twin Systems Architect.
    TASK: Review the user concept: "{concept}" and find 3 physical/architectural blind spots.
    
    STRICT RULES:
    1. Focus on domain-appropriate Human factors (e.g., safety hazards, manual overrides, staff), Edge cases (e.g., power outages, network drops, physical accidents), and Environmental variables (e.g., dust, lighting, temperature affecting sensors).
    2. NO PREAMBLE. Just output the critiques.
    3. NO BULLET POINTS.
    4. MANDATORY CITATION: You MUST begin every single critique with exactly one of these tool citations: [Tool: smile_overview], [Tool: query_knowledge], [Tool: get_case_studies], [Tool: smile_phase_detail].

    CONTEXT DATA:
    [Tool: smile_overview]: {context_data.get('overview')}
    [Tool: query_knowledge]: {context_data.get('knowledge')}
    [Tool: get_case_studies]: {context_data.get('cases')}
    [Tool: smile_phase_detail]: {context_data.get('phase')}
    
    REQUIRED OUTPUT FORMAT (Copy this exactly for all 3 critiques):
    [Tool: your_chosen_tool] Critique 1: [Your paragraph identifying the gap].
    
    [Tool: your_chosen_tool] Critique 2: [Your paragraph identifying the gap].
    
    [Tool: your_chosen_tool] Critique 3: [Your paragraph identifying the gap].
    """
    try:
        import urllib.request
        req = urllib.request.Request(
            OLLAMA_URL, 
            data=json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read())
            print("🚨 MISSING REALITY REPORT 🚨")
            print("="*50)
            # .strip() removes any weird newlines the LLM tries to sneak in at the start
            print(result.get("response", "Error generating response.").strip()) 
            print("="*50)
    except Exception as e:
        print(f"LLM Connection Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Describe your digital twin idea"')
        sys.exit(1)
    
    try:
        audit_architecture(" ".join(sys.argv[1:]))
    except Exception as e:
        print(f"Fatal execution error: {e}")