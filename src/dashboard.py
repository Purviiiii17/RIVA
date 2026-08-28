from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

console = Console()


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        console.print(
            f"[bold red]Missing file:[/bold red] {path}"
        )
        raise SystemExit(1)

    return pd.read_csv(path)


# Load current project results
evaluation = load_csv("evaluation_results.csv")
reconciliation = load_csv("reconciliation_results.csv")
audit_log = load_csv("audit_log.csv")


# =============================
# Metrics
# =============================

total = len(evaluation)

correct = int(
    evaluation["correct"].sum()
)

accuracy = (
    correct / total * 100
    if total else 0
)

decision_counts = (
    evaluation["system_decision"]
    .value_counts()
    .to_dict()
)

match_count = decision_counts.get("MATCH", 0)
human_count = decision_counts.get("HUMAN_REVIEW", 0)
exception_count = decision_counts.get("EXCEPTION", 0)

ai_cases = len(audit_log)

successful_ai = int(
    (audit_log["ai_status"] == "SUCCESS").sum()
)

api_errors = int(
    (audit_log["ai_status"] == "API_ERROR").sum()
)

provider_counts = (
    audit_log["ai_provider"]
    .value_counts()
    .to_dict()
)

gemini_count = provider_counts.get("GEMINI", 0)
groq_count = provider_counts.get("GROQ", 0)

safety_overrides = int(
    audit_log["safety_override"].sum()
)


# =============================
# Header
# =============================

console.print()
console.print(
    Panel.fit(
        Text(
            "AI FINANCE CONTROLLER",
            style="bold",
        ),
        subtitle="Reconciliation & AI Investigation Dashboard",
    )
)


# =============================
# Main summary
# =============================

summary = Table(
    title="System Summary",
    expand=False,
)

summary.add_column("Category")
summary.add_column("Count", justify="right")
summary.add_column("Percentage", justify="right")

def pct(value):
    return f"{value / total * 100:.1f}%" if total else "0.0%"

summary.add_row(
    "Total Transactions",
    str(total),
    "100.0%",
)

summary.add_row(
    "Matched",
    str(match_count),
    pct(match_count),
)

summary.add_row(
    "Human Review",
    str(human_count),
    pct(human_count),
)

summary.add_row(
    "Exceptions",
    str(exception_count),
    pct(exception_count),
)

console.print(summary)


# =============================
# AI summary
# =============================

ai_table = Table(
    title="AI Investigation",
    expand=False,
)

ai_table.add_column("Metric")
ai_table.add_column("Value", justify="right")

ai_table.add_row(
    "Cases Investigated",
    str(ai_cases),
)

ai_table.add_row(
    "Successful AI Cases",
    str(successful_ai),
)

ai_table.add_row(
    "Gemini",
    str(gemini_count),
)

ai_table.add_row(
    "Groq Fallback",
    str(groq_count),
)

ai_table.add_row(
    "API Errors",
    str(api_errors),
)

ai_table.add_row(
    "Safety Overrides",
    str(safety_overrides),
)

console.print(ai_table)


# =============================
# Accuracy
# =============================

accuracy_panel = Panel(
    Text(
        f"{accuracy:.2f}%\n"
        f"{correct}/{total} decisions correct",
        justify="center",
        style="bold",
    ),
    title="Overall Accuracy",
)

console.print(accuracy_panel)


# =============================
# Final status
# =============================

status = (
    "[bold green]SYSTEM VERIFIED[/bold green]"
    if accuracy == 100 and api_errors == 0
    else "[bold yellow]REVIEW RESULTS[/bold yellow]"
)

console.print(
    Panel(
        status,
        subtitle="Latest evaluated dataset",
    )
)

console.print()
