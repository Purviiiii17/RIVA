# RIVA — AI Finance Controller

### Reconciliation & Investigation Virtual Agent

**An AI-powered financial reconciliation and investigation system that combines deterministic controls, AI reasoning, provider fallback, and human review.**

RIVA reconciles transactions across **ledger, settlements, bank statements, and invoices**, automatically resolves deterministic cases, investigates unresolved cases using AI, and escalates uncertain cases instead of guessing.

---

## ✦ What is RIVA?

Financial reconciliation is rarely as simple as matching two numbers.

Real-world transactions can contain:

- Partial payments
- Multiple settlements
- Missing bank records
- Amount mismatches
- Refunds
- Fees
- Date differences
- Reference inconsistencies

RIVA addresses these problems through a **layered reconciliation architecture**.

Instead of sending every transaction to an AI model, RIVA first applies deterministic financial rules and only sends unresolved cases to AI.

```text
                    TRANSACTION
                         │
                         ▼
              ┌────────────────────┐
              │  DETERMINISTIC     │
              │  RECONCILIATION    │
              └─────────┬──────────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
           MATCH     REVIEW     AI CASE
                                  │
                                  ▼
                           ┌────────────┐
                           │   GEMINI   │
                           │  PRIMARY   │
                           └─────┬──────┘
                                 │
                           API FAILURE
                                 │
                                 ▼
                           ┌────────────┐
                           │    GROQ    │
                           │  FALLBACK  │
                           └─────┬──────┘
                                 │
                                 ▼
                         SAFETY VALIDATION
                                 │
                                 ▼
                          FINAL DECISION
                                 │
                                 ▼
                            AUDIT LOG

# ✦ Dashboard

RIVA includes a Streamlit-based finance operations dashboard designed to give users a clear view of reconciliation results, investigations, and exceptions.

The application is divided into five main sections:

- Overview
- Transaction Inspector
- Settlement Q&A
- Audit Trail
- Human Review

---

## 🔹 Overview

The Overview dashboard provides a high-level summary of the complete reconciliation dataset.

### Key metrics

| Metric | Result |
|---|---:|
| Total Transactions | 500 |
| Matched | 373 |
| Human Review | 69 |
| Exceptions | 58 |

### Reconciliation Health

The dashboard visually represents the distribution of transaction decisions:

```text
MATCH          373  (74.6%)
HUMAN_REVIEW    69  (13.8%)
EXCEPTION       58  (11.6%)

# ✦ Benchmark Verification

RIVA includes an evaluation pipeline to verify system decisions against predefined ground-truth results.

The evaluation is performed on a synthetic dataset containing **500 transactions**.

## Evaluation Results

| Metric | Result |
|---|---:|
| Total decisions | 500 |
| Correct decisions | 500 |
| Accuracy | 100.00% |
| Incorrect | 0 |
| Unresolved | 0 |

### Reconciliation Distribution

| Final Decision | Count | Percentage |
|---|---:|---:|
| MATCH | 373 | 74.6% |
| HUMAN_REVIEW | 69 | 13.8% |
| EXCEPTION | 58 | 11.6% |
| **TOTAL** | **500** | **100%** |

### AI Investigation Statistics

| Metric | Count |
|---|---:|
| AI cases | 58 |
| Gemini investigations | 52 |
| Groq fallback | 6 |
| API errors | 0 |
| Safety overrides | 0 |

> These results are generated from the project's synthetic evaluation dataset.

---

# ✦ Technology Stack

### Core

- **Python**
- **Pandas**
- **Streamlit**

### AI

- **Google Gemini**
- **Groq**

### Configuration

- **python-dotenv**

### Terminal / CLI

- **Rich**

### Data

- CSV-based financial datasets
- Ground-truth evaluation data
- AI audit logs

---

# ✦ Project Architecture

```text
                         ┌───────────────────┐
                         │   Streamlit UI    │
                         │      app.py       │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
      Transaction             Settlement              Audit
       Inspector                 Q&A                  Trail
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    Reconciler     │
                         │  Rule-based logic │
                         └─────────┬─────────┘
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                     Resolved              Unresolved
                        │                     │
                        ▼                     ▼
                     Decision          AI Investigator
                                              │
                                      ┌───────┴───────┐
                                      │               │
                                   Gemini           Groq
                                   Primary         Fallback
                                      │               │
                                      └───────┬───────┘
                                              │
                                              ▼
                                      Safety Validation
                                              │
                                              ▼
                                        Final Decision
                                              │
                                              ▼
                                          Audit Log