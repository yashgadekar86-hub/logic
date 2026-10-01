from modules.theory import show_module_theory
import streamlit as st
import pandas as pd
import numpy as np

DEFAULT = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "2023": [120, 150, 100, 180],
    "2024": [150, 165, 130, 210],
})

def tabular_page():
    st.title("📊 Tabular Data Interpretation")
    st.write("Analyze a dataset using totals, averages, differences and percentage change.")

    show_module_theory('Tabular Data Interpretation')


    uploaded = st.file_uploader("Upload CSV (optional)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = DEFAULT.copy()

    st.subheader("Dataset")
    st.data_editor(df, use_container_width=True, num_rows="dynamic", key="table_editor")

    numeric = df.select_dtypes(include=np.number)
    if numeric.empty:
        st.warning("No numeric columns found.")
        return

    st.subheader("📐 Automatic Analysis")
    cols = st.columns(4)
    cols[0].metric("Rows", len(df))
    cols[1].metric("Numeric Columns", len(numeric.columns))
    cols[2].metric("Total", f"{numeric.to_numpy().sum():,.0f}")
    cols[3].metric("Average", f"{numeric.to_numpy().mean():,.2f}")

    st.dataframe(numeric.describe().round(2), use_container_width=True)

    if len(numeric.columns) >= 2:
        a, b = numeric.columns[:2]
        st.write(f"### Percentage Change: {a} → {b}")
        pct = ((df[b] - df[a]) / df[a].replace(0, np.nan) * 100).round(2)
        out = df[[a,b]].copy()
        out["% Change"] = pct
        st.dataframe(out, use_container_width=True, hide_index=True)

    st.subheader("📈 Visualization")
    chart_df = numeric.copy()
    chart_df.index = df.iloc[:,0].astype(str) if len(df.columns) > len(numeric.columns) else chart_df.index.astype(str)
    st.bar_chart(chart_df)
