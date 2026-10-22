"""Run retrieval metrics against the checked-in question set."""
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rag.config import ROOT
from rag.index import load_index
from rag.retrieve import retrieve


def main():
    questions = json.loads((ROOT / "eval/test_questions.json").read_text(encoding="utf-8"))
    chunks, dense, bm25, model = load_index()
    hits, reciprocal, refusals, latencies = [], [], [], []
    details = []
    for item in questions:
        start = time.perf_counter()
        found, confidence, refused = retrieve(item["question"], chunks, dense, bm25, model)
        latency = time.perf_counter() - start
        latencies.append(latency)
        if item["answerable"]:
            rank = next((n for n, c in enumerate(found, 1) if c["source_file"] == item["expected_source_file"] and (item.get("expected_page") is None or c["page"] == item["expected_page"])), None)
            hits.append(bool(rank)); reciprocal.append(1 / rank if rank else 0)
        else:
            refusals.append(refused)
        details.append((item["id"], item["question"], found, refused, latency))
    hit = sum(hits) / len(hits) if hits else 0
    mrr = sum(reciprocal) / len(reciprocal) if reciprocal else 0
    refusal = sum(refusals) / len(refusals) if refusals else 0
    # Claim-level validity and answer correctness require manual review; not inferred here.
    report = f"""# Evaluation results

These are real retrieval-only metrics from the checked-in evaluation set. No answer-generation accuracy or citation-validity score is claimed because those require manual claim review. Expected PDF pages are currently unverified and marked null, so Hit@5/MRR below match expected source files only until page labels are checked.

| Metric | Result |
|---|---:|
| Answerable source-file Hit@5 | {hit:.1%} |
| Answerable source-file MRR | {mrr:.3f} |
| Refusal accuracy (retrieval gate) | {refusal:.1%} |
| Mean retrieval latency | {statistics.mean(latencies):.3f}s |
| Answer accuracy | Not measured (manual labels pending) |
| Citation validity | Not measured (manual spot check pending) |

## Failure analysis

No cases can be honestly labeled as real retrieval failures until the index is built from extracted PDF pages. Known evaluation blockers:

1. Expected page labels are null; verify the cited page against each source PDF, then rerun the evaluation. Root cause: PDF extraction/index build is unavailable in this environment.
2. Generation and citation validity are not measured. Root cause: no configured LLM credential and no generated answer corpus; fix by configuring Groq/Gemini and manually checking claims against source passages.
"""
    (ROOT / "eval/results.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
