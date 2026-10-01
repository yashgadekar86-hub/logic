from modules.theory import show_module_theory
import streamlit as st
import random

def pattern_question():
    kind = random.randint(1, 4)
    if kind == 1:
        start = random.randint(1, 8)
        seq = [start + i*i for i in range(1, 5)]
        ans = start + 25
        exp = "The added amounts are consecutive squares: 1², 2², 3², 4², 5²."
    elif kind == 2:
        start = random.randint(2, 8)
        seq = [start * (i+1) for i in range(1, 5)]
        ans = start * 5
        exp = f"Each term is a multiple of {start}; the next multiplier is 5."
    elif kind == 3:
        start = random.randint(2, 6)
        seq = [start]
        for i in range(3):
            seq.append(seq[-1] + (i+2)*2)
        ans = seq[-1] + 10
        exp = "The differences increase by 2 each time."
    else:
        start = random.randint(1, 5)
        seq = [start]
        for _ in range(3):
            seq.append(seq[-1] * 2 + 1)
        ans = seq[-1] * 2 + 1
        exp = "Multiply by 2 and add 1 for every next term."
    return {
        "question": "Find the next number: " + ", ".join(map(str, seq)) + ", ?",
        "answer": ans,
        "explanation": exp + f" Therefore the answer is {ans}."
    }

def patterns_page(record_result):
    st.title("🔢 Figures & Pattern Recognition")
    st.write("Identify numerical patterns and infer the next value.")

    show_module_theory('Pattern Recognition')


    st.info("For a production extension, image-based pattern recognition can be added with OpenCV. This version focuses on logical number-pattern recognition.")

    st.subheader("🎯 Pattern Practice")
    if "pattern_q" not in st.session_state:
        st.session_state.pattern_q = pattern_question()
    if st.button("🎲 New Pattern"):
        st.session_state.pattern_q = pattern_question()

    q = st.session_state.pattern_q
    st.write("###", q["question"])
    ans = st.number_input("Your answer", value=0.0, step=1.0, key="pattern_answer")
    if st.button("Check Pattern"):
        ok = abs(ans - q["answer"]) < 0.01
        record_result("Pattern", ok)
        if ok:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Correct answer: {q['answer']}")
        with st.expander("Explanation"):
            st.write(q["explanation"])
