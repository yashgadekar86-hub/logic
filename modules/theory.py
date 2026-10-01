import json, os
import streamlit as st

_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "module_theory.json")

@st.cache_data
def load_module_theory():
    with open(_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def show_module_theory(module_name):
    data = load_module_theory().get(module_name)
    if not data:
        return
    st.divider()
    st.markdown(f'<div class="module-hero"><div class="module-hero-kicker">LEARNING MODULE</div><div class="module-hero-title">{data["title"]}</div><div class="module-hero-text">Learn the core idea, study the method, then apply it in practice.</div></div>', unsafe_allow_html=True)
    st.markdown(data["overview"])
    st.markdown('<div class="journey-label">YOUR LEARNING JOURNEY</div>', unsafe_allow_html=True)
    j1,j2,j3,j4=st.columns(4)
    journey=[("01","Learn","Understand the concept"),("02","Formula","Remember the method"),("03","Example","See it solved"),("04","Practice","Test yourself")]
    for col,(num,title,text) in zip([j1,j2,j3,j4],journey):
        with col:
            st.markdown(f'<div class="journey-card"><span>{num}</span><strong>{title}</strong><small>{text}</small></div>',unsafe_allow_html=True)
    with st.expander("📘 Core Concepts", expanded=True):
        for x in data["concepts"]: st.markdown(f"- {x}")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🧮 Important Formulas")
        for x in data["formulas"]: st.markdown(f"- `{x}`")
    with c2:
        st.subheader("📝 Solved Examples")
        for q, sol in data["examples"]:
            with st.expander(q): st.write(sol)
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("⚠️ Common Mistakes")
        for x in data["mistakes"]: st.markdown(f"- {x}")
    with c4:
        st.subheader("🎯 Exam Tips")
        for x in data["tips"]: st.markdown(f"- {x}")
