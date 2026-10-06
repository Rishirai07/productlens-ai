# Product Requirements Document: ProductLens AI

| Field | Detail |
| --- | --- |
| Product | ProductLens AI |
| Document owner | Your name |
| Status | Draft, version 0.2 |
| Last updated | 7 October 2026 |
| Stakeholders | Product (owner), engineering (owner), pilot users |

## 1. Summary

ProductLens AI is a research assistant for product teams. A product manager uploads customer feedback, asks questions in plain English, and gets answers that cite the exact reviews behind every claim. The assistant can also turn a validated finding into a product opportunity and give it a consistent priority score.

The first version focuses on one data source (Google Play reviews for a single consumer app) and one user type (a product manager or product analyst). The aim is to prove that grounded AI answers can cut the time spent on feedback synthesis while staying accurate enough to trust in a team review.

## 2. Problem statement

Product teams collect hundreds or thousands of reviews, support tickets and survey comments every month. Turning that text into decisions is slow and inconsistent today.

* **It takes too long.** A PM reading feedback by hand covers a small sample and spends hours doing it.
* **Findings are hard to defend.** Summaries written from memory rarely link back to the original feedback, so stakeholders question them.
* **Results vary by person.** Two people reading the same reviews often reach different conclusions about what matters most.
* **Generic chatbots are not safe to rely on.** Pasting reviews into a general AI tool gives fluent answers with no citations, and those answers can include problems that customers never mentioned.

Evidence from the pilot dataset (to be added after Stage 2): two or three real reviews that show the problem, and the volume of feedback a PM would need to read each week.

## 3. Goals and non goals

**Goals for version 1**

1. Let a PM ask a question about customer feedback and receive a cited answer in under 6 seconds.
2. Make every important claim traceable to specific feedback IDs.
3. Refuse to answer, clearly and helpfully, when the data does not contain enough evidence.
4. Produce a transparent priority score for an opportunity using a fixed formula.
5. Measure quality, speed and cost with a repeatable evaluation set.

**Non goals for version 1**

* Changing roadmaps, creating tickets or launching features automatically.
* Multi agent workflows or autonomous planning.
* User accounts, login, permissions or multiple workspaces.
* Languages other than English.
* Live connections to support tools such as Zendesk or Intercom.

## 4. Target users

**Primary persona: Priya, product manager at a consumer app**

Priya owns the checkout and payments area of a food delivery app. Every week she prepares a short update on what customers are complaining about. She reads app store reviews in a spreadsheet, tags them by hand and pulls quotes into slides. She wants to spend less time sorting and more time deciding, but she will not present anything to her director that she cannot back up with real customer words.

**Secondary persona: Arjun, product analyst**

Arjun supports three PMs and gets frequent ad hoc requests such as "are people still unhappy about refunds?" He needs quick, repeatable answers and wants to know how many reviews support a finding.

## 5. User stories

| ID | As a | I want to | So that | Priority |
| --- | --- | --- | --- | --- |
| US1 | PM | ask what customers say about a product area | I can understand pain points quickly | P0 |
| US2 | PM | see the reviews behind each claim | I can verify the insight and quote it | P0 |
| US3 | PM | be told when there is not enough evidence | I do not act on a made up insight | P0 |
| US4 | PM | turn a finding into an opportunity statement | I can move from insight to action | P1 |
| US5 | PM | get a priority score with visible inputs | I can compare opportunities consistently | P1 |
| US6 | Analyst | filter by rating, date or app version | I can check if a problem is new or growing | P2 |
| US7 | Any user | rate an answer as useful or not | the team can improve the system | P0 |

## 6. Core user flow

1. The user opens ProductLens and the indexed feedback dataset loads.
2. The user types a question, for example "What are the main complaints about payments?"
3. The system finds the most relevant reviews and generates an answer that cites feedback IDs.
4. The user expands the evidence panel to read the original reviews.
5. Optionally, the user asks for a priority score. The assistant proposes impact, reach, confidence and effort values, the calculator computes the score, and the trace shows each step.
6. The user rates the answer with a thumbs up or thumbs down.

## 7. Functional requirements

| ID | Requirement | Priority | Stage |
| --- | --- | --- | --- |
| F1 | Ingest feedback from CSV, with PDF as an optional input | P0 | 4 |
| F2 | Clean text, remove duplicates and very short entries, keep raw data unchanged | P0 | 2 |
| F3 | Store each feedback record with metadata: ID, date, source, rating, app version | P0 | 4 |
| F4 | Create embeddings and index records in a vector database | P0 | 4 |
| F5 | Retrieve the top K most relevant records for a question | P0 | 5 |
| F6 | Generate answers only from retrieved evidence and cite feedback IDs | P0 | 6 |
| F7 | Show the cited reviews in an expandable evidence panel | P0 | 7 |
| F8 | Decline when retrieval confidence is below a tuned threshold | P0 | 14 |
| F9 | Decline questions outside the scope of customer feedback | P0 | 14 |
| F10 | Calculate a priority score through a deterministic tool called by the model | P1 | 8 |
| F11 | Display a step by step trace of retrieval, tool calls and the final answer | P1 | 8 |
| F12 | Log every query with retrieved IDs, answer, latency and token usage | P0 | 5 |
| F13 | Capture thumbs up or down feedback per answer | P0 | 7 |
| F14 | Filter retrieval by rating, date range or app version | P2 | Later |

## 8. Non functional requirements

| Area | Requirement |
| --- | --- |
| Latency | Median response under 3 seconds, p95 under 6 seconds |
| Cost | Report cost per query; target under USD 0.005 with the shipped model |
| Privacy | Do not store reviewer names or any personal identifiers; mask phone numbers and emails found in text |
| Security | API keys live only in environment variables or platform secrets, never in the repository |
| Reliability | Clear error message if the model provider is unavailable; no blank screens |
| Transparency | Every answer shows its sources and the date of each cited review |
| Portability | Model provider can be swapped through configuration without changing app logic |

## 9. Solution approach

**Why AI.** Feedback is unstructured, high volume and written in many different ways. Keyword search misses paraphrases such as "money got stuck" versus "payment failed". Language models handle meaning, summarisation and extraction well.

**Why retrieval augmented generation (RAG).** A model on its own will produce plausible themes that are not in the data. Retrieving the actual reviews first and instructing the model to answer only from them keeps answers grounded and makes citations possible.

**Why a deterministic tool for scoring.** Models are inconsistent at arithmetic and at applying a formula the same way every time. The model proposes the inputs from evidence; Python calculates the score. This keeps the result repeatable and auditable.

**Model strategy.** Start with one mid sized model, then compare a smaller and a larger model on the evaluation set. Ship the model with the best balance of correctness, latency and cost, and record the reasoning in EXPERIMENTS.md.

**High level architecture.** Feedback CSV, then cleaning, then chunking, then embeddings stored in ChromaDB. At query time: the question is embedded, the top K records are retrieved with metadata, guardrails check scope and evidence strength, the model writes a cited answer and calls the priority tool when asked, and everything is logged for evaluation.

## 10. Data

| Item | Detail |
| --- | --- |
| Source | Public Google Play reviews for one consumer app (app to be confirmed in Stage 2) |
| Volume | 300 to 400 raw reviews, roughly 250 or more after cleaning |
| Fields | feedback_id, date, source, rating, app_version, text |
| Collection | google-play-scraper Python package, English reviews, India store |
| Privacy | Reviewer names and profile data are not stored |
| Retention | Raw file kept unchanged; cleaned file saved separately and reproducible from scripts |
| Known bias | App store reviewers skew towards strong opinions, especially negative ones; answers will note sample size |

## 11. Success metrics

**Quality metrics** (measured on the evaluation set)

| Metric | Definition | Target |
| --- | --- | --- |
| Retrieval hit rate at 5 | Share of questions where an expected source appears in the top 5 results | 85% or higher |
| Answer correctness | Share of answers graded correct by rubric | 80% or higher |
| Faithfulness | Share of answers whose claims are all supported by retrieved evidence | 90% or higher |
| Refusal accuracy | Share of unanswerable or out of scope questions correctly declined | 80% or higher |
| Tool accuracy | Share of scoring requests where the tool is called with valid inputs | 90% or higher |

**Experience metrics** (measured in user testing)

| Metric | Target |
| --- | --- |
| Useful answer rate (thumbs up share) | 70% or higher |
| Users who say citations increased trust | 4 out of 5 testers |
| p95 latency | 6 seconds or less |

**Business and operational metrics**

| Metric | Target |
| --- | --- |
| Cost per query | Measured and reported for each model |
| Estimated time saved per weekly feedback review | Measured through tester interviews |

**Guardrail metrics** (must not get worse while other metrics improve)

* False refusal rate on answerable questions stays under 10%.
* Prompt injection test pass rate stays at 100% for the tested cases.

## 12. Evaluation plan

1. Build a set of 15 to 20 hand checked questions across six categories: direct factual, cross source, numerical, unanswerable, out of scope and adversarial.
2. Record the expected answer and expected source IDs for each question.
3. Run the baseline and score every metric in section 11.
4. Use a rubric based model judge for correctness and faithfulness, and hand grade a sample to measure how often the judge agrees with a person.
5. Tag each failure (wrong chunk, missing chunk, ranking, hallucination, refusal, parsing, tool) and fix the largest group first.
6. Rerun the full set after every change and log the results in EXPERIMENTS.md.

## 13. Guardrails and responsible AI

* **Evidence threshold.** If the best match is weak, the assistant says it could not find enough evidence instead of guessing.
* **Scope check.** Questions unrelated to customer feedback are declined politely with an explanation of what the tool can do.
* **Prompt injection defence.** Review text is treated as data, never as instructions. The system prompt and keys are never revealed.
* **Human in control.** Priority scores are recommendations. The PM makes the final call, and the inputs behind every score are visible.
* **Bias awareness.** Answers mention how many reviews support a finding so users do not overreact to a handful of comments.

## 14. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Model invents themes not present in the data | Medium | High | Evidence only prompt, citations, faithfulness metric |
| Relevant reviews are not retrieved | Medium | High | Retrieval hit rate tracking, hybrid search or reranking experiment |
| Malicious text inside a review changes model behaviour | Low | High | Data and instruction separation, red team tests |
| Small or skewed sample leads to wrong priorities | Medium | Medium | Show sample size, keep human decision |
| API cost grows with usage | Low | Medium | Spend cap, smaller model where quality allows, cost per query reporting |
| Feedback goes stale | Medium | Low | Show review dates, document refresh steps |

## 15. Assumptions and dependencies

* Public Play Store reviews are available for the chosen app and can be used for a non commercial portfolio project.
* An LLM API key is available with a monthly spend cap.
* ChromaDB's built in embedding model is good enough for short English reviews; this will be checked in evaluation.
* Streamlit Community Cloud is available for free hosting.

## 16. Release plan

| Milestone | Scope | Exit criteria |
| --- | --- | --- |
| M1 Setup and data | Repository, environment, cleaned dataset | Setup check passes; cleaned CSV saved |
| M2 Baseline | Plain model answers without retrieval | Baseline failures documented |
| M3 RAG MVP | Ingestion, retrieval, cited answers, Streamlit UI | Cited answers shown in the browser |
| M4 Tool | Priority calculator with tool calling and trace | Correct score on test cases |
| M5 Evaluation | Eval set, baseline scores, failure analysis | Metrics recorded in EVALUATION.md |
| M6 Improve | One retrieval improvement, two model comparison | Before and after numbers logged |
| M7 Safety and launch | Guardrails, deployment, five user tests | Live link and tester feedback collected |

## 17. Open questions

1. Which app's reviews give the most useful mix of product areas?
2. Should product area tags come from keyword rules or from a model classification step?
3. What retrieval confidence threshold balances refusals and coverage? To be tuned on the eval set.
4. Is a single dataset enough, or should a second source be added after the MVP?

## 18. Future scope

* Hybrid keyword and vector search, and reranking.
* Clustering similar complaints into themes automatically.
* Trend view comparing pain points across months and app versions.
* Segment comparison, such as new versus returning users.
* Generating a draft PRD from a validated opportunity.
* An evaluation dashboard that tracks regressions across prompt and model changes.
