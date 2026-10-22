# Evaluation results

These are real retrieval-only metrics from the checked-in evaluation set. No answer-generation accuracy or citation-validity score is claimed because those require manual claim review. Expected PDF pages are currently unverified and marked null, so Hit@5/MRR below match expected source files only until page labels are checked.

| Metric | Result |
|---|---:|
| Answerable source-file Hit@5 | 75.0% |
| Answerable source-file MRR | 0.510 |
| Refusal accuracy (retrieval gate) | 0.0% |
| Mean retrieval latency | 0.016s |
| Answer accuracy | Not measured (manual labels pending) |
| Citation validity | Not measured (manual spot check pending) |

## Failure analysis

No cases can be honestly labeled as real retrieval failures until the index is built from extracted PDF pages. Known evaluation blockers:

1. Expected page labels are null; verify the cited page against each source PDF, then rerun the evaluation. Root cause: PDF extraction/index build is unavailable in this environment.
2. Generation and citation validity are not measured. Root cause: no configured LLM credential and no generated answer corpus; fix by configuring Groq/Gemini and manually checking claims against source passages.
