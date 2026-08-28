import os
import random
from datetime import datetime, timedelta

import pandas as pd


# Settings
NUM_EVENTS = 500
OUTPUT_DIR = "data"
START_DATE = datetime(2026, 8, 1)

random.seed(42)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Reference data
customers = [f"C{100 + i}" for i in range(50)]

scenarios = [
    "exact_match",
    "fee_difference",
    "refund",
    "date_shift",
    "reference_typo",
    "partial_payment",
    "multiple_settlements",
    "amount_mismatch",
    "missing_bank",
]

scenario_weights = [45, 10, 8, 8, 8, 7, 5, 5, 4]

amount_options = [
    1000, 1500, 2500, 5000, 7500,
    10000, 15000, 25000, 50000, 75000
]


# Output storage
ledger_rows = []
settlement_rows = []
bank_rows = []
invoice_rows = []
ground_truth_rows = []


# Generate transactions
for i in range(1, NUM_EVENTS + 1):

    event_id = f"E{i:04d}"
    transaction_id = f"TXN{i:04d}"
    payment_id = f"PAY{i:04d}"
    settlement_id = f"SET{i:04d}"
    bank_id = f"BANK{i:04d}"
    invoice_id = f"INV{i:04d}"

    customer_id = random.choice(customers)
    transaction_date = START_DATE + timedelta(
        days=random.randint(0, 20)
    )
    amount = random.choice(amount_options)

    scenario = random.choices(
        scenarios,
        weights=scenario_weights,
        k=1
    )[0]

    # Default transaction state
    fee = 0.0
    refund = 0.0
    settlement_amount = float(amount)
    settlement_date = transaction_date + timedelta(days=1)

    expected_status = "MATCH"
    expected_reason = "Records agree."
    correct_match = transaction_id
    payment_status = "PAID"


    # Scenario-specific changes
    if scenario == "fee_difference":
        fee = round(amount * 0.02, 2)
        settlement_amount = round(amount - fee, 2)
        expected_reason = (
            "Settlement difference is explained by processing fee."
        )

    elif scenario == "refund":
        refund = round(amount * 0.10, 2)
        settlement_amount = round(amount - refund, 2)
        expected_reason = (
            "Settlement difference is explained by refund."
        )

    elif scenario == "date_shift":
        settlement_date = transaction_date + timedelta(days=3)
        expected_reason = (
            "Settlement occurred within the allowed date window."
        )

    elif scenario == "reference_typo":
        expected_reason = (
            "Reference contains a minor formatting difference."
        )

    elif scenario == "partial_payment":
        settlement_amount = round(amount * 0.60, 2)
        payment_status = "PARTIAL"
        expected_status = "HUMAN_REVIEW"
        expected_reason = (
            "Payment covers only part of the invoice."
        )

    elif scenario == "multiple_settlements":
        expected_status = "HUMAN_REVIEW"
        expected_reason = (
            "One payment is represented by multiple settlement records."
        )

    elif scenario == "amount_mismatch":
        difference = random.choice([500, 1000, 2000])
        settlement_amount = max(0, amount - difference)
        expected_status = "EXCEPTION"
        correct_match = "NONE"
        expected_reason = (
            "Amount difference cannot be explained by known adjustments."
        )

    elif scenario == "missing_bank":
        expected_status = "EXCEPTION"
        correct_match = "NONE"
        expected_reason = (
            "Corresponding bank record is missing."
        )


    # Ledger
    ledger_rows.append({
        "event_id": event_id,
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_date": transaction_date.date(),
        "description": f"Customer payment for Order {i:04d}",
        "amount": amount,
        "transaction_type": "SALE",
        "status": "RECORDED",
    })


    # Settlement reference
    settlement_reference = f"RZP-{transaction_id}"

    if scenario == "reference_typo":
        settlement_reference = (
            f"RZP-{transaction_id[:-1]}X"
        )


    # Settlements
    if scenario == "multiple_settlements":

        first_part = round(amount * 0.60, 2)
        second_part = round(amount - first_part, 2)

        settlement_rows.extend([
            {
                "payment_id": payment_id,
                "settlement_id": f"{settlement_id}_1",
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "payment_date": transaction_date.date(),
                "gross_amount": first_part,
                "fee": 0.0,
                "refund_amount": 0.0,
                "net_settlement": first_part,
                "settlement_date": settlement_date.date(),
                "settlement_status": "SETTLED",
                "reference": f"{settlement_reference}-1",
            },
            {
                "payment_id": payment_id,
                "settlement_id": f"{settlement_id}_2",
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "payment_date": transaction_date.date(),
                "gross_amount": second_part,
                "fee": 0.0,
                "refund_amount": 0.0,
                "net_settlement": second_part,
                "settlement_date": settlement_date.date(),
                "settlement_status": "SETTLED",
                "reference": f"{settlement_reference}-2",
            },
        ])

    else:

        settlement_rows.append({
            "payment_id": payment_id,
            "settlement_id": settlement_id,
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "payment_date": transaction_date.date(),
            "gross_amount": amount,
            "fee": fee,
            "refund_amount": refund,
            "net_settlement": settlement_amount,
            "settlement_date": settlement_date.date(),
            "settlement_status": "SETTLED",
            "reference": settlement_reference,
        })


    # Bank
    if scenario != "missing_bank":

        if scenario == "multiple_settlements":

            bank_rows.extend([
                {
                    "bank_transaction_id": f"{bank_id}_1",
                    "reference": f"{settlement_reference}-1",
                    "transaction_date": settlement_date.date(),
                    "description": (
                        f"Payment settlement {transaction_id} - Part 1"
                    ),
                    "credit": first_part,
                    "debit": 0,
                    "balance": random.randint(100000, 500000),
                },
                {
                    "bank_transaction_id": f"{bank_id}_2",
                    "reference": f"{settlement_reference}-2",
                    "transaction_date": settlement_date.date(),
                    "description": (
                        f"Payment settlement {transaction_id} - Part 2"
                    ),
                    "credit": second_part,
                    "debit": 0,
                    "balance": random.randint(100000, 500000),
                },
            ])

        else:

            bank_rows.append({
                "bank_transaction_id": bank_id,
                "reference": settlement_reference,
                "transaction_date": settlement_date.date(),
                "description": f"Payment settlement {transaction_id}",
                "credit": settlement_amount,
                "debit": 0,
                "balance": random.randint(100000, 500000),
            })


    # Invoice
    invoice_rows.append({
        "invoice_id": invoice_id,
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "invoice_date": transaction_date.date(),
        "invoice_amount": amount,
        "tax_amount": round(amount * 0.18, 2),
        "refund_amount": refund,
        "invoice_status": (
            "PAID" if payment_status == "PAID" else "PARTIAL"
        ),
        "refund_date": (
            settlement_date.date() if refund > 0 else None
        ),
        "payment_status": payment_status,
    })


    # Ground truth
    ground_truth_rows.append({
        "event_id": event_id,
        "scenario": scenario,
        "correct_match": correct_match,
        "expected_status": expected_status,
        "expected_reason": expected_reason,
    })


# Save datasets
pd.DataFrame(ledger_rows).to_csv(
    f"{OUTPUT_DIR}/company_ledger.csv",
    index=False
)

pd.DataFrame(settlement_rows).to_csv(
    f"{OUTPUT_DIR}/settlements.csv",
    index=False
)

pd.DataFrame(bank_rows).to_csv(
    f"{OUTPUT_DIR}/bank_statement.csv",
    index=False
)

pd.DataFrame(invoice_rows).to_csv(
    f"{OUTPUT_DIR}/invoices.csv",
    index=False
)

pd.DataFrame(ground_truth_rows).to_csv(
    f"{OUTPUT_DIR}/ground_truth.csv",
    index=False
)


# Summary
scenario_counts = pd.Series(
    [row["scenario"] for row in ground_truth_rows]
).value_counts()

print("Data generation complete!")
print(f"Financial events created: {len(ground_truth_rows)}")

print("\nScenario distribution:")
print(scenario_counts)

print("\nFiles created inside the data/ folder:")
print("- company_ledger.csv")
print("- settlements.csv")
print("- bank_statement.csv")
print("- invoices.csv")
print("- ground_truth.csv")