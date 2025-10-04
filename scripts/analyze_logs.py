#!/usr/bin/env python3
import argparse, os, re
from chain import build_chain

ERROR_PAT = re.compile(
    r"(Traceback|ERROR|Exception|FAIL|ModuleNotFoundError|AssertionError|Build step '.*' marked build as failure)",
    re.IGNORECASE,
)

def extract_error_windows(text: str, context: int = 60, max_chars: int = 15000) -> str:
    lines = text.splitlines()
    idxs = [i for i, line in enumerate(lines) if ERROR_PAT.search(line)]
    if not idxs:
        return "\n".join(lines[-300:])[-max_chars:]
    chunks = []
    for i in idxs[:8]:
        start = max(0, i - context)
        end = min(len(lines), i + context)
        chunks.append("\n".join(lines[start:end]))
    excerpt = "\n\n---\n\n".join(chunks)
    return excerpt[-max_chars:]

def main():
    ap = argparse.ArgumentParser(description="Analyze CI logs with LangChain + Ollama")
    ap.add_argument("--log", required=True, help="Path to build log file")
    ap.add_argument("--out", default="analysis.md", help="Write Markdown analysis here")
    ap.add_argument("--ollama-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    ap.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "gpt-oss:20b"))
    args = ap.parse_args()

    with open(args.log, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    excerpt = extract_error_windows(raw)
    chain = build_chain(ollama_url=args.ollama_url, model=args.model)
    result = chain.invoke({"logs": excerpt})

    md = f"""# CI Failure Analysis

**Model:** `{args.model}`  
**Ollama:** `{args.ollama_url}`

## Findings
{result}

---
**Input excerpt (truncated):**

"""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[+] Wrote analysis to {args.out}")

if __name__ == "__main__":
    main()
