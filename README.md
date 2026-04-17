# SMILE Gap Analyzer (The Critic Agent)

**LPI Level 3: Agent Builder Track Submission** **Author:** Aditi Mehta  
**GitHub:** [Dynamic-ctrl](https://github.com/Dynamic-ctrl)

Most agents are built to answer questions or generate templates. This agent is built to **audit assumptions**. The **SMILE Gap Analyzer** acts as an automated Senior Systems Architect. It ingests a digital twin concept, cross-references it against the official SMILE methodology and industry case studies via the LPI (Life Programmable Interface), and identifies the physical, human, and environmental blind spots that engineers often overlook.

---

##  Engineered Features (Architecture)

* **Auditor Persona:** Instead of a generic chat interface, this agent follows a strict architectural review logic. It outputs a **"Missing Reality Report"** focused on Human Factors, Edge Cases, and Environmental Variables.
* **Stateless IPC Bridge:** Replaces the fragile, persistent `stdio` stream with a resilient, stateless `subprocess.communicate()` bridge. This architecture explicitly solves the `BrokenPipeError` commonly found in MCP implementations by cleanly opening and closing the Node process for each tool call.
* **Strict XAI (Explainable AI):** Uses "Few-Shot Template Forcing" to ensure the LLM never hallucinates tool names. Every architectural critique is explicitly front-loaded with a mandatory citation (e.g., `[Tool: query_knowledge]`) so that all reasoning is traceable.
* **Security Sanitization Layer:** Implements a Regex-based sanitization bridge that scrubs user input before it reaches the MCP server or the LLM, mitigating prompt injection and special-character terminal exploits.
* **A2A Manifest:** Includes a schema-compliant `agent.json` (A2A discovery card) that defines the agent's skills, protocols, and explainability methods for machine-to-machine discovery.

---

## Technical Stack

* **Core:** Python 3.10+ (Zero-framework, `stdlib` only)
* **Protocol:** Model Context Protocol (MCP) via JSON-RPC
* **Inference:** Ollama (`qwen2.5:1.5b` or equivalent)
* **Knowledge Base:** Life Programmable Interface (LPI) Sandbox

---

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Dynamic-ctrl/lpi-smile-agent
    cd lpi-smile-agent
    ```
2.  **Verify LPI Sandbox:**
    Ensure your `lpi-developer-kit` is built:
    ```bash
    cd ../lpi-developer-kit
    npm run build
    ```
3.  **Configure Paths:**
    Update the `LPI_SERVER_PATH` inside `agent.py` to point to your local `dist/src/index.js` file.
4.  **Start Inference:**
    Ensure Ollama is running and the model is pulled:
    ```bash
    ollama serve
    ollama pull qwen2.5:1.5b
    ```

---

## Usage

Run the agent by describing a digital twin concept as a command-line argument:

```bash
python3 agent.py "I want to build a digital twin of an offshore wind farm to monitor turbine integrity.