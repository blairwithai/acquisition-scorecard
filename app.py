
import os
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Acquisition Scorecard", page_icon="✅", layout="wide")
st.title("✅ Acquisition Scorecard (Interactive)")

st.markdown("""
Upload your **Acquisition Scorecard** (XLSX/CSV) or use the bundled example in `/data`.
- Edit **Scores (0–5)**, **Weights**, **Responsible Party**, and optional **Notes**.
- Live **category scores** and **overall score**.
- Export a **summary CSV** or the **full edited table**.
""")

# ---------- File handling ----------
file = st.file_uploader("Upload XLSX/CSV", type=["xlsx", "xls", "csv"])

default_path = "data/TEMPLATE_Acquisition_Scorecard.xlsx"
if file is not None:
    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, sheet_name=0)
else:
    if os.path.exists(default_path):
        df = pd.read_excel(default_path)
        st.info("Using bundled example: data/TEMPLATE_Acquisition_Scorecard.xlsx")
    else:
        st.warning("No file uploaded and no bundled example found. Please upload a scorecard file.")
        st.stop()

# ---------- Normalize columns ----------
def pick(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None

col_category = pick(df.columns, ["Category", "category"])
col_item     = pick(df.columns, ["Item","Question","Metric","item"])
col_party    = pick(df.columns, ["Responsible Party for Assessment","Responsible","Owner","Assignee"])
col_weight   = pick(df.columns, ["Weight","Weighting","weight"])
col_score    = pick(df.columns, ["Score (1-5)","Score","Rating","score"])

needed = [col_category, col_item, col_weight, col_score]
if any(c is None for c in needed):
    st.error(f"Missing one or more required columns. Found: {list(df.columns)}")
    st.stop()

# Optional notes
if "Notes" not in df.columns:
    df["Notes"] = ""

# Clean empty rows
df = df.dropna(how="all")
if col_category in df.columns:
    df = df[~df[col_category].isna()]

# ---------- Sidebar options ----------
st.sidebar.header("Options")
lock_weights = st.sidebar.checkbox("Lock weights", value=True)
score_step = st.sidebar.select_slider("Score granularity", options=[0.1,0.5,1.0], value=0.5)
show_notes = st.sidebar.checkbox("Enable notes per line item", value=True)

# ---------- Interactive editor ----------
st.subheader("Score the items")
rows = []
for cat, group in df.groupby(col_category, sort=False):
    with st.expander(f"📂 {cat}", expanded=True):
        for idx, row in group.iterrows():
            cols = st.columns([3, 2, 2, 2, 3] if show_notes else [3,2,2,2])
            with cols[0]:
                st.markdown(f"**{row[col_item]}**")
            with cols[1]:
                party_val = st.text_input("Responsible", value=str(row.get(col_party,"") or ""), key=f"r_{idx}", label_visibility="collapsed")
            with cols[2]:
                w = float(row.get(col_weight, 0.25) or 0.0)
                if lock_weights:
                    weight_val = st.number_input("Weight", value=w, step=0.05, key=f"w_{idx}", disabled=True, label_visibility="collapsed")
                else:
                    weight_val = st.number_input("Weight", value=w, step=0.05, min_value=0.0, max_value=5.0, key=f"w_{idx}", label_visibility="collapsed")
            with cols[3]:
                score_val = st.number_input("Score", value=float(row.get(col_score,0.0) or 0.0), step=float(score_step), min_value=0.0, max_value=5.0, key=f"s_{idx}", label_visibility="collapsed")
            if show_notes:
                with cols[4]:
                    note = st.text_input("Notes", value=str(row.get("Notes","") or ""), key=f"n_{idx}", label_visibility="collapsed")
            else:
                note = row.get("Notes","")
            rows.append({
                col_category: cat,
                col_item: row[col_item],
                col_party: party_val,
                col_weight: weight_val,
                col_score: score_val,
                "Notes": note
            })

clean = pd.DataFrame(rows)
clean["Weighted Score"] = clean[col_weight] * clean[col_score]

# ---------- Category/overall ----------
summary = clean.groupby(col_category).agg(
    Items=("Notes","count"),
    Weight_Sum=(col_weight,"sum"),
    Weighted_Sum=("Weighted Score","sum")
).reset_index()
summary["Max_Points"] = summary["Weight_Sum"]*5
summary["Score_%"] = np.where(summary["Max_Points"]>0, (summary["Weighted_Sum"]/summary["Max_Points"])*100, np.nan).round(2)

overall_weighted = summary["Weighted_Sum"].sum()
overall_weight = summary["Weight_Sum"].sum()
overall_pct = (overall_weighted/(overall_weight*5)*100) if overall_weight>0 else np.nan
overall_pct = np.round(overall_pct, 2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Weighted", f"{overall_weighted:,.3f}")
c2.metric("Total Weight", f"{overall_weight:,.3f}")
c3.metric("Overall Score", f"{overall_pct:.2f}%")
def badge(p):
    return "🟢" if p>=85 else ("🟡" if p>=70 else "🔴")
c4.metric("Deal Signal", f"{badge(overall_pct)}")

st.subheader("Category Breakdown")
show_cols = {
    "Category": summary[col_category],
    "Items": summary["Items"],
    "Weight Sum": summary["Weight_Sum"],
    "Weighted Sum": summary["Weighted_Sum"],
    "Score %": summary["Score_%"]
}
st.dataframe(pd.DataFrame(show_cols), use_container_width=True)

# ---------- Exports ----------
st.subheader("Exports")
st.download_button(
    "Download Summary CSV",
    summary.assign(Overall_Score_Percent=overall_pct).to_csv(index=False).encode("utf-8"),
    file_name="scorecard_summary.csv",
    mime="text/csv"
)
st.download_button(
    "Download Full Table CSV",
    clean.to_csv(index=False).encode("utf-8"),
    file_name="scorecard_full.csv",
    mime="text/csv"
)

st.caption("Tip: Lock weights for consistent scoring across deals. Use notes to justify each rating.")
