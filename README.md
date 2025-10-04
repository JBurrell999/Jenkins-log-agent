# Jenkins-log-agent
This is consulting project for Apple to track failure logs from Jenkins

# CI Log Agent (Ollama + LangChain)

This Jenkins pipeline intentionally fails, captures the console log, and sends an error-focused excerpt to a LangChain+ChatOllama agent. The agent returns a crisp summary, root causes, fixes, and a compact JSON object.

## Local quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r analyzer/requirements.txt

export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=gpt-oss:20b

python scripts/analyze_logs.py --log sample_logs/fail_build.log --out local_analysis.md
