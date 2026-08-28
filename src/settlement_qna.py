import os
import re
import json
import pandas as pd

from dotenv import load_dotenv
from google import genai
from openai import OpenAI


# =============================
# CONFIG
# =============================

GEMINI_MODEL = "gemini-3.6-flash"
GROQ_MODEL = "openai/gpt-oss-20b"


# =============================
# API SETUP
# =============================

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found in .env")

gemini_client = genai.Client(
    api_key=gemini_key
)

groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_key,
)


# =============================
# LOAD DATA
# =============================

ledger = pd.read_csv("data/company_ledger.csv")
settlements = pd.read_csv("data/settlements.csv")
bank = pd.read_csv("data/bank_statement.csv")
invoices = pd.read_csv("data/invoices.csv")
reconciliation = pd.read_csv(
    "data/reconciliation_results.csv"
)
audit_log = pd.read_csv(
    "data/audit_log.csv"
)


# =============================
# TRANSACTION ID
# =============================

def extract_transaction_id(question):
    match = re.search(
        r"TXN\d{4}",
        question.upper()
    )

    return match.group(0) if match else None


# =============================
# COLLECT EVIDENCE
# =============================

def get_transaction_evidence(transaction_id):

    evidence = {
        "transaction_id": transaction_id,
        "ledger": ledger[
            ledger["transaction_id"].astype(str)
            == transaction_id
        ].to_dict(orient="records"),

        "settlements": settlements[
            settlements["transaction_id"].astype(str)
            == transaction_id
        ].to_dict(orient="records"),

        "bank_records": bank[
            bank["description"]
            .astype(str)
            .str.contains(
                transaction_id,
                na=False
            )
        ].to_dict(orient="records"),

        "invoice": invoices[
            invoices["transaction_id"].astype(str)
            == transaction_id
        ].to_dict(orient="records"),

        "reconciliation": reconciliation[
            reconciliation["transaction_id"].astype(str)
            == transaction_id
        ].to_dict(orient="records"),

        "ai_audit": audit_log[
            audit_log["transaction_id"].astype(str)
            == transaction_id
        ].to_dict(orient="records"),
    }

    return evidence


# =============================
# BUILD PROMPT
# =============================

def build_prompt(question, evidence):

    return f"""
You are a financial settlement Q&A assistant.

Answer the user's question using ONLY the supplied
transaction evidence.

Rules:
- Do not invent facts.
- Do not guess missing information.
- A missing record is different from a zero amount.
- Mention missing bank or settlement records explicitly.
- Mention multiple settlement records when present.
- Use the reconciliation result when explaining the
  final system decision.
- Use AI audit information only as recorded.
- Keep the answer clear and concise.

Question:
{question}

Transaction evidence:
{json.dumps(evidence, indent=2, default=str)}
"""


# =============================
# AI PROVIDERS
# =============================

def ask_gemini(prompt):

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text


def ask_groq(prompt):

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial settlement "
                    "Q&A assistant. Answer only from "
                    "the supplied evidence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_completion_tokens=1000,
        reasoning_effort="low",
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError(
            "Groq returned an empty response."
        )

    return answer


# =============================
# GEMINI → GROQ FALLBACK
# =============================

def answer_question(question, evidence):

    prompt = build_prompt(
        question,
        evidence
    )

    try:
        return ask_gemini(prompt), "GEMINI"

    except Exception as gemini_error:

        print("\nGemini unavailable.")
        print("Using Groq fallback.")

        try:
            return ask_groq(prompt), "GROQ"

        except Exception as groq_error:

            return (
                "I could not safely answer the question "
                "because both AI services were unavailable.\n\n"
                f"Gemini: {gemini_error}\n"
                f"Groq: {groq_error}",
                "NONE"
            )


# =============================
# Q&A LOOP
# =============================

print("\n==============================")
print("      SETTLEMENT Q&A")
print("==============================")

print("Ask about a transaction, for example:")
print("- Why is TXN0013 an exception?")
print("- What happened with TXN0207?")
print("- Why was TXN0040 sent for review?")
print("\nType 'exit' to quit.")


while True:

    question = input("\nQuestion: ").strip()

    if question.lower() == "exit":
        print("Goodbye.")
        break

    transaction_id = extract_transaction_id(
        question
    )

    if not transaction_id:
        print(
            "\nPlease include a transaction ID "
            "such as TXN0013."
        )
        continue

    evidence = get_transaction_evidence(
        transaction_id
    )

    if not any(
        evidence[key]
        for key in evidence
        if key != "transaction_id"
    ):
        print(
            f"\nNo records found for {transaction_id}."
        )
        continue

    print("\nInvestigating...")

    answer, provider = answer_question(
        question,
        evidence
    )

    print("\n------------------------------")
    print(f"AI Provider: {provider}")
    print("Answer:")
    print(answer)
    print("------------------------------")