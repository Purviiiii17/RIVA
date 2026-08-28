import pandas as pd


# Load data
ground_truth = pd.read_csv("data/ground_truth.csv")
reconciliation = pd.read_csv("data/reconciliation_results.csv")
audit_log = pd.read_csv("data/audit_log.csv")


# Convert E0001 → TXN0001
ground_truth["transaction_id"] = (
    ground_truth["event_id"].str.replace(
        "E", "TXN", regex=False
    )
)


# Start with all transactions
results = ground_truth[
    [
        "transaction_id",
        "scenario",
        "expected_status",
    ]
].copy()


# Add rule-based decisions
rule_results = reconciliation[
    [
        "transaction_id",
        "reconciliation_status",
    ]
].rename(
    columns={
        "reconciliation_status": "rule_decision"
    }
)

results = results.merge(
    rule_results,
    on="transaction_id",
    how="left",
)


# Add AI decisions
ai_results = audit_log[
    [
        "transaction_id",
        "final_decision",
        "ai_status",
        "ai_provider",
    ]
]

results = results.merge(
    ai_results,
    on="transaction_id",
    how="left",
)


# Normalize rule-based labels
results["rule_decision"] = (
    results["rule_decision"].replace(
        {
            "MATCHED": "MATCH",
            "UNMATCHED": "EXCEPTION",
        }
    )
)


# Use AI decision for AI-investigated cases
results["system_decision"] = results["rule_decision"]

ai_mask = results["ai_status"].notna()

results.loc[ai_mask, "system_decision"] = (
    results.loc[ai_mask, "final_decision"]
)


# Evaluate
results["correct"] = (
    results["system_decision"]
    == results["expected_status"]
)

accuracy = results["correct"].mean() * 100


# Summary
print("\n===== OVERALL SYSTEM EVALUATION =====")

print("Total transactions:", len(results))
print("Correct decisions:", results["correct"].sum())
print(f"Overall accuracy: {accuracy:.2f}%")

print("\nSystem decisions:")
print(results["system_decision"].value_counts(dropna=False))

print("\nExpected decisions:")
print(results["expected_status"].value_counts())

print(
    "\nUnresolved decisions:",
    results["system_decision"].isna().sum()
)


# Incorrect cases
incorrect = results[~results["correct"]]

if incorrect.empty:
    print("\nNo incorrect decisions.")
else:
    print("\n===== INCORRECT DECISIONS =====")
    print(
        incorrect[
            [
                "transaction_id",
                "scenario",
                "expected_status",
                "rule_decision",
                "final_decision",
                "ai_status",
                "ai_provider",
            ]
        ].to_string(index=False)
    )


# Save evaluation
results.to_csv(
    "data/evaluation_results.csv",
    index=False,
)

print("\nEvaluation saved to:")
print("data/evaluation_results.csv")