from modules.theory import show_module_theory
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def pie_chart_page():
    st.title("🥧 Pie Chart Analysis")
    st.write("Analyze percentages, sector angles and category contributions.")

    show_module_theory('Pie Chart Analysis')


    default = pd.DataFrame({
        "Category": ["Food", "Rent", "Travel", "Education", "Other"],
        "Value": [30, 35, 15, 10, 10]
    })
    df = st.data_editor(default, num_rows="dynamic", use_container_width=True, key="pie_editor")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
    df = df[df["Value"] >= 0]

    total = df["Value"].sum()
    if total <= 0:
        st.error("Total must be greater than zero.")
        return

    fig, ax = plt.subplots()
    ax.pie(df["Value"], labels=df["Category"], autopct="%1.1f%%")
    ax.set_title("Pie Chart")
    st.pyplot(fig)

    out = df.copy()
    out["Percentage (%)"] = (out["Value"] / total * 100).round(2)
    out["Sector Angle (°)"] = (out["Value"] / total * 360).round(2)
    st.dataframe(out, use_container_width=True, hide_index=True)

    selected = st.selectbox("Select category", out["Category"])
    row = out[out["Category"] == selected].iloc[0]
    st.success(f"{selected}: {row['Percentage (%)']}% = {row['Sector Angle (°)']}°")
