import os
import streamlit as st

try:
    from google import genai
except Exception:
    genai = None

def _api_key():
    return st.session_state.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt, model="gemini-3.8-flash"):
    key = _api_key()
    if not key:
        return None, "Add a Gemini API key in the AI Tutor page or set GEMINI_API_KEY in your environment."
    if genai is None:
        return None, "Gemini SDK is not installed. Run: pip install -r requirements.txt"
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text, None
    except Exception as exc:
        return None, f"Gemini request failed: {exc}"

def gemini_page():
    st.markdown('<div class="hero"><div class="hero-badge">AI STUDY ASSISTANT</div><div class="hero-title">Your personal aptitude tutor</div><div class="hero-text">Use Gemini to explain difficult concepts, guide your reasoning, generate practice questions and turn mistakes into quick revision notes.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Choose how you want to learn</div>', unsafe_allow_html=True)

    with st.expander("🔐 Gemini API Setup", expanded=not bool(_api_key())):
        st.caption("Your API key is used only for this running app session. For a permanent setup, use the GEMINI_API_KEY environment variable or Streamlit secrets.")
        key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_api_key", ""), key="gemini_key_input")
        if st.button("Save Key", type="primary"):
            st.session_state.gemini_api_key = key.strip()
            st.success("API key saved for this session.")

    modules=["All Modules","Clock Problems","Calendar Problems","Pattern Recognition","Tabular Data Interpretation","Bar Graph Analysis","Pie Chart Analysis","Line Graph Analysis","Missing Data Interpretation"]
    module=st.selectbox("1. Learning context",modules)
    mode=st.selectbox("2. Learning mode",["Explain a concept","Give me a hint","Solve step-by-step","Create practice questions","Check my solution","Create a short revision note"])
    question=st.text_area("3. What are you working on?",height=150,placeholder="Example: Explain why the hour hand moves 0.5° per minute, with an example.")

    if st.button("✨ Ask Gemini",type="primary",use_container_width=True):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            prompt=f"""You are the LogicIQ college aptitude tutor. Be accurate, exam-oriented and clear.
Module: {module}
Task: {mode}
Student request: {question}

Rules:
- Teach the reasoning, not just the final answer.
- Use step-by-step calculations for numerical problems.
- For Clock, use the moving hour-hand formula and distinguish smaller/larger angles.
- For Calendar, use Gregorian leap-year rules and modulo-7 reasoning.
- For DI, state the denominator when calculating percentages.
- If the student's information is insufficient, ask for the missing value instead of inventing it.
- Format formulas clearly and finish with an exam tip.
"""
            with st.spinner("Gemini is thinking..."):
                answer,error=ask_gemini(prompt)
            if error: st.error(error)
            else: st.markdown(answer)

    st.info("Tip: For a college demo, configure GEMINI_API_KEY before launching Streamlit so the AI Tutor is ready without entering the key every time.")
