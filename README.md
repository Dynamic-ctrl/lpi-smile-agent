# LPI SMILE Agent

A Python-based AI agent that queries the Life Programmable Interface (LPI) via the Model Context Protocol to generate implementation plans.

## Setup Instructions
1. Clone this repository.
2. Install the required packages: `pip install -r requirements.txt`
3. Ensure you have Ollama running locally with the `qwen2.5:1.5b` model.
4. Update the `LPI_SERVER_PATH` inside `agent.py` to point to your local LPI sandbox build.
5. Run the script: `python agent.py "I want to build a smart campus"`