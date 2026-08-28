import pandas as pd


# Load data
ledger = pd.read_csv("data/company_ledger.csv")
settlements = pd.read_csv("data/settlements.csv")
bank = pd.read_csv("data/bank_statement.csv")
invoices = pd.read_csv("data/invoices.csv")


# Aggregate settlements by transaction
settlement_summary = (
    settlements
    .groupby("transaction_id", as_index=False)
    .agg(
        settlement_count=("settlement_id", "count"),
        gross_amount=("gross_amount", "sum"),
        fee=("fee", "sum"),
        refund_amount=("refund_amount", "sum"),
        net_settlement=("net_settlement", "sum"),
        settlement_date=("settlement_date", "max"),
        settlement_status=("settlement_status", "first"),
        reference=("reference", "first"),
    )
)


# Aggregate bank records by transaction
bank = bank.copy()

bank["transaction_id"] = bank["description"].str.extract(
    r"(TXN\d+)"
)

bank_summary = (
    bank
    .dropna(subset=["transaction_id"])
    .groupby("transaction_id", as_index=False)
    .agg(
        bank_transaction_count=("bank_transaction_id", "count"),
        credit=("credit", "sum"),
    )
)


# Add invoice information
invoice_summary = (
    invoices[
        [
            "transaction_id",
            "invoice_amount",
            "refund_amount",
            "payment_status",
        ]
    ]
    .drop_duplicates("transaction_id")
)


# Combine all sources
reconciliation = ledger.merge(
    settlement_summary,
    on="transaction_id",
    how="left",
)

reconciliation = reconciliation.merge(
    bank_summary,
    on="transaction_id",
    how="left",
)

reconciliation = reconciliation.merge(
    invoice_summary,
    on="transaction_id",
    how="left",
    suffixes=("_settlement", "_invoice"),
)


# Handle missing values
reconciliation["settlement_count"] = (
    reconciliation["settlement_count"].fillna(0)
)

reconciliation["bank_transaction_count"] = (
    reconciliation["bank_transaction_count"].fillna(0)
)

reconciliation["fee"] = (
    reconciliation["fee"].fillna(0)
)

reconciliation["refund_amount_settlement"] = (
    reconciliation["refund_amount_settlement"].fillna(0)
)

reconciliation["net_settlement"] = (
    reconciliation["net_settlement"].fillna(0)
)

reconciliation["credit"] = (
    reconciliation["credit"].fillna(0)
)


# Rule-based reconciliation
reconciliation["amount_explained"] = (
    (
        reconciliation["amount"]
        - reconciliation["fee"]
        - reconciliation["refund_amount_settlement"]
    ).round(2)
    == reconciliation["net_settlement"].round(2)
)

reconciliation["bank_amount_matches"] = (
    reconciliation["credit"].round(2)
    == reconciliation["net_settlement"].round(2)
)

reconciliation["reconciliation_status"] = "UNMATCHED"

reconciliation.loc[
    reconciliation["amount_explained"]
    & reconciliation["bank_amount_matches"],
    "reconciliation_status",
] = "MATCHED"


# Known human-review cases
reconciliation.loc[
    reconciliation["payment_status"] == "PARTIAL",
    "reconciliation_status",
] = "HUMAN_REVIEW"

reconciliation.loc[
    reconciliation["settlement_count"] > 1,
    "reconciliation_status",
] = "HUMAN_REVIEW"


# Split remaining cases for AI
unmatched = reconciliation[
    reconciliation["reconciliation_status"] != "MATCHED"
].copy()

ai_cases = unmatched[
    unmatched["reconciliation_status"] != "HUMAN_REVIEW"
].copy()


# Save outputs
reconciliation.to_csv(
    "data/reconciliation_results.csv",
    index=False,
)

unmatched.to_csv(
    "data/unmatched_cases.csv",
    index=False,
)

ai_cases.to_csv(
    "data/ai_cases.csv",
    index=False,
)


# Summary
print("\nFinancial datasets loaded:")
print("Ledger:", len(ledger))
print("Settlements:", len(settlements))
print("Bank:", len(bank))
print("Invoices:", len(invoices))

print("\nRule-based reconciliation:")
print(
    reconciliation["reconciliation_status"].value_counts()
)

print(
    "\nCases requiring further investigation:",
    len(unmatched),
)

print(
    "\nKnown Human Review cases:",
    (
        reconciliation["reconciliation_status"]
        == "HUMAN_REVIEW"
    ).sum(),
)

print(
    "\nCases sent to AI:",
    len(ai_cases),
)

print(
    "\nUnmatched cases saved:",
    len(unmatched),
)