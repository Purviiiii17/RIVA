RIVA — AI Finance Controller

Reconciliation & Investigation Virtual Agent

AI-assisted financial reconciliation for multi-source payment data, with deterministic checks, AI investigation, fallback recovery, human escalation, and evidence-based settlement Q&A.

🚀 What It Does

RIVA reconciles financial records across:

Company ledger

Payment settlements

Bank statement

Invoices

It uses code for deterministic financial checks and AI only for unresolved cases.

🧠 Architecture

                  500 Financial Transactions
                           │
                           ▼
              ┌─────────────────────────┐
              │   Rule-Based Engine     │
              │ Ledger • Settlement     │
              │ Bank • Invoice          │
              └────────────┬────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          MATCH       HUMAN REVIEW    AI CASES
           373             69             58
                                          │
                                          ▼
                                    ┌───────────┐
                                    │  Gemini   │
                                    │  Primary  │
                                    └─────┬─────┘
                                          │
                                   Failure / 503 / Quota
                                          │
                                          ▼
                                    ┌───────────┐
                                    │   Groq    │
                                    │  Fallback │
                                    └─────┬─────┘
                                          │
                                          ▼
                                    Final Decision
                                          │
                                          ▼
                                      Audit Log

⚙️ Key Features

Multi-source reconciliation

Combines ledger, settlement, bank, and invoice evidence at the transaction level.

Deterministic financial checks

Handles:

Exact matches

Processing fees

Refunds

Date shifts

Reference typos

Partial payments

Multiple settlements

Amount mismatches

Missing bank records

AI investigation

Only unresolved cases are sent to the AI layer.

Primary: Gemini
Fallback: Groq

Safety & reliability

Missing records are distinguished from zero-value records.

Multiple settlement records are aggregated before reconciliation.

Low-confidence AI decisions can be escalated to HUMAN_REVIEW.

Groq retries rate-limit failures.

If both AI providers fail, the case safely goes to HUMAN_REVIEW.

Every AI investigation is recorded in audit_log.csv.

Settlement Q&A

Ask transaction-specific questions such as:

Why is TXN0013 an exception?

RIVA retrieves the relevant financial evidence and explains the decision.

Transaction Inspector

Inspect a transaction directly:

python src/inspector.py TXN0013

The inspector shows the ledger, settlement, bank, invoice, reconciliation result, and AI audit trail.

📊 Results

Reconciliation

Decision

Count

Share

MATCH

373

74.6%

HUMAN_REVIEW

69

13.8%

EXCEPTION

58

11.6%

Total

500

100%

AI Investigation

Metric

Result

AI cases

58

Gemini

52

Groq fallback

6

API errors in final run

0

Correct AI decisions

58 / 58

End-to-end Evaluation

500 / 500 correct — 100.00%

This result is measured against the project's current synthetic dataset and ground-truth labels.

🔄 Failure Recovery

RIVA does not depend on a single AI provider:

Gemini
  │
  ├── success ─────────────► decision
  │
  └── failure
         │
         ▼
       Groq
         │
         ├── success ───────► decision
         │
         └── failure
                │
                ▼
           HUMAN_REVIEW

During development, Gemini quota/availability errors and Groq token-rate limits were encountered and handled through fallback, retries, and safe human escalation.

🛠️ Tech Stack

Python

Pandas

Gemini API

Groq API

Pydantic

python-dotenv

Rich

📁 Project Structure

ai-finance-controller/
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
│   ├── dashboard.py
│   ├── data_generator.py
│   ├── evaluator.py
│   ├── inspector.py
│   ├── reconciler.py
│   └── settlement_qna.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt

▶️ Setup

Install dependencies

pip install -r requirements.txt

Configure API keys

Create a local .env file:

GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

Never commit .env to Git.

▶️ Run

Generate synthetic data

python src/data_generator.py

Run reconciliation

python src/reconciler.py

Run AI investigation

python src/ai_investigator.py

Evaluate the complete pipeline

python src/evaluator.py

Launch the dashboard

python src/dashboard.py

Ask settlement questions

python src/settlement_qna.py

Inspect one transaction

python src/inspector.py TXN0013

🎯 Design Philosophy

RIVA intentionally follows a layered approach:

Deterministic Controls
        +
AI Investigation
        +
Provider Fallback
        +
Human Safety Escalation

Financial calculations and reconciliation rules remain explicit and auditable. AI is used where contextual investigation adds value.

⚠️ Disclaimer

All financial records in this project are synthetic and are intended only for demonstration and evaluation.