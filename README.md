# LPI SMILE Agent

A lightweight, custom Python agent built from scratch to interface with the Life Programmable Interface (LPI) via the Model Context Protocol (MCP). 

Instead of relying on heavy AI frameworks like LangChain, this agent uses standard Python libraries to establish a direct `stdio` bridge with the local Node MCP server. It routes user input through the tools, extracts the JSON data, and pipes it into a local LLM to synthesize actionable project plans.

## ✨ Key Features

* **Zero-Framework Architecture:** Built with raw Python to handle inter-process communication (IPC) and JSON-RPC protocols directly without bloatware.
* **Fully Local & Private:** Uses standard local streams for communication and a local Ollama instance (`qwen2.5:1.5b`) for inference. Zero network latency and zero cloud APIs required.
* **Explainable AI (XAI):** Engineered with a strict system prompt that turns the LLM into a "citation engine." The model is forced to explicitly tag which MCP tool (`smile_overview` or `get_insights`) provided the data, preventing black-box answers.
* **Built-in Security:** Implements a regex-based sanitization layer to scrub terminal input, preventing prompt and terminal injection attacks before the data touches the LLM.
* **A2A Discoverability:** Includes a fully configured `agent.json` manifest card to support Agent-to-Agent discovery.

## ⚙️ Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/Dynamic-ctrl/lpi-smile-agent.git](https://github.com/Dynamic-ctrl/lpi-smile-agent.git)
   cd lpi-smile-agent
   ```
2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ensure prerequisites are running:** Make sure you have Ollama running locally with the `qwen2.5:1.5b` model pulled, and the LPI sandbox built.
4. **Configure your environment:** Update the `LPI_SERVER_PATH` inside `agent.py` to point to your local LPI sandbox build directory.
5. **Run the script:**
   ```bash
   python agent.py "I want to build a smart campus"
   ```
