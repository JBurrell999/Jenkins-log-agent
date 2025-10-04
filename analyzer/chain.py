from typing import Optional
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

SYSTEM = """You are a senior CI/CD engineer.
Given raw Jenkins/GitHub Actions logs, do ALL of the following:
1) Summarize failure in 1-2 sentences.
2) List likely root cause(s) with short rationale.
3) Provide up to 5 concrete fixes (shell commands, config edits, code pointers).
4) Classify the failure: one of [dependency, compile, test, infra, config, flaky, other].
5) Output a compact JSON object with keys: summary, root_causes, fixes, classification.
Keep it crisp and actionable."""

USER_TMPL = """<log_excerpt>
{logs}
</log_excerpt>

Return sections:
- Summary
- Root causes
- Fixes (bulleted)
- Classification
- JSON (summary, root_causes, fixes, classification)
"""

def make_llm(ollama_url: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.2):
    base_url = ollama_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = model or os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
    return ChatOllama(base_url=base_url, model=model, temperature=temperature)

def build_chain(ollama_url: Optional[str] = None, model: Optional[str] = None):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        ("human", USER_TMPL),
    ])
    llm = make_llm(ollama_url=ollama_url, model=model)
    return prompt | llm | StrOutputParser()
