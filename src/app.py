import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

st.set_page_config(
    page_title="RIVA — AI Finance Controller",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    :root {
        --bg: #0A0F18;
        --surface: #111827;
        --surface-2: #162033;
        --surface-3: #1B2638;
        --border: #263449;
        --text: #F8FAFC;
        --muted: #94A3B8;
        --accent: #38BDF8;
        --success: #34D399;
        --warning: #FBBF24;
        --danger: #FB7185;
    }

    html, body {
        max-width: 100vw;
        overflow-x: hidden !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 82% 0%, rgba(56,189,248,.07), transparent 28%),
            var(--bg);
        color: var(--text);
        max-width: 100vw;
        overflow-x: hidden !important;
    }

    .block-container {
        max-width: 1280px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        margin: 0 auto !important;
    }

    body, h1, h2, h3, h4, h5, h6, p, label, input, textarea {
        font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    }

    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
    }

    [data-testid="stSidebar"] {
        background: #0D1522;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: .22em;
        color: var(--text);
    }

    .brand-sub {
        color: var(--muted);
        font-size: 12px;
        letter-spacing: .03em;
        margin-bottom: 1.25rem;
    }

    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 4px;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        border-radius: 8px;
        padding: 7px 10px;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(56,189,248,.08);
    }

    .online {
        color: var(--success);
        font-size: 11px;
        letter-spacing: .14em;
        font-weight: 700;
        padding-top: 10px;
    }

    .page-kicker {
        color: var(--accent);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .18em;
        text-transform: uppercase;
    }

    .page-title {
        font-size: 26px;
        font-weight: 750;
        color: var(--text);
        letter-spacing: -.02em;
        margin-bottom: 2px;
    }

    .page-copy {
        color: var(--muted);
        font-size: 13.5px;
        line-height: 1.45;
        max-width: 850px;
        margin-bottom: 1rem;
    }

    /* KPI Cards Layout */
    .kpi-card {
        background: linear-gradient(145deg, #131D2D, #0F1725);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,.2);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: .11em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 750;
        color: var(--text);
        line-height: 1.1;
        font-family: "Space Mono", monospace, sans-serif;
    }

    .kpi-pct {
        margin-top: 6px;
        color: var(--accent);
        font-size: 11.5px;
        font-weight: 600;
    }

    /* Standard Panel Containers */
    .panel {
        background: linear-gradient(145deg, #121C2B, #101824);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,.15);
    }

    .panel-title {
        font-size: 13px;
        font-weight: 700;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(38, 52, 73, 0.5);
    }

    .section-h {
        font-size: 14.5px;
        font-weight: 700;
        margin: 14px 0 8px;
        color: var(--text);
        letter-spacing: -.01em;
    }

    /* Inspector Card Layouts */
    .inspector-card {
        background: linear-gradient(145deg, #121C2B, #101824);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
    }

    .inspector-card-title {
        font-size: 12.5px;
        font-weight: 700;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.09em;
        padding-bottom: 6px;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(38, 52, 73, 0.6);
    }

    .detail-grid {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid rgba(38, 52, 73, 0.4);
        font-size: 12.5px;
        line-height: 1.4;
    }

    .detail-grid:last-child {
        border-bottom: none;
    }

    .detail-k {
        color: var(--muted);
        font-weight: 500;
    }

    .detail-v {
        color: var(--text);
        font-weight: 650;
        font-family: "Space Mono", monospace, sans-serif;
    }

    /* Metric Row Alignment Fix */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6.5px 0;
        border-bottom: 1px solid rgba(38, 52, 73, 0.4);
        font-size: 12.5px;
    }

    .metric-row:last-child {
        border-bottom: none;
    }

    .metric-label {
        color: var(--muted);
        font-weight: 500;
    }

    .metric-value {
        color: var(--text);
        font-weight: 700;
        text-align: right;
        font-family: "Space Mono", monospace, sans-serif;
    }

    .health-track {
        background: #0C1420;
        border-radius: 6px;
        overflow: hidden;
        display: flex;
        height: 12px;
        border: 1px solid var(--border);
        margin: 8px 0 12px;
    }

    .health-seg { height: 12px; }

    .legend {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        color: var(--muted);
        font-size: 11.5px;
        margin-bottom: 12px;
    }

    .dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 5px;
    }

    .verified, .review-flag {
        background: rgba(15, 24, 38, 0.6);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 14px;
        margin-top: 10px;
    }

    .verified { border-left: 4px solid var(--success); }
    .review-flag { border-left: 4px solid var(--warning); }

    .status-line {
        font-size: 14px;
        font-weight: 750;
        letter-spacing: .08em;
        color: var(--text);
    }

    .status-copy {
        color: var(--muted);
        font-size: 11.5px;
        margin-top: 2px;
    }

    .missing-banner, .warn-banner, .ok-banner {
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: .05em;
        margin-bottom: 8px;
    }

    .missing-banner {
        background: rgba(251,113,133,.08);
        border: 1px solid rgba(251,113,133,.7);
        color: var(--danger);
    }

    .warn-banner {
        background: rgba(251,191,36,.08);
        border: 1px solid rgba(251,191,36,.55);
        color: var(--warning);
    }

    .ok-banner {
        background: rgba(52,211,153,.08);
        border: 1px solid rgba(52,211,153,.55);
        color: var(--success);
    }

    .badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: .06em;
        border: 1px solid var(--border);
        background: var(--surface-3);
    }

    .badge-match {
        color: var(--success);
        border-color: rgba(52,211,153,.3);
        background: rgba(52,211,153,.08);
    }

    .badge-human {
        color: var(--warning);
        border-color: rgba(251,191,36,.3);
        background: rgba(251,191,36,.08);
    }

    .badge-ex {
        color: var(--danger);
        border-color: rgba(251,113,133,.3);
        background: rgba(251,113,133,.08);
    }

    .badge-neutral {
        color: var(--muted);
        border-color: var(--border);
        background: var(--surface-3);
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    textarea {
        background: #0F1826 !important;
        border-color: var(--border) !important;
    }

    input, textarea {
        color: var(--text) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg,#1597C7,#38BDF8) !important;
        color: #04111B !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 750 !important;
    }

    [data-testid="stDataFrame"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow-x: auto !important;
        max-width: 100% !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        background: rgba(17,24,39,.72);
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    footer { visibility: hidden; }
</style>
    """,
    unsafe_allow_html=True,
)

def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

def is_true(value):
    if isinstance(value, bool):
        return value
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}

def money(value):
    if pd.isna(value) or value is None:
        return "—"
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "—"

def pct_label(count, total):
    if not total:
        return "0.0%"
    return f"{count / total * 100:.1f}%"

def badge(label):
    text = "" if pd.isna(label) else str(label).upper()
    klass = "badge-neutral"
    if text in {"MATCH", "MATCHED"}:
        klass = "badge-match"
    elif text == "HUMAN_REVIEW":
        klass = "badge-human"
    elif text in {"EXCEPTION", "UNMATCHED", "API_ERROR"}:
        klass = "badge-ex"
    return f'<span class="badge {klass}">{text or "—"}</span>'

def final_system_decision(reconciliation_row, audit_rows):
    if audit_rows is not None and not audit_rows.empty:
        value = audit_rows.iloc[-1].get("final_decision")
        if pd.notna(value) and str(value).strip():
            return str(value).strip().upper()

    if reconciliation_row is None or reconciliation_row.empty:
        return "—"

    status = str(
        reconciliation_row.iloc[0].get("reconciliation_status", "")
    ).upper()

    mapping = {
        "MATCHED": "MATCH",
        "UNMATCHED": "EXCEPTION",
        "HUMAN_REVIEW": "HUMAN_REVIEW",
        "MATCH": "MATCH",
        "EXCEPTION": "EXCEPTION",
    }
    return mapping.get(status, status or "—")

def lookup_records(transaction_id):
    ledger = load_csv("company_ledger.csv")
    settlements = load_csv("settlements.csv")
    bank = load_csv("bank_statement.csv")
    invoices = load_csv("invoices.csv")
    reconciliation = load_csv("reconciliation_results.csv")
    audit_log = load_csv("audit_log.csv")
    evaluation = load_csv("evaluation_results.csv")

    txn = str(transaction_id).upper().strip()

    ledger_row = pd.DataFrame()
    settlement_rows = pd.DataFrame()
    invoice_row = pd.DataFrame()
    reconciliation_row = pd.DataFrame()
    bank_rows = pd.DataFrame()
    audit_rows = pd.DataFrame()
    evaluation_row = pd.DataFrame()

    if not ledger.empty and "transaction_id" in ledger.columns:
        ledger_row = ledger[ledger["transaction_id"].astype(str) == txn]

    if not settlements.empty and "transaction_id" in settlements.columns:
        settlement_rows = settlements[
            settlements["transaction_id"].astype(str) == txn
        ]

    if not invoices.empty and "transaction_id" in invoices.columns:
        invoice_row = invoices[invoices["transaction_id"].astype(str) == txn]

    if (
        not reconciliation.empty
        and "transaction_id" in reconciliation.columns
    ):
        reconciliation_row = reconciliation[
            reconciliation["transaction_id"].astype(str) == txn
        ]

    if not bank.empty and "description" in bank.columns:
        bank_rows = bank[
            bank["description"].astype(str).str.contains(txn, na=False, regex=False)
        ]

    if not audit_log.empty and "transaction_id" in audit_log.columns:
        audit_rows = audit_log[
            audit_log["transaction_id"].astype(str) == txn
        ]

    if not evaluation.empty and "transaction_id" in evaluation.columns:
        evaluation_row = evaluation[
            evaluation["transaction_id"].astype(str) == txn
        ]

    return {
        "ledger_row": ledger_row,
        "settlement_rows": settlement_rows,
        "invoice_row": invoice_row,
        "reconciliation_row": reconciliation_row,
        "bank_rows": bank_rows,
        "audit_rows": audit_rows,
        "evaluation_row": evaluation_row,
    }

def render_detail(label, value):
    st.markdown(
        f'<div class="detail-grid">'
        f'<div class="detail-k">{label}</div>'
        f'<div class="detail-v">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

def render_transaction_inspector(transaction_id):
    txn = str(transaction_id).upper().strip()

    if not txn:
        st.warning("Enter a transaction ID such as TXN0013.")
        return

    records = lookup_records(txn)
    ledger_row = records["ledger_row"]

    if ledger_row.empty:
        st.error(f"No ledger record found for {txn}.")
        return

    row = ledger_row.iloc[0]
    settlement_rows = records["settlement_rows"]
    bank_rows = records["bank_rows"]
    invoice_row = records["invoice_row"]
    reconciliation_row = records["reconciliation_row"]
    audit_rows = records["audit_rows"]
    evaluation_row = records["evaluation_row"]

    decision = final_system_decision(reconciliation_row, audit_rows)
    if not evaluation_row.empty and "system_decision" in evaluation_row.columns:
        eval_decision = evaluation_row.iloc[0].get("system_decision")
        if pd.notna(eval_decision) and str(eval_decision).strip():
            decision = str(eval_decision).strip().upper()

    st.markdown(
        f'<div class="ok-banner">TRANSACTION FOUND: {txn}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="margin:10px 0 16px 0; font-size:14px; font-weight:600;">'
        f'Final Decision &nbsp; {badge(decision)}</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        # Ledger Section Card
        st.markdown(
            f"""
            <div class="inspector-card">
                <div class="inspector-card-title">Ledger</div>
                <div class="detail-grid"><div class="detail-k">Amount</div><div class="detail-v">{money(row.get("amount"))}</div></div>
                <div class="detail-grid"><div class="detail-k">Date</div><div class="detail-v">{row.get("transaction_date", "—")}</div></div>
                <div class="detail-grid"><div class="detail-k">Customer</div><div class="detail-v">{row.get("customer_id", "—")}</div></div>
                <div class="detail-grid"><div class="detail-k">Type</div><div class="detail-v">{row.get("transaction_type", "—")}</div></div>
                <div class="detail-grid"><div class="detail-k">Status</div><div class="detail-v">{row.get("status", "—")}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Settlement Section Card
        if settlement_rows.empty:
            st.markdown(
                """
                <div class="inspector-card">
                    <div class="inspector-card-title">Settlement</div>
                    <div class="warn-banner">SETTLEMENT RECORD MISSING</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            settle_net = settlement_rows["net_settlement"].sum() if "net_settlement" in settlement_rows.columns else 0
            settle_fee = settlement_rows["fee"].sum() if "fee" in settlement_rows.columns else 0
            settle_refund = settlement_rows["refund_amount"].sum() if "refund_amount" in settlement_rows.columns else 0
            settle_html = f"""
            <div class="inspector-card">
                <div class="inspector-card-title">Settlement</div>
                <div class="detail-grid"><div class="detail-k">Records</div><div class="detail-v">{len(settlement_rows)}</div></div>
                <div class="detail-grid"><div class="detail-k">Total settlement</div><div class="detail-v">{money(settle_net)}</div></div>
                <div class="detail-grid"><div class="detail-k">Total fees</div><div class="detail-v">{money(settle_fee)}</div></div>
                <div class="detail-grid"><div class="detail-k">Total refunds</div><div class="detail-v">{money(settle_refund)}</div></div>
            """
            if len(settlement_rows) > 1:
                settle_html += '<div class="detail-grid"><div class="detail-k">Note</div><div class="detail-v">Multiple settlement records detected</div></div>'
            settle_html += "</div>"
            st.markdown(settle_html, unsafe_allow_html=True)
            st.dataframe(settlement_rows, use_container_width=True, hide_index=True)

    with col_b:
        # Bank Section Card
        if bank_rows.empty:
            st.markdown(
                """
                <div class="inspector-card">
                    <div class="inspector-card-title">Bank</div>
                    <div class="missing-banner">BANK RECORD MISSING</div>
                    <div style="font-size:12px; color:var(--muted); margin-top:6px; line-height:1.4;">
                        No bank statement line contains this transaction ID. A missing bank record is not treated as a zero credit.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            bank_credit = bank_rows["credit"].sum() if "credit" in bank_rows.columns else 0
            st.markdown(
                f"""
                <div class="inspector-card">
                    <div class="inspector-card-title">Bank</div>
                    <div class="detail-grid"><div class="detail-k">Bank records</div><div class="detail-v">{len(bank_rows)}</div></div>
                    <div class="detail-grid"><div class="detail-k">Total credit</div><div class="detail-v">{money(bank_credit)}</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.dataframe(bank_rows, use_container_width=True, hide_index=True)

        # Invoice Section Card
        if invoice_row.empty:
            st.markdown(
                """
                <div class="inspector-card">
                    <div class="inspector-card-title">Invoice</div>
                    <div class="warn-banner">INVOICE RECORD MISSING</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            inv = invoice_row.iloc[0]
            st.markdown(
                f"""
                <div class="inspector-card">
                    <div class="inspector-card-title">Invoice</div>
                    <div class="detail-grid"><div class="detail-k">Invoice amount</div><div class="detail-v">{money(inv.get("invoice_amount"))}</div></div>
                    <div class="detail-grid"><div class="detail-k">Payment status</div><div class="detail-v">{inv.get("payment_status", "—")}</div></div>
                    <div class="detail-grid"><div class="detail-k">Refund</div><div class="detail-v">{money(inv.get("refund_amount"))}</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Rule-Based Reconciliation Panel
    st.markdown('<div class="section-h">Rule-Based Reconciliation</div>', unsafe_allow_html=True)
    if reconciliation_row.empty:
        st.info("No reconciliation record is available for this transaction.")
    else:
        rec = reconciliation_row.iloc[0]
        rec_html = f"""
        <div class="inspector-card">
            <div class="detail-grid"><div class="detail-k">Status</div><div class="detail-v">{rec.get("reconciliation_status", "—")}</div></div>
        """
        if "settlement_count" in rec:
            rec_html += f'<div class="detail-grid"><div class="detail-k">Settlement count</div><div class="detail-v">{int(rec["settlement_count"])}</div></div>'
        if "bank_transaction_count" in rec:
            bank_count = rec["bank_transaction_count"]
            b_val = "missing" if pd.isna(bank_count) else str(int(bank_count))
            rec_html += f'<div class="detail-grid"><div class="detail-k">Bank transaction count</div><div class="detail-v">{b_val}</div></div>'
            if not pd.isna(bank_count) and int(bank_count) == 0:
                rec_html += '<div class="detail-grid"><div class="detail-k">Bank evidence</div><div class="detail-v">Absent (count is 0; not a zero credit)</div></div>'
        if "amount_explained" in rec:
            rec_html += f'<div class="detail-grid"><div class="detail-k">Amount explained</div><div class="detail-v">{rec["amount_explained"]}</div></div>'
        if "bank_amount_matches" in rec:
            rec_html += f'<div class="detail-grid"><div class="detail-k">Bank amount matches</div><div class="detail-v">{rec["bank_amount_matches"]}</div></div>'
        rec_html += "</div>"
        st.markdown(rec_html, unsafe_allow_html=True)

    # AI Investigation Panel
    st.markdown('<div class="section-h">AI Investigation</div>', unsafe_allow_html=True)
    if audit_rows.empty:
        st.info("No AI investigation recorded for this transaction.")
    else:
        ai = audit_rows.iloc[-1]
        st.markdown(
            f"""
            <div class="inspector-card">
                <div class="detail-grid"><div class="detail-k">Provider</div><div class="detail-v">{ai.get("ai_provider", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">AI status</div><div class="detail-v">{ai.get("ai_status", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">AI decision</div><div class="detail-v">{ai.get("ai_decision", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">Confidence</div><div class="detail-v">{ai.get("confidence_score", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">Safety override</div><div class="detail-v">{ai.get("safety_override", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">Final decision</div><div class="detail-v">{ai.get("final_decision", "N/A")}</div></div>
                <div class="detail-grid"><div class="detail-k">Reason</div><div class="detail-v">{ai.get("reason", "N/A")}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.sidebar:
    st.markdown('<div class="brand-title">RIVA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">AI Finance Controller</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Transaction Inspector",
            "Settlement Q&A",
            "Audit Trail",
            "Human Review",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        '<div class="online">● SYSTEM ONLINE</div>',
        unsafe_allow_html=True,
    )

if page == "Overview":
    st.markdown('<div class="page-kicker">Control room</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-copy">'
        "Final system metrics are calculated from evaluation_results.csv. "
        "AI provider counts come from audit_log.csv."
        "</div>",
        unsafe_allow_html=True,
    )

    evaluation = load_csv("evaluation_results.csv")
    audit_log = load_csv("audit_log.csv")

    if evaluation.empty:
        st.error(
            "evaluation_results.csv was not found. "
            "Run python src/evaluator.py after reconciliation and AI investigation."
        )
    else:
        total = len(evaluation)
        decisions = (
            evaluation["system_decision"]
            .fillna("")
            .astype(str)
            .str.upper()
        )
        match_count = int((decisions == "MATCH").sum())
        human_count = int((decisions == "HUMAN_REVIEW").sum())
        exception_count = int((decisions == "EXCEPTION").sum())

        if "correct" in evaluation.columns:
            correct_mask = evaluation["correct"].map(is_true)
            correct = int(correct_mask.sum())
            incorrect = int((~correct_mask).sum())
        else:
            correct = 0
            incorrect = 0

        unresolved = int(
            evaluation["system_decision"].isna().sum()
            + (
                evaluation["system_decision"].notna()
                & (decisions == "")
            ).sum()
        )

        accuracy = (correct / total * 100) if total else 0.0

        # KPI Cards Grid - Improved Visual Hierarchy & Contextual Labels
        k1, k2, k3, k4 = st.columns(4)
        cards = [
            (k1, "Total Transactions", total, f"{total} records evaluated"),
            (k2, "Matched", match_count, pct_label(match_count, total)),
            (k3, "Human Review", human_count, pct_label(human_count, total)),
            (k4, "Exceptions", exception_count, pct_label(exception_count, total)),
        ]
        for col, label, value, share in cards:
            with col:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                        <div class="kpi-pct">{share}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        left, right = st.columns((1.35, 1))

        with left:
            match_w = pct_label(match_count, total)
            human_w = pct_label(human_count, total)
            ex_w = pct_label(exception_count, total)

            if not audit_log.empty:
                ai_cases = len(audit_log)
                providers = audit_log["ai_provider"].astype(str).str.upper()
                gemini_count = int((providers == "GEMINI").sum())
                groq_count = int((providers == "GROQ").sum())
                api_errors = int(
                    (audit_log["ai_status"].astype(str).str.upper() == "API_ERROR").sum()
                )
                if "safety_override" in audit_log.columns:
                    safety_overrides = int(
                        audit_log["safety_override"].map(is_true).sum()
                    )
                else:
                    safety_overrides = 0
            else:
                ai_cases = gemini_count = groq_count = 0
                api_errors = safety_overrides = 0

            verified = accuracy == 100 and api_errors == 0
            flag_class = "verified" if verified else "review-flag"
            flag_label = "SYSTEM VERIFIED" if verified else "REVIEW RESULTS"

            st.markdown(
                f"""
                <div class="panel">
                    <div class="panel-title">Reconciliation Health</div>
                    <div class="health-track">
                        <div class="health-seg" style="width:{match_w};background:#35C759;"></div>
                        <div class="health-seg" style="width:{human_w};background:#E5A23C;"></div>
                        <div class="health-seg" style="width:{ex_w};background:#FF6B5F;"></div>
                    </div>
                    <div class="legend">
                        <span><span class="dot" style="background:#35C759;"></span>Match {match_count} ({match_w})</span>
                        <span><span class="dot" style="background:#E5A23C;"></span>Human review {human_count} ({human_w})</span>
                        <span><span class="dot" style="background:#FF6B5F;"></span>Exception {exception_count} ({ex_w})</span>
                    </div>
                    <div class="{flag_class}">
                        <div class="status-line">{flag_label}</div>
                        <div class="status-copy">Latest evaluated dataset</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if audit_log.empty:
                st.info("audit_log.csv was not found. AI metrics are shown as zero.")

        with right:
            # Benchmark Verification Panel with right-aligned metrics
            st.markdown(
                '<div class="panel"><div class="panel-title">Benchmark Verification</div>',
                unsafe_allow_html=True,
            )
            rows = [
                ("Correct decisions", correct),
                ("Total decisions", total),
                ("Accuracy", f"{accuracy:.2f}%"),
                ("Incorrect", incorrect),
                ("Unresolved", unresolved),
            ]
            html = "".join(
                f'<div class="metric-row"><span class="metric-label">{k}</span>'
                f'<span class="metric-value">{v}</span></div>'
                for k, v in rows
            )
            st.markdown(html + "</div>", unsafe_allow_html=True)

            # AI Investigation Panel with right-aligned metrics
            st.markdown(
                '<div class="panel"><div class="panel-title">AI Investigation</div>',
                unsafe_allow_html=True,
            )
            ai_rows = [
                ("AI cases", ai_cases),
                ("Gemini", gemini_count),
                ("Groq fallback", groq_count),
                ("API errors", api_errors),
                ("Safety overrides", safety_overrides),
            ]
            html = "".join(
                f'<div class="metric-row"><span class="metric-label">{k}</span>'
                f'<span class="metric-value">{v}</span></div>'
                for k, v in ai_rows
            )
            st.markdown(html + "</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-h">Scenario Breakdown</div>', unsafe_allow_html=True)
        if "scenario" in evaluation.columns:
            scenario = (
                evaluation.groupby(
                    ["scenario", "system_decision"],
                    dropna=False,
                )
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False)
            )
            st.dataframe(scenario, use_container_width=True, hide_index=True)
        else:
            st.info("No scenario column found in evaluation_results.csv.")

        st.markdown('<div class="section-h">Recent Exceptions</div>', unsafe_allow_html=True)
        exceptions = evaluation[decisions == "EXCEPTION"].copy()
        if exceptions.empty:
            st.info("No exception decisions in the current evaluation file.")
        else:
            exceptions = exceptions.sort_values(
                "transaction_id",
                ascending=False,
            )
            show_cols = [
                col
                for col in [
                    "transaction_id",
                    "scenario",
                    "expected_status",
                    "rule_decision",
                    "system_decision",
                    "ai_provider",
                ]
                if col in exceptions.columns
            ]
            st.dataframe(
                exceptions[show_cols].head(15),
                use_container_width=True,
                hide_index=True,
            )

elif page == "Transaction Inspector":
    st.markdown('<div class="page-kicker">Evidence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-title">Transaction Inspector</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-copy">'
        "Inspect the ledger, settlement, bank, invoice, rule result, "
        "and AI trail for a single transaction."
        "</div>",
        unsafe_allow_html=True,
    )

    with st.form("inspect_form"):
        transaction_id = st.text_input(
            "Transaction ID",
            value="TXN0013",
            placeholder="TXN0013",
        )
        submitted = st.form_submit_button("Inspect transaction")

    if submitted or transaction_id:
        render_transaction_inspector(transaction_id)

elif page == "Settlement Q&A":
    st.markdown('<div class="page-kicker">Investigation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-title">Settlement Q&A</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-copy">'
        "Ask a question that includes a transaction ID. "
        "RIVA retrieves recorded evidence and answers through the existing "
        "Gemini → Groq fallback path. No answers are invented."
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption("Example: Why is TXN0013 an exception?")

    with st.form("qa_form"):
        question = st.text_input("Question")
        asked = st.form_submit_button("Ask RIVA")

    if asked:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                from settlement_qna import (
                    extract_transaction_id,
                    get_transaction_evidence,
                    build_prompt,
                    answer_question,
                )
            except Exception as error:
                st.error(
                    "The Settlement Q&A module could not be loaded. "
                    f"{error}"
                )
            else:
                transaction_id = extract_transaction_id(question)

                if not transaction_id:
                    st.warning(
                        "Please include a transaction ID such as TXN0013."
                    )
                else:
                    try:
                        evidence = get_transaction_evidence(transaction_id)
                    except FileNotFoundError:
                        st.error(
                            "Required data files are missing. "
                            "Confirm the CSV files exist in the data folder."
                        )
                    except Exception as error:
                        st.error(
                            "Could not load transaction evidence. "
                            f"{error}"
                        )
                    else:
                        has_records = any(
                            evidence[key]
                            for key in evidence
                            if key != "transaction_id"
                        )

                        if not has_records:
                            st.error(
                                f"No records found for {transaction_id}."
                            )
                        else:
                            if not evidence.get("bank_records"):
                                st.markdown(
                                    '<div class="missing-banner">'
                                    "BANK RECORD MISSING"
                                    "</div>",
                                    unsafe_allow_html=True,
                                )
                            if not evidence.get("settlements"):
                                st.markdown(
                                    '<div class="warn-banner">'
                                    "SETTLEMENT RECORD MISSING"
                                    "</div>",
                                    unsafe_allow_html=True,
                                )
                            if not evidence.get("invoice"):
                                st.markdown(
                                    '<div class="warn-banner">'
                                    "INVOICE RECORD MISSING"
                                    "</div>",
                                    unsafe_allow_html=True,
                                )

                            prompt = build_prompt(question, evidence)

                            with st.spinner("Investigating from recorded evidence…"):
                                try:
                                    answer, provider = answer_question(
                                        question,
                                        evidence,
                                    )
                                except ValueError as error:
                                    st.error(str(error))
                                except Exception as error:
                                    st.error(
                                        "The AI services could not complete "
                                        "this question. "
                                        f"{error}"
                                    )
                                else:
                                    if not answer or not str(answer).strip():
                                        st.error(
                                            "The AI provider returned an empty response."
                                        )
                                    else:
                                        st.markdown(
                                            f'<div class="panel">'
                                            f'<div class="panel-title">'
                                            f"Provider · {provider}"
                                            f"</div>"
                                            f'<div style="font-size:14px; line-height:1.6; color:var(--text);">{answer}</div>'
                                            f'</div>',
                                            unsafe_allow_html=True,
                                        )

                                    if provider == "NONE":
                                        st.warning(
                                            "Both Gemini and Groq were unavailable. "
                                            "The message above is a safety response, "
                                            "not a transaction conclusion."
                                        )

                                    with st.expander("Evidence used", expanded=False):
                                        st.json(evidence)

                                    with st.expander("Prompt sent to the model", expanded=False):
                                        st.code(prompt, language="markdown")

elif page == "Audit Trail":
    st.markdown('<div class="page-kicker">Trace</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Audit Trail</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-copy">'
        "AI investigation records from audit_log.csv. "
        "Raw batch JSON is hidden unless expanded."
        "</div>",
        unsafe_allow_html=True,
    )

    audit_log = load_csv("audit_log.csv")

    if audit_log.empty:
        st.error(
            "audit_log.csv was not found. "
            "Run python src/ai_investigator.py to generate it."
        )
    else:
        providers = sorted(
            audit_log["ai_provider"].dropna().astype(str).str.upper().unique()
        )
        statuses = sorted(
            audit_log["ai_status"].dropna().astype(str).str.upper().unique()
        )
        decisions = sorted(
            audit_log["final_decision"].dropna().astype(str).str.upper().unique()
        )

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            txn_filter = st.text_input("Transaction ID", key="audit_txn_filter").upper().strip()
        with f2:
            provider_filter = st.selectbox(
                "Provider",
                ["All"] + providers,
                key="audit_provider_select",
            )
        with f3:
            status_filter = st.selectbox(
                "AI status",
                ["All"] + statuses,
                key="audit_status_select",
            )
        with f4:
            decision_filter = st.selectbox(
                "Final decision",
                ["All"] + decisions,
                key="audit_decision_select",
            )

        filtered = audit_log.copy()
        filtered["ai_provider"] = filtered["ai_provider"].astype(str).str.upper()
        filtered["ai_status"] = filtered["ai_status"].astype(str).str.upper()
        filtered["final_decision"] = (
            filtered["final_decision"].astype(str).str.upper()
        )

        if txn_filter:
            filtered = filtered[
                filtered["transaction_id"].astype(str).str.upper() == txn_filter
            ]
        if provider_filter != "All":
            filtered = filtered[filtered["ai_provider"] == provider_filter]
        if status_filter != "All":
            filtered = filtered[filtered["ai_status"] == status_filter]
        if decision_filter != "All":
            filtered = filtered[filtered["final_decision"] == decision_filter]

        display_cols = [
            col
            for col in [
                "transaction_id",
                "ai_provider",
                "ai_decision",
                "confidence_score",
                "safety_override",
                "final_decision",
                "reason",
                "processing_time_seconds",
                "ai_status",
            ]
            if col in filtered.columns
        ]

        st.caption(f"{len(filtered)} record(s)")
        st.dataframe(
            filtered[display_cols],
            use_container_width=True,
            hide_index=True,
        )

        if txn_filter and not filtered.empty and "raw_ai_response" in filtered.columns:
            with st.expander("Raw AI response for filtered transaction", expanded=False):
                st.text(str(filtered.iloc[-1]["raw_ai_response"]))
        elif "raw_ai_response" in audit_log.columns:
            with st.expander("Raw AI response for a selected row", expanded=False):
                options = filtered["transaction_id"].astype(str).tolist()
                if options:
                    chosen = st.selectbox("Transaction", options, key="audit_raw_select")
                    raw = filtered[
                        filtered["transaction_id"].astype(str) == chosen
                    ]
                    if not raw.empty:
                        st.text(str(raw.iloc[-1]["raw_ai_response"]))
                else:
                    st.caption("No rows match the current filters.")

elif page == "Human Review":
    st.markdown('<div class="page-kicker">Queue</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-title">Human Review</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-copy">'
        "Transactions whose final system decision is HUMAN_REVIEW. "
        "This view is read-only. Decisions cannot be changed here."
        "</div>",
        unsafe_allow_html=True,
    )

    evaluation = load_csv("evaluation_results.csv")

    if evaluation.empty:
        st.error(
            "evaluation_results.csv was not found. "
            "The human review queue is built from final system decisions."
        )
    else:
        decisions = (
            evaluation["system_decision"]
            .fillna("")
            .astype(str)
            .str.upper()
        )
        queue = evaluation[decisions == "HUMAN_REVIEW"].copy()

        if queue.empty:
            st.info("There are no HUMAN_REVIEW transactions in the current results.")
        else:
            show_cols = [
                col
                for col in [
                    "transaction_id",
                    "scenario",
                    "expected_status",
                    "rule_decision",
                    "system_decision",
                    "ai_provider",
                ]
                if col in queue.columns
            ]
            st.caption(f"{len(queue)} transaction(s) in queue")
            st.dataframe(
                queue[show_cols],
                use_container_width=True,
                hide_index=True,
            )

            selected = st.selectbox(
                "Inspect a transaction",
                queue["transaction_id"].astype(str).tolist(),
                key="human_review_select",
            )
            if selected:
                render_transaction_inspector(selected)