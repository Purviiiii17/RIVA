AI Finance Controller

AI-assisted financial reconciliation and settlement investigation system built for the Razorpay Buildathon – AI Finance Controller track.

Overview

The system processes a synthetic batch of 500 financial transactions across multiple sources:

Company ledger

Payment settlements

Bank statement

Invoices

Ground-truth labels

It combines deterministic reconciliation with AI investigation so that strict financial checks are handled by code, while unresolved cases can be investigated by an LLM.

Architecture

                    ┌─────────────────────┐
                    │  Synthetic Dataset  │
                    │      500 records    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Rule-Based          │
                    │ Reconciliation      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
          MATCHED         HUMAN_REVIEW       AI CASES
          373                69                58
                                                │
                                                ▼
                                      ┌─────────────────┐
                                      │ Gemini (Primary)│
                                      └────────┬────────┘
                                               │
                                      API failure / unavailable
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Groq (Fallback) │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      Final AI Decision
                                               │
                                               ▼
                                      Audit Log / Output

Key Features

Multi-source reconciliation

Matches ledger, settlement, bank, and invoice information at the transaction level.

Deterministic financial rules

Handles objective checks such as:

Exact reconciliation

Processing fees

Refunds

Date shifts

Reference variations

Partial payments

Multiple settlements

Amount mismatches

Missing bank records

AI investigation

Only unresolved transactions are sent to the AI layer.

Gemini is used as the primary model, with Groq as a fallback when Gemini is unavailable or encounters an API failure.

Safety controls

The system:

Does not treat a missing record as a zero-value record.

Uses a confidence threshold for AI decisions.

Escalates uncertain results to HUMAN_REVIEW.

Falls back to a secondary AI provider when the primary provider fails.

Records AI decisions and errors in an audit log.

Settlement Q&A

A separate assistant answers transaction-specific settlement questions using the underlying financial evidence and audit trail.

Example:

Why is TXN0013 an exception?

Transaction Inspector

Inspect an individual transaction with:

python src/inspector.py TXN0013

The inspector shows ledger, settlement, bank, invoice, reconciliation, and AI-audit information.

Project Structure

AI FINANCE CONTROLLER/
│
├── data/
│   ├── ai_cases.csv
│   ├── audit_log.csv
│   ├── bank_statement.csv
│   ├── company_ledger.csv
│   ├── evaluation_results.csv
│   ├── ground_truth.csv
│   ├── invoices.csv
│   ├── reconciliation_results.csv
│   ├── settlements.csv
│   └── unmatched_cases.csv
│
├── src/
│   ├── ai_investigator.py
│   ├── data_generator.py
│   ├── evaluator.py
│   ├── inspector.py
│   ├── reconciler.py
│   └── settlement_qna.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

Setup

1. Install dependencies

pip install -r requirements.txt

2. Configure API keys

Create a .env file:

GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

Do not commit .env to Git.

Running the Project

Generate synthetic data

python src/data_generator.py

Run reconciliation

python src/reconciler.py

Run AI investigation

python src/ai_investigator.py

Evaluate the complete system

python src/evaluator.py

Ask settlement questions

python src/settlement_qna.py

Inspect one transaction

python src/inspector.py TXN0013

Current Test Results

The current synthetic dataset contains 500 transactions.

Reconciliation

MATCHED        373
HUMAN_REVIEW    69
UNMATCHED       58

The 58 unresolved transactions are sent to the AI investigation stage.

AI investigation

The latest verified run processed all 58 AI cases successfully:

Gemini       52
Groq          6
API errors    0

AI-stage decisions:

EXCEPTION    58

End-to-end evaluation

The latest verified evaluation produced:

Total transactions: 500
Correct decisions: 500
Overall accuracy: 100.00%
Unresolved decisions: 0
Incorrect decisions: 0

This accuracy is measured on the current synthetic dataset and its ground-truth labels.

Reliability and Failure Recovery

The system was designed so that AI availability is not a single point of failure:

Gemini
  │
  ├── success ─────────────► Decision
  │
  └── failure
          │
          ▼
        Groq
          │
          ├── success ─────► Decision
          │
          └── failure
                  │
                  ▼
             HUMAN_REVIEW

The project also encountered and handled API rate limits, including Gemini request quotas and Groq token-per-minute limits.

Design Philosophy

The system intentionally does not send every transaction to an LLM.

Deterministic financial logic is handled in Python because calculations, aggregation, and record existence checks should be explicit and auditable.

AI is reserved for investigation of cases that remain unresolved after deterministic checks.

This produces a finance workflow built around:

Deterministic checks
        +
AI investigation
        +
Fallback resilience
        +
Human safety escalation

Disclaimer

The datasets used by this project are synthetic and are intended for demonstration and evaluation purposes only.