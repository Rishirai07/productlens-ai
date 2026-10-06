# ProductLens AI

An AI copilot that turns customer feedback into evidence backed product insights and priority recommendations.

**Status:** in progress. The live demo, results and architecture diagram will be added as each stage is finished.

## The problem

Product managers spend hours reading reviews by hand to find recurring problems, and the summaries they produce are hard to back up. ProductLens lets them ask questions in plain English and get answers that cite the exact feedback behind every claim. The full reasoning is in [PRD.md](PRD.md).

## How it works

Feedback CSV, then cleaning, chunking and embeddings stored in ChromaDB. For each question, the most relevant reviews are retrieved and the model answers using only that evidence, with citations. A separate tool calculates priority scores, and every query is logged for evaluation.

## Results

| Metric | Baseline | Improved |
| --- | --- | --- |
| Retrieval hit rate | not measured yet | not measured yet |
| Answer correctness | not measured yet | not measured yet |
| Faithfulness | not measured yet | not measured yet |
| Refusal accuracy | not measured yet | not measured yet |
| p95 latency | not measured yet | not measured yet |
| Cost per query | not measured yet | not measured yet |

## Project documents

* [PRD.md](PRD.md): problem, users, requirements and success metrics
* [ARCHITECTURE.md](ARCHITECTURE.md): components and design decisions
* [EVALUATION.md](EVALUATION.md): evaluation method and results
* [EXPERIMENTS.md](EXPERIMENTS.md): experiment log and model comparison

## Run it locally

```bash
# Windows: setup.bat
# macOS or Linux: bash setup.sh
# Then add your API key to the .env file and run:
streamlit run app.py
```

## Tech stack

Python, ChromaDB, Streamlit, an LLM API and pandas.
