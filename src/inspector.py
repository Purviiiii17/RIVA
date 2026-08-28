import sys
import pandas as pd


if len(sys.argv) != 2:
    print("Usage: python src/inspector.py TXN0013")
    sys.exit(1)

transaction_id = sys.argv[1].upper()


# Load data
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


# Find transaction records
ledger_row = ledger[
    ledger["transaction_id"] == transaction_id
]

settlement_rows = settlements[
    settlements["transaction_id"] == transaction_id
]

invoice_row = invoices[
    invoices["transaction_id"] == transaction_id
]

reconciliation_row = reconciliation[
    reconciliation["transaction_id"] == transaction_id
]

bank_rows = bank[
    bank["description"]
    .astype(str)
    .str.contains(transaction_id, na=False)
]

audit_rows = audit_log[
    audit_log["transaction_id"] == transaction_id
]


# Validate transaction
if ledger_row.empty:
    print(f"Transaction {transaction_id} not found.")
    sys.exit(1)


print("\n" + "=" * 60)
print(f"TRANSACTION INSPECTOR: {transaction_id}")
print("=" * 60)


# Ledger
row = ledger_row.iloc[0]

print("\n[1] LEDGER")
print(f"Amount: ₹{row['amount']:,.2f}")
print(f"Date: {row['transaction_date']}")
print(f"Customer: {row['customer_id']}")


# Settlement
print("\n[2] SETTLEMENT")

if settlement_rows.empty:
    print("Settlement record: MISSING")
else:
    print(f"Records: {len(settlement_rows)}")
    print(
        f"Total settlement: "
        f"₹{settlement_rows['net_settlement'].sum():,.2f}"
    )
    print(
        f"Total fees: "
        f"₹{settlement_rows['fee'].sum():,.2f}"
    )
    print(
        f"Total refunds: "
        f"₹{settlement_rows['refund_amount'].sum():,.2f}"
    )

    if len(settlement_rows) > 1:
        print("Multiple settlement records detected.")


# Bank
print("\n[3] BANK")

if bank_rows.empty:
    print("Bank record: MISSING")
else:
    print(f"Bank records: {len(bank_rows)}")
    print(
        f"Total bank credit: "
        f"₹{bank_rows['credit'].sum():,.2f}"
    )


# Invoice
print("\n[4] INVOICE")

if invoice_row.empty:
    print("Invoice record: MISSING")
else:
    row = invoice_row.iloc[0]

    print(
        f"Invoice amount: "
        f"₹{row['invoice_amount']:,.2f}"
    )
    print(
        f"Payment status: "
        f"{row['payment_status']}"
    )
    print(
        f"Refund: "
        f"₹{row['refund_amount']:,.2f}"
    )


# Reconciliation
print("\n[5] RULE-BASED RECONCILIATION")

if reconciliation_row.empty:
    print("No reconciliation record.")
else:
    row = reconciliation_row.iloc[0]

    print(
        f"Status: "
        f"{row['reconciliation_status']}"
    )

    if "settlement_count" in row:
        print(
            f"Settlement count: "
            f"{int(row['settlement_count'])}"
        )

    if "bank_transaction_count" in row:
        print(
            f"Bank transaction count: "
            f"{int(row['bank_transaction_count'])}"
        )


# AI audit
print("\n[6] AI INVESTIGATION")

if audit_rows.empty:
    print("No AI investigation recorded.")
else:
    row = audit_rows.iloc[-1]

    print(
        f"Provider: "
        f"{row.get('ai_provider', 'N/A')}"
    )
    print(
        f"AI decision: "
        f"{row.get('ai_decision', 'N/A')}"
    )
    print(
        f"Confidence: "
        f"{row.get('confidence_score', 'N/A')}"
    )
    print(
        f"Safety override: "
        f"{row.get('safety_override', 'N/A')}"
    )
    print(
        f"Final decision: "
        f"{row.get('final_decision', 'N/A')}"
    )
    print(
        f"Reason: "
        f"{row.get('reason', 'N/A')}"
    )


# Summary
print("\n" + "=" * 60)
print("AUDIT SUMMARY")
print("=" * 60)

print(f"Transaction: {transaction_id}")

if not reconciliation_row.empty:
    print(
        f"Rule result: "
        f"{reconciliation_row.iloc[0]['reconciliation_status']}"
    )

if not audit_rows.empty:
    print(
        f"Final result: "
        f"{audit_rows.iloc[-1]['final_decision']}"
    )

print("=" * 60)