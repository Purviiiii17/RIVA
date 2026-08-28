<div align="center">

# RIVA

### Reconciliation & Investigation Virtual Agent

**An AI Finance Controller for multi-source financial reconciliation**

<p>
  <a href="#-overview">Overview</a> ·
  <a href="#-architecture">Architecture</a> ·
  <a href="#-results">Results</a> ·
  <a href="#-quick-start">Quick Start</a>
</p>

</div>

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=flat-square&logo=pandas&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini-4285F4?style=flat-square&logo=google)
![Groq](https://img.shields.io/badge/Fallback-Groq-F55036?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-100%25-2EA44F?style=flat-square)

</div>

---

## ✦ Overview

Financial reconciliation means comparing records across different systems and investigating anything that does not line up.

**RIVA closes that loop.**

It combines:

- **Deterministic reconciliation** for strict financial checks
- **AI investigation** for unresolved cases
- **Provider fallback** for AI reliability
- **Human escalation** when automation is not safe
- **Settlement Q&A** for evidence-based explanations
- **Transaction inspection** for auditability

> **Use deterministic code where certainty matters. Use AI where reasoning helps.**

---

## ✦ At a Glance

<table>
<tr>
<td align="center"><b>500</b><br/>transactions</td>
<td align="center"><b>373</b><br/>matched</td>
<td align="center"><b>69</b><br/>human review</td>
<td align="center"><b>58</b><br/>AI cases</td>
<td align="center"><b>100%</b><br/>accuracy</td>
</tr>
</table>

---

## ✦ Architecture

```text
                         500 Transactions
                                │
                                ▼
                  ┌────────────────────────┐
                  │  Rule-Based Engine     │
                  │                        │
                  │ Ledger                  │
                  │ Settlements             │
                  │ Bank                    │
                  │ Invoices                │
                  └────────────┬───────────┘
                               │
               ┌───────────────┼───────────────┐
               │               │               │
               ▼               ▼               ▼
            MATCH         HUMAN REVIEW      AI CASES
             373               69               58
                                                 │
                                                 ▼
                                          ┌────────────┐
                                          │   Gemini   │
                                          │  Primary   │
                                          └─────┬──────┘
                                                │
                                         API failure
                                                │
                                                ▼
                                          ┌────────────┐
                                          │    Groq    │
                                          │  Fallback  │
                                          └─────┬──────┘
                                                │
                                                ▼
                                          Final Decision
                                                │
                                                ▼
                                           Audit Log
                                                │
                                                ▼
                                            Evaluation
```

### Why this architecture?

Financial calculations and record matching stay **deterministic and auditable**.

Only unresolved cases reach an LLM, reducing unnecessary AI usage and keeping the final decision path understandable.

---

## ✦ What RIVA Does

### Multi-source reconciliation

RIVA brings together:

`Ledger ↔ Settlement ↔ Bank ↔ Invoice`

It handles:

`Exact match` · `Fees` · `Refunds` · `Date shifts` · `Reference typos` · `Partial payments` · `Multiple settlements` · `Amount mismatches` · `Missing bank records`

### AI investigation

Only unresolved transactions are passed to the AI layer.

**Primary:** Gemini  
**Fallback:** Groq

Each AI response is validated before it becomes a final decision.

### Safety controls

RIVA includes:

- Missing-record detection
- Multiple-settlement aggregation
- Confidence thresholding
- Rate-limit retries
- Provider fallback
- `HUMAN_REVIEW` safety escalation
- Full AI audit logging

### Settlement Q&A

Ask:

```text
Why is TXN0013 an exception?
```

RIVA retrieves the underlying transaction evidence and explains the decision.

### Transaction Inspector

Run:

```bash
python src/inspector.py TXN0013
```

See the complete transaction trail in one place:

`Ledger → Settlement → Bank → Invoice → Rules → AI → Final Decision`

---

## ✦ Results

### Reconciliation

| Decision | Count | Share |
|:--|--:|--:|
| ✅ MATCH | **373** | 74.6% |
| 👤 HUMAN_REVIEW | **69** | 13.8% |
| 🚨 EXCEPTION | **58** | 11.6% |
| **Total** | **500** | **100%** |

### AI layer

| Metric | Result |
|:--|--:|
| AI cases | **58** |
| Gemini | **52** |
| Groq fallback | **6** |
| API errors in final run | **0** |
| Correct AI decisions | **58 / 58** |

### End-to-end evaluation

<div align="center">

# 100.00%

**500 / 500 decisions correct**

`0 unresolved` · `0 incorrect`

</div>

> Measured on the current synthetic dataset and its ground-truth labels.

---

## ✦ Failure Recovery

RIVA was built to avoid a single-provider failure becoming a system failure.

```text
Gemini
  │
  ├── Success ───────────────► Decision
  │
  └── Failure
          │
          ▼
        Groq
          │
          ├── Success ───────► Decision
          │
          └── Failure
                  │
                  ▼
             HUMAN_REVIEW
```

During development, Gemini quota/availability issues and Groq token-rate limits were encountered. The final implementation handles them with fallback logic, retries, and safe escalation.

---

## ✦ Example

### TXN0013

```text
Ledger          ₹7,500
Settlement      ₹7,500
Bank            MISSING
Invoice         ₹7,500

Rule result     UNMATCHED
AI decision     EXCEPTION
Confidence      100%
Final result    EXCEPTION
```

This is important because **a missing bank record is not treated as a legitimate zero-value bank transaction**.

---

## ✦ Quick Start

<details>
<summary><b>Install</b></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Configure API keys</b></summary>

Create `.env` locally:

```env
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
```

**Never commit `.env` to Git.**

</details>

<details>
<summary><b>Generate synthetic data</b></summary>

```bash
python src/data_generator.py
```

</details>

<details>
<summary><b>Run reconciliation</b></summary>

```bash
python src/reconciler.py
```

</details>

<details>
<summary><b>Run AI investigation</b></summary>

```bash
python src/ai_investigator.py
```

</details>

<details>
<summary><b>Evaluate the complete system</b></summary>

```bash
python src/evaluator.py
```

</details>

<details>
<summary><b>Launch dashboard</b></summary>

```bash
python src/dashboard.py
```

</details>

<details>
<summary><b>Use Settlement Q&A</b></summary>

```bash
python src/settlement_qna.py
```

</details>

<details>
<summary><b>Inspect a transaction</b></summary>

```bash
python src/inspector.py TXN0013
```

</details>

---

## ✦ Project Structure

```text
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
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ✦ Tech Stack

**Python** · **Pandas** · **Gemini API** · **Groq API** · **Pydantic** · **python-dotenv** · **Rich**

---

## ✦ Design Principle

```text
Deterministic Controls
        +
AI Investigation
        +
Provider Fallback
        +
Human Safety Escalation
```

RIVA intentionally does **not** send every transaction to an LLM.

Strict financial calculations remain explicit and reproducible. AI is reserved for unresolved cases where contextual investigation adds value.

---

## ✦ Built For

**Razorpay Buildathon — AI Finance Controller**

All records used by this project are **synthetic** and are intended only for demonstration and evaluation.
