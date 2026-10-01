from modules.theory import show_module_theory
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def bar_graph_page():
    st.title("📈 Bar Graph Analysis")
    st.write("Enter category values and analyze them visually.")

    show_module_theory('Bar Graph Analysis')


    default = pd.DataFrame({"Category": ["A","B","C","D","E"], "Value": [40,65,55,80,50]})
    df = st.data_editor(default, num_rows="dynamic", use_container_width=True, key="bar_editor")

    fig, ax = plt.subplots()
    ax.bar(df["Category"].astype(str), df["Value"])
    ax.set_title("Bar Graph")
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.grid(axis="y", alpha=0.2)
    st.pyplot(fig)

    mx = df.loc[df["Value"].idxmax()]
    mn = df.loc[df["Value"].idxmin()]
    total = df["Value"].sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("Highest", f"{mx['Category']} ({mx['Value']})")
    c2.metric("Lowest", f"{mn['Category']} ({mn['Value']})")
    c3.metric("Total", f"{total:,.0f}")

    st.subheader("Percentage Contribution")
    out = df.copy()
    out["Contribution (%)"] = (out["Value"] / total * 100).round(2) if total else 0
    st.dataframe(out, use_container_width=True, hide_index=True)
