import os
import json
import time

import pandas as pd
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from pydantic import BaseModel, Field


# =============================
# CONFIG
# =============================

BATCH_SIZE = 3
BATCH_DELAY = 3
GROQ_RETRIES = 3
MODEL_GEMINI = "gemini-3.6-flash"
MODEL_GROQ = "openai/gpt-oss-20b"


# =============================
# API SETUP
# =============================

gemini_client = None
groq_client = None


def _ensure_clients():
    global gemini_client, groq_client

    if gemini_client is not None and groq_client is not None:
        return

    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    if not groq_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    gemini_client = genai.Client(api_key=gemini_key)

    groq_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key,
    )


# =============================
# AI RESPONSE MODELS
# =============================

class AIReconciliationResult(BaseModel):
    transaction_id: str
    decision: str = Field(
        description="MATCH, EXCEPTION, or HUMAN_REVIEW"
    )
    confidence_score: float = Field(
        description="Confidence score from 0 to 100"
    )
    reason: str


class BatchAIResult(BaseModel):
    results: list[AIReconciliationResult]


# =============================
# LOAD CASES
# =============================

def load_ai_cases():
    ai_cases = pd.read_csv("data/ai_cases.csv")
    print("Cases available for AI:", len(ai_cases))
    return ai_cases


# =============================
# PROMPT
# =============================

def build_prompt(batch):
    records = []

    for _, case in batch.iterrows():
        settlement_count = int(
            case.get("settlement_count", 0) or 0
        )

        bank_count = int(
            case.get("bank_transaction_count", 0) or 0
        )

        records.append({
            "transaction_id": str(case["transaction_id"]),
            "ledger_amount": case["amount"],
            "settlement_record_exists": settlement_count > 0,
            "settlement_record_count": settlement_count,
            "settlement_amount": case["net_settlement"],
            "settlement_fee": case["fee"],
            "settlement_refund": case["refund_amount_settlement"],
            "bank_record_exists": bank_count > 0,
            "bank_record_count": bank_count,
            "bank_credit": case["credit"],
            "invoice_amount": case["invoice_amount"],
            "invoice_refund": case["refund_amount_invoice"],
            "payment_status": case["payment_status"],
        })

    return f"""
You are a financial reconciliation investigator.

Analyze each transaction independently using ONLY the supplied evidence.

Return exactly one result per transaction containing:
- transaction_id
- decision: MATCH, EXCEPTION, or HUMAN_REVIEW
- confidence_score: 0 to 100
- reason

Rules:

EXCEPTION:
- Missing settlement record = EXCEPTION.
- Missing bank record = EXCEPTION.
- An absent record is NOT the same as a zero amount.
- An unexplained financial discrepancy = EXCEPTION.
- Do not treat PAID as proof that the transaction reconciles.

MATCH:
- Required records must exist.
- Ledger and settlement must reconcile.
- Any difference must be fully explained by legitimate fees/refunds.
- Bank evidence must support the settlement.

HUMAN_REVIEW:
- Use when evidence is genuinely ambiguous or insufficient.

Do not invent transactions, fees, refunds, bank records, or other evidence.
Do not omit any transaction.

Transactions:
{json.dumps(records, indent=2, default=str)}
"""


# =============================
# RESULT VALIDATION
# =============================

def process_results(
    batch,
    parsed_results,
    raw_response,
    elapsed,
    provider,
):
    requested_ids = set(
        batch["transaction_id"].astype(str)
    )

    returned_ids = {
        str(result.transaction_id)
        for result in parsed_results
    }

    if (
        len(parsed_results) != len(batch)
        or returned_ids != requested_ids
    ):
        raise ValueError(
            "AI returned an incomplete or mismatched batch."
        )

    results = []

    for result in parsed_results:
        decision = result.decision.strip().upper()

        source = batch[
            batch["transaction_id"].astype(str)
            == str(result.transaction_id)
        ].iloc[0]

        settlement_count = int(
            source.get("settlement_count", 0) or 0
        )

        bank_count = int(
            source.get("bank_transaction_count", 0) or 0
        )

        # Deterministic safety rule.
        if settlement_count == 0 or bank_count == 0:
            decision = "EXCEPTION"

            missing = []

            if settlement_count == 0:
                missing.append("settlement record")

            if bank_count == 0:
                missing.append("bank record")

            result.reason = (
                "Missing "
                + " and ".join(missing)
                + "; the transaction cannot be fully reconciled."
            )

            result.confidence_score = 100

        if decision not in {
            "MATCH",
            "EXCEPTION",
            "HUMAN_REVIEW",
        }:
            raise ValueError(
                f"Invalid AI decision: {result.decision}"
            )

        safety_override = (
            result.confidence_score < 80
        )

        final_decision = (
            "HUMAN_REVIEW"
            if safety_override
            else decision
        )

        results.append({
            "transaction_id": result.transaction_id,
            "ai_status": "SUCCESS",
            "ai_decision": decision,
            "confidence_score": result.confidence_score,
            "reason": result.reason,
            "safety_override": safety_override,
            "final_decision": final_decision,
            "processing_time_seconds": round(elapsed, 3),
            "raw_ai_response": raw_response,
            "ai_provider": provider,
            "error": "",
        })

    return results


# =============================
# GEMINI
# =============================

def investigate_with_gemini(batch, prompt):
    _ensure_clients()

    start = time.perf_counter()

    response = gemini_client.models.generate_content(
        model=MODEL_GEMINI,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": BatchAIResult,
        },
    )

    elapsed = time.perf_counter() - start

    parsed = BatchAIResult.model_validate_json(
        response.text
    )

    return process_results(
        batch,
        parsed.results,
        response.text,
        elapsed,
        "GEMINI",
    )


# =============================
# GROQ
# =============================

def investigate_with_groq(batch, prompt):
    _ensure_clients()

    last_error = None

    schema = {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string"
                        },
                        "decision": {
                            "type": "string",
                            "enum": [
                                "MATCH",
                                "EXCEPTION",
                                "HUMAN_REVIEW",
                            ],
                        },
                        "confidence_score": {
                            "type": "number"
                        },
                        "reason": {
                            "type": "string"
                        },
                    },
                    "required": [
                        "transaction_id",
                        "decision",
                        "confidence_score",
                        "reason",
                    ],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["results"],
        "additionalProperties": False,
    }

    for attempt in range(1, GROQ_RETRIES + 1):
        start = time.perf_counter()

        try:
            response = groq_client.chat.completions.create(
                model=MODEL_GROQ,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial reconciliation "
                            "investigator. Return only valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_completion_tokens=1200,
                reasoning_effort="low",
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "batch_ai_result",
                        "schema": schema,
                    },
                },
            )

            elapsed = time.perf_counter() - start
            raw_text = response.choices[0].message.content

            if not raw_text:
                raise ValueError(
                    "Groq returned an empty response."
                )

            parsed = BatchAIResult.model_validate_json(
                raw_text
            )

            return process_results(
                batch,
                parsed.results,
                raw_text,
                elapsed,
                "GROQ",
            )

        except Exception as error:
            last_error = error
            error_text = str(error).lower()

            is_rate_limit = (
                "429" in error_text
                or "rate_limit" in error_text
            )

            if not is_rate_limit:
                raise

            if attempt < GROQ_RETRIES:
                wait_time = 5 * attempt

                print(
                    f"Groq rate limit. Retrying in "
                    f"{wait_time}s "
                    f"(attempt {attempt}/{GROQ_RETRIES})..."
                )

                time.sleep(wait_time)

    raise last_error


# =============================
# PROVIDER FALLBACK
# =============================

def investigate_batch(batch):
    prompt = build_prompt(batch)

    try:
        return investigate_with_gemini(batch, prompt)

    except Exception as gemini_error:
        print("Gemini failed. Using Groq fallback.")
        print("Gemini error:", str(gemini_error)[:200])

        try:
            results = investigate_with_groq(batch, prompt)

            for result in results:
                result["error"] = (
                    f"Gemini failed: {gemini_error}"
                )

            return results

        except Exception as groq_error:
            print(
                "Groq failed after retries. "
                "Sending batch to HUMAN_REVIEW."
            )

            return [
                {
                    "transaction_id": row["transaction_id"],
                    "ai_status": "API_ERROR",
                    "ai_decision": "",
                    "confidence_score": 0,
                    "reason": "",
                    "safety_override": True,
                    "final_decision": "HUMAN_REVIEW",
                    "processing_time_seconds": 0,
                    "raw_ai_response": "",
                    "ai_provider": "NONE",
                    "error": (
                        f"Gemini: {gemini_error} | "
                        f"Groq: {groq_error}"
                    ),
                }
                for _, row in batch.iterrows()
            ]


# =============================
# RUN
# =============================

def main():
    _ensure_clients()
    ai_cases = load_ai_cases()

    batches = [
        ai_cases.iloc[i:i + BATCH_SIZE]
        for i in range(0, len(ai_cases), BATCH_SIZE)
    ]

    all_results = []
    start_time = time.perf_counter()

    for batch_number, batch in enumerate(batches, start=1):
        print(
            f"\nProcessing batch "
            f"{batch_number}/{len(batches)} "
            f"({len(batch)} cases)..."
        )

        all_results.extend(
            investigate_batch(batch)
        )

        print(f"Batch {batch_number} complete.")

        if batch_number < len(batches):
            time.sleep(BATCH_DELAY)


    # =============================
    # SAVE AUDIT LOG
    # =============================

    audit_log = pd.DataFrame(all_results)

    audit_log.to_csv(
        "data/audit_log.csv",
        index=False
    )


    # =============================
    # SUMMARY
    # =============================

    total_time = time.perf_counter() - start_time

    print("\nAI investigation complete.")
    print("Cases processed:", len(audit_log))

    print("\nAI status:")
    print(audit_log["ai_status"].value_counts())

    print("\nAI provider:")
    print(audit_log["ai_provider"].value_counts())

    successful = audit_log[
        audit_log["ai_status"] == "SUCCESS"
    ]

    if not successful.empty:
        print("\nAI decisions:")
        print(successful["ai_decision"].value_counts())

        print("\nSafety overrides:")
        print(successful["safety_override"].value_counts())

    print("\nFinal decisions:")
    print(audit_log["final_decision"].value_counts())

    print(
        f"\nTotal processing time: "
        f"{total_time:.2f} seconds"
    )

    print("\nAudit log saved to:")
    print("data/audit_log.csv")


if __name__ == "__main__":
    main()