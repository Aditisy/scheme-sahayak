"""
End-to-end evaluation: retrieval -> gate -> LLM answer -> citation + number checks.
Save as eval/run_e2e.py, then run from the project root:  python eval/run_e2e.py
Writes eval/results_e2e.md
"""
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rag.generate import UNKNOWN, answer, llm_client  # noqa: E402
from rag.index import load_index  # noqa: E402
from rag.retrieve import retrieve  # noqa: E402

# Extra questions added on top of eval/test_questions.json.
# expected_source_file None = file-level hit is not scored for that question.
EXTRA = [
    {"id": "pk3", "question": "Is Aadhaar compulsory to receive PM-KISAN benefits?", "answerable": True, "expected_source_file": None},
    {"id": "pk4", "question": "How is a family defined under PM-KISAN?", "answerable": True, "expected_source_file": None},
    {"id": "jay3", "question": "What is the health cover per family per year under PM-JAY?", "answerable": True, "expected_source_file": None},
    {"id": "sc3", "question": "What is the annual parental income limit for the SC post-matric scholarship?", "answerable": True, "expected_source_file": None},
    {"id": "sc4", "question": "Are students doing correspondence or online courses eligible for the SC post-matric scholarship?", "answerable": True, "expected_source_file": None},
    {"id": "oos4", "question": "What is the PM-JAY health cover in the USA?", "answerable": False},
    {"id": "oos5", "question": "Who is the current Agriculture Minister of India?", "answerable": False},
    {"id": "oos6", "question": "What will the PM-KISAN installment amount be in 2030?", "answerable": False},
]


def numbers_in(text):
    """Numbers (2+ digits or with commas) in an answer, ignoring [n] citation markers."""
    text = re.sub(r"\[\d+\]", " ", text)
    out = set()
    for m in re.findall(r"\d[\d,]*\.?\d*", text):
        n = m.replace(",", "").rstrip(".")
        if len(n) >= 2:
            out.add(n)
    return out


def supported(nums, chunks):
    blob = " ".join(c["text"] for c in chunks).replace(",", "")
    return {n for n in nums if n in blob}


def main():
    questions = json.loads((ROOT / "eval" / "test_questions.json").read_text(encoding="utf-8-sig"))
    questions += EXTRA
    chunks, dense, bm25, model = load_index()
    client, llm_model = llm_client()
    if not client:
        print("No LLM client. Check .streamlit/secrets.toml")
        return

    rows = []
    for q in questions:
        t0 = time.time()
        found, conf, refused = retrieve(q["question"], chunks, dense, bm25, model, None)
        if refused:
            result = UNKNOWN
        else:
            try:
                result = answer(q["question"], found, client, llm_model)
            except Exception as e:  # never crash the eval
                result = UNKNOWN
                print("ERROR on", q["id"], repr(e))
        latency = time.time() - t0
        answered = isinstance(result, tuple)
        text, sources = (result if answered else (UNKNOWN, []))

        rank = None
        exp = q.get("expected_source_file")
        if q["answerable"] and exp:
            for i, c in enumerate(found, 1):
                if c["source_file"] == exp:
                    rank = i
                    break

        nums = numbers_in(text) if answered else set()
        ok_nums = supported(nums, sources) if answered else set()

        rows.append({
            "id": q["id"], "question": q["question"], "answerable": q["answerable"],
            "refused_by_gate": bool(refused), "answered": answered, "conf": float(conf),
            "rank": rank, "expected": exp, "latency": latency,
            "sources": sorted({(c["source_file"], c["page"]) for c in sources}),
            "text": text, "nums": nums, "nums_ok": ok_nums,
        })
        print(f"{q['id']:6} answered={answered!s:5} conf={conf:.2f} rank={rank}")
        time.sleep(1.5)  # be gentle with free-tier rate limits

    ans_rows = [r for r in rows if r["answerable"]]
    oos_rows = [r for r in rows if not r["answerable"]]
    scored = [r for r in ans_rows if r["expected"]]
    hit5 = sum(1 for r in scored if r["rank"]) / max(len(scored), 1)
    mrr = sum((1 / r["rank"]) for r in scored if r["rank"]) / max(len(scored), 1)
    answered_rate = sum(r["answered"] for r in ans_rows) / max(len(ans_rows), 1)
    refusal = sum(1 for r in oos_rows if not r["answered"]) / max(len(oos_rows), 1)
    with_nums = [r for r in rows if r["answered"] and r["nums"]]
    num_support = (
        sum(len(r["nums_ok"]) for r in with_nums) / max(sum(len(r["nums"]) for r in with_nums), 1)
        if with_nums else None
    )
    lat = statistics.mean(r["latency"] for r in rows)

    L = ["# End-to-end evaluation results", ""]
    L += [f"Questions: {len(rows)} ({len(ans_rows)} answerable, {len(oos_rows)} out-of-scope). LLM: `{llm_model}`.", ""]
    L += ["| Metric | Result |", "|---|---:|"]
    L += [f"| Answerable questions answered (not refused) | {answered_rate:.0%} |"]
    L += [f"| Source-file Hit@5 (questions with expected file: {len(scored)}) | {hit5:.0%} |"]
    L += [f"| Source-file MRR | {mrr:.2f} |"]
    L += [f"| Refusal accuracy on out-of-scope | {refusal:.0%} |"]
    L += [f"| Numbers in answers found in cited passages (automatic) | " + (f"{num_support:.0%}" if num_support is not None else "n/a") + " |"]
    L += [f"| Mean end-to-end latency | {lat:.1f}s |", ""]
    L += ["Answer correctness is NOT auto-scored: fill the `Correct?` column by reading each answer against the PDF page.", ""]
    L += ["| ID | Question | Answered | Gate refused | Conf | Rank | Cited sources (file p.page) | Numbers ok | Correct? |", "|---|---|---|---|---:|---:|---|---|---|"]
    for r in rows:
        src = "; ".join(f"{f} p.{p}" for f, p in r["sources"]) or "-"
        nums = f"{len(r['nums_ok'])}/{len(r['nums'])}" if r["answered"] and r["nums"] else "-"
        L.append(f"| {r['id']} | {r['question']} | {r['answered']} | {r['refused_by_gate']} | {r['conf']:.2f} | {r['rank'] or '-'} | {src} | {nums} | |")
    L += ["", "## Answers", ""]
    for r in rows:
        L += [f"**{r['id']}** {r['question']}", "", r["text"].strip(), ""]

    L += ["## Auto-flagged failure candidates (review these, then write the root cause)", ""]
    flagged = False
    for r in rows:
        if r["answerable"] and not r["answered"]:
            L.append(f"- `{r['id']}`: answerable but the system said 'I don't know'")
            flagged = True
        if (not r["answerable"]) and r["answered"]:
            L.append(f"- `{r['id']}`: out-of-scope but the system gave an answer (hallucination risk)")
            flagged = True
        if r["answered"] and r["nums"] and len(r["nums_ok"]) < len(r["nums"]):
            missing = sorted(r["nums"] - r["nums_ok"])
            L.append(f"- `{r['id']}`: numbers not found in cited passages: {missing}")
            flagged = True
        if r["answerable"] and r["expected"] and not r["rank"]:
            L.append(f"- `{r['id']}`: expected file `{r['expected']}` not in top-5")
            flagged = True
    if not flagged:
        L.append("- none flagged automatically")
    L += ["", "Known finding: the similarity gate does not separate in-scope from out-of-scope queries "
              "(MiniLM scores unrelated questions high), so refusal depends on the LLM prompt.", ""]

    out = ROOT / "eval" / "results_e2e.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\nWrote", out)


if __name__ == "__main__":
    main()