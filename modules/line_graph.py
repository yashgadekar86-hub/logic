from modules.theory import show_module_theory
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def line_graph_page():
    st.title("📉 Line Graph Analysis")
    st.write("Study trends, increases, decreases and percentage changes.")

    show_module_theory('Line Graph Analysis')


    default = pd.DataFrame({
        "Period": ["Q1","Q2","Q3","Q4","Q5","Q6"],
        "Value": [45, 52, 48, 70, 76, 90]
    })
    df = st.data_editor(default, num_rows="dynamic", use_container_width=True, key="line_editor")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Value"])

    fig, ax = plt.subplots()
    ax.plot(df["Period"].astype(str), df["Value"], marker="o")
    ax.set_title("Line Graph")
    ax.set_xlabel("Period")
    ax.set_ylabel("Value")
    ax.grid(alpha=0.2)
    st.pyplot(fig)

    first = df["Value"].iloc[0]
    last = df["Value"].iloc[-1]
    change = ((last-first)/first*100) if first else 0

    c1,c2,c3 = st.columns(3)
    c1.metric("Highest", f"{df['Value'].max():,.2f}")
    c2.metric("Lowest", f"{df['Value'].min():,.2f}")
    c3.metric("First → Last", f"{change:+.2f}%")

    st.subheader("Period-to-Period Change")
    out = df.copy()
    out["Change"] = out["Value"].diff()
    out["Change (%)"] = out["Value"].pct_change().mul(100).round(2)
    st.dataframe(out, use_container_width=True, hide_index=True)
