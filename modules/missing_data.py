from modules.theory import show_module_theory
import streamlit as st
import pandas as pd
import numpy as np

def missing_data_page():
    st.title("🔍 Missing Data Interpretation")
    st.write("Find an unknown value when the row/column total is known.")

    show_module_theory('Missing Data Interpretation')


    st.subheader("Example")
    example = pd.DataFrame({
        "Student": ["A", "B", "C"],
        "Maths": [80, 70, 90],
        "Physics": [75, np.nan, 85],
        "Chemistry": [85, 80, 95],
        "Total": [240, 220, 270]
    })
    st.dataframe(example, use_container_width=True, hide_index=True)

    st.markdown("For Student B:")
    st.code("Physics = Total − Maths − Chemistry")
    st.success("Physics = 220 − 70 − 80 = 70")

    st.divider()
    st.subheader("🧮 Custom Missing Value Calculator")
    total = st.number_input("Known total", min_value=0.0, value=220.0, step=1.0)
    known1 = st.number_input("Known value 1", min_value=0.0, value=70.0, step=1.0)
    known2 = st.number_input("Known value 2", min_value=0.0, value=80.0, step=1.0)
    if st.button("Calculate Missing Value", type="primary"):
        missing = total - known1 - known2
        if missing < 0:
            st.error("The input values exceed the total. Check the data.")
        else:
            st.success(f"Missing value = **{missing:g}**")

    st.subheader("📊 Percentage-based Missing Value")
    total_pct = st.number_input("Total percentage", min_value=0.0, max_value=100.0, value=100.0, step=1.0)
    known_pct = st.number_input("Known percentage", min_value=0.0, max_value=100.0, value=65.0, step=1.0)
    st.info(f"Missing percentage = **{total_pct-known_pct:.2f}%**")
