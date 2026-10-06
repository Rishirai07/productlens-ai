# Architecture

This file is completed during Stages 4 to 8. Add a diagram image made in Excalidraw or draw.io once the pipeline works.

## Components

| Component | File | Why it exists |
| --- | --- | --- |
| Ingestion | `src/ingestion.py` | Loads and normalises feedback |
| Chunking | `src/chunking.py` | Splits long text into pieces that can be retrieved |
| Embeddings | `src/embeddings.py` | Turns text into vectors for meaning based search |
| Retrieval | `src/retrieval.py` | Finds the most relevant feedback for a question |
| RAG answerer | `src/rag.py` | Writes grounded answers with citations |
| Tools | `src/tools.py` | Calculates the priority score deterministically |
| Guardrails | `src/guardrails.py` | Checks scope, evidence strength and injection attempts |
| Evaluation | `src/evaluation.py` | Measures quality, latency and cost |

## Key decisions

Record each decision with the reason behind it. Example: chose the built in ChromaDB embedding model because it is free, runs locally and works well on short reviews.
