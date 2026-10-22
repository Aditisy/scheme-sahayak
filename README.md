# Scheme Sahayak

## Problem and user

**Named user:** a first-generation college student or rural family member in India, or the NGO / CSC volunteer helping them, who needs to know “am I eligible, how much do I get, what documents do I need?”

**Problem:** the answers sit inside long official guideline PDFs, circulars and amendments that are hard to search manually, and web summaries are often outdated or wrong.

**Why these documents:** official government PDFs for PM-KISAN, Ayushman Bharat PM-JAY and the Post-Matric Scholarship for SC students. They are authoritative, real and contain eligibility, benefit amounts and process rules.

## Documents used

The PDFs in `data/` are the nine inputs supplied with this project. Scheme URLs below point to their official source portals; the supplied files are snapshots and may be older than the current online versions.

| File | Scheme | Official source |
|---|---|---|
| `2022050996.pdf`, `2022051036.pdf`, `AMH.pdf`, `ayush.pdf` | PM-JAY | [National Health Authority PM-JAY](https://nha.gov.in/PM-JAY) |
| `gr6_dscw_sje_02092022.pdf`, `Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf` | Post-Matric Scholarship (SC) | [Scheme guidelines, Department of Social Justice and Empowerment](https://www.socialjustice.gov.in/writereaddata/UploadFile/PMS_for_SCs_Scheme_Guidelines.pdf) |
| `physicalverificationofbeneficiariesunderPM-KISAN.pdf`, `PMKisanSamanNidhi.pdf`, `RevisedPM-KISANOperationalGuidelines(English).pdf` | PM-KISAN | [PM-KISAN official portal](https://pmkisan.gov.in/) |

## Architecture

```text
PDF pages -> clean + page-local chunks -> MiniLM embeddings -> FAISS cosine index
                                       -> BM25 keyword index
Question + last 4 turns -> LLM query rewrite -> dense + BM25 -> RRF top 5
                                                      -> not-found gate
Answer + numbered context -> Groq (Gemini fallback) -> validated citations + source passages
```

## Chunking choice and why

Chunks target 800 characters with 150 characters of overlap. At this length a passage usually retains a numbered clause and enough surrounding conditions to answer a question, without making retrieval overly broad. The overlap preserves definitions and qualifications that straddle a boundary. We split on numbered clauses and paragraph boundaries where possible, and never combine separate PDF pages, so citations keep their original page number.

## Retrieval

The app combines the top 10 cosine-similarity matches from a normalized FAISS `IndexFlatIP` with the top 10 BM25 keyword matches using Reciprocal Rank Fusion, then returns five passages. An LLM rewrites follow-up questions using the four most recent conversation turns; on rewrite failure it uses the original. A configurable similarity and BM25 gate returns the exact not-found response without generation when both signals are weak. Use the sidebar to filter by scheme.

## How grounding works

The model receives only numbered retrieved passages and is instructed to cite each factual claim. Citations are checked against the supplied context; missing or invalid citations become “I don't know based on the provided documents.” The UI displays the cited file, scheme, page and passage. This is a prototype; verify all model answers against the source before relying on them.

## Evaluation results

See [`eval/results.md`](eval/results.md). Retrieval metrics are intentionally pending: the current environment could not install PyMuPDF, FAISS, or the embedding model because package-network DNS is unavailable. No page citations or metric values are fabricated. Run the commands below in a network-enabled Python 3.11 environment after installing requirements and building the index to produce real results. Manually verify expected pages and fill the answer labels before reporting evaluation as complete.

## Failure cases

No actual retrieval failures are claimed without a built index and a completed evaluation. The current build blockers are:

1. **PDF extraction and indexing unavailable here.** PyMuPDF and the other pinned libraries could not be installed. Root cause: this execution environment cannot resolve PyPI. Fix: run the build in an environment with package access, inspect skipped-page logs, then tune chunking or OCR only if a supplied PDF actually needs it.
2. **No checked answer/citation audit.** Page labels and model-claim checks remain pending. Root cause: no extracted corpus or configured Groq/Gemini secret. Fix: verify each gold page and manually inspect answer claims and citations after deployment.

These are setup limitations, not measured retrieval failures; replace this section with two observed failure cases after running the evaluation.

## Limitations

The documents are snapshots of guidelines, not legal advice. Rules can change, state implementation can differ, and scanned or poorly extracted pages may be missed. Confirm eligibility and current process with the responsible department.

## How to run locally

Use Python 3.11. Install the pinned dependencies, then build the index once:

```bash
python -m pip install -r requirements.txt
python scripts/build_index.py
streamlit run app.py
```

Set `GROQ_API_KEY` (preferred) or `GEMINI_API_KEY` in the environment or `.streamlit/secrets.toml`. Optional `LLM_MODEL` and `GEMINI_MODEL` variables select provider models. `SIM_THRESHOLD` is defined in `rag/config.py`.

## Deployment

The app is structured for Streamlit Community Cloud. Push this repository to GitHub, choose the repo and `app.py` in Streamlit Community Cloud, add `GROQ_API_KEY` under app secrets, then deploy. Prebuild `index/` and commit it before deployment so the app does not need to ingest PDFs on startup. This checkout currently has no Git remote, no built index, and no deployment secret; therefore no live demo can be reported yet.

**Live demo:** Not deployed.

## Team

GAT AIML department hack hour team (add participant names here).
