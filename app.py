import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import calendar as cal
import random
import math

from modules.clock import clock_page, clock_question
from modules.calendar_module import calendar_page, calendar_question
from modules.patterns import patterns_page, pattern_question
from modules.tabular import tabular_page
from modules.bar_graph import bar_graph_page
from modules.pie_chart import pie_chart_page
from modules.line_graph import line_graph_page
from modules.missing_data import missing_data_page
from modules.gemini_ai import gemini_page

st.set_page_config(
    page_title="LogicIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Session state ----------
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "module_stats" not in st.session_state:
    st.session_state.module_stats = {}
if "history" not in st.session_state:
    st.session_state.history = []

def record_result(module, correct):
    st.session_state.attempts += 1
    if correct:
        st.session_state.correct += 1
    if module not in st.session_state.module_stats:
        st.session_state.module_stats[module] = {"attempts": 0, "correct": 0}
    st.session_state.module_stats[module]["attempts"] += 1
    if correct:
        st.session_state.module_stats[module]["correct"] += 1
    st.session_state.history.append({
        "Module": module,
        "Result": "Correct" if correct else "Wrong"
    })

def reset_progress():
    st.session_state.attempts = 0
    st.session_state.correct = 0
    st.session_state.module_stats = {}
    st.session_state.history = []

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');
:root { --ink:#182230; --muted:#667085; --line:#e7eaf0; --surface:#ffffff; --soft:#f6f8fc; --primary:#4f46e5; --primary2:#7c3aed; --green:#16a34a; }
html, body, [class*="css"] { font-family:'Inter',sans-serif; }
[data-testid="stAppViewContainer"] { background:linear-gradient(180deg,#f8faff 0%,#f7f8fc 42%,#f4f6fa 100%); }
[data-testid="stHeader"] { background:rgba(255,255,255,.82); backdrop-filter:blur(14px); }
.block-container { max-width:1320px; padding-top:2rem; padding-bottom:4rem; }
[data-testid="stSidebar"] { background:rgba(255,255,255,.96); border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child { padding-top:1.25rem; }
.brand { padding:.5rem .35rem 1.35rem; margin-bottom:1rem; border-bottom:1px solid #eef0f4; }
.brand-title { font-family:'Manrope',sans-serif; font-size:1.5rem; font-weight:800; color:var(--ink); letter-spacing:-.04em; }
.brand-subtitle { margin-top:.25rem; color:#7b8494; font-size:.78rem; line-height:1.5; }
.page-kicker { display:inline-flex; padding:.34rem .65rem; border-radius:999px; background:#eef2ff; color:#4f46e5; font-size:.72rem; font-weight:800; letter-spacing:.06em; text-transform:uppercase; margin-bottom:.65rem; }
.page-title, h1 { font-family:'Manrope',sans-serif !important; color:var(--ink) !important; font-weight:800 !important; letter-spacing:-.045em !important; }
.page-title { font-size:2.65rem; line-height:1.08; }
.page-subtitle { color:var(--muted); font-size:1rem; line-height:1.65; margin-bottom:1.5rem; }
.hero { position:relative; overflow:hidden; background:linear-gradient(135deg,#151b36 0%,#29346d 48%,#5b4bd8 100%); border-radius:24px; padding:2rem 2.15rem; color:white; margin:.2rem 0 1.5rem; box-shadow:0 18px 45px rgba(39,46,95,.16); }
.hero:after { content:""; position:absolute; width:260px; height:260px; border-radius:50%; right:-80px; top:-100px; background:rgba(255,255,255,.10); }
.hero-title { font-family:'Manrope',sans-serif; font-size:2rem; font-weight:800; letter-spacing:-.04em; margin-bottom:.4rem; }
.hero-text { color:rgba(255,255,255,.78); max-width:720px; line-height:1.6; }
.hero-badge { display:inline-block; background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.17); padding:.35rem .65rem; border-radius:999px; font-size:.72rem; font-weight:700; margin-bottom:.8rem; }
.metric-card { background:rgba(255,255,255,.9); border:1px solid var(--line); border-radius:18px; padding:1.15rem 1.2rem; box-shadow:0 7px 22px rgba(16,24,40,.045); min-height:108px; }
.metric-label { color:#7a8494; font-size:.76rem; font-weight:700; text-transform:uppercase; letter-spacing:.04em; }
.metric-value { color:var(--ink); font-family:'Manrope',sans-serif; font-size:1.75rem; font-weight:800; margin-top:.25rem; }
.module-card { background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:1.2rem; min-height:160px; margin-bottom:.9rem; box-shadow:0 6px 20px rgba(16,24,40,.035); transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
.module-card:hover { transform:translateY(-3px); box-shadow:0 14px 28px rgba(16,24,40,.08); border-color:#d7dcf2; }
.module-icon { width:42px; height:42px; display:flex; align-items:center; justify-content:center; border-radius:13px; background:#f1f3ff; font-size:1.35rem; margin-bottom:.85rem; }
.module-name { color:var(--ink); font-family:'Manrope',sans-serif; font-size:1rem; font-weight:800; margin-bottom:.35rem; }
.module-description { color:var(--muted); font-size:.82rem; line-height:1.55; }
.section-title { color:var(--ink); font-family:'Manrope',sans-serif; font-size:1.25rem; font-weight:800; margin-top:1.7rem; margin-bottom:.8rem; }
.learning-step { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1rem 1.05rem; height:100%; box-shadow:0 5px 16px rgba(16,24,40,.03); }
.learning-num { color:#4f46e5; font-size:.72rem; font-weight:800; letter-spacing:.06em; text-transform:uppercase; }
.learning-title { color:var(--ink); font-weight:800; margin:.25rem 0; }
.learning-text { color:var(--muted); font-size:.8rem; line-height:1.5; }
.info-strip { background:#fff; border:1px solid var(--line); border-left:4px solid #4f46e5; border-radius:14px; padding:1rem 1.1rem; color:#475467; margin:1rem 0 1.2rem; box-shadow:0 5px 15px rgba(16,24,40,.025); }
[data-testid="stExpander"] { border:1px solid var(--line); border-radius:14px; background:#fff; box-shadow:0 3px 12px rgba(16,24,40,.025); margin-bottom:.55rem; }
[data-testid="stExpander"] summary { font-weight:700; }
div.stButton > button { border-radius:11px; border:1px solid #d5d9e3; font-weight:700; min-height:2.65rem; transition:.15s ease; }
div.stButton > button:hover { border-color:#8b85e9; color:#4338ca; box-shadow:0 5px 14px rgba(79,70,229,.12); }
div.stButton > button[kind="primary"] { background:linear-gradient(135deg,#4f46e5,#6366f1); border-color:#4f46e5; color:#fff; }
div.stButton > button[kind="primary"]:hover { background:linear-gradient(135deg,#4338ca,#4f46e5); color:#fff; }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:14px; padding:.75rem .9rem; box-shadow:0 4px 14px rgba(16,24,40,.03); }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.stProgress > div > div > div > div { background:linear-gradient(90deg,#4f46e5,#7c3aed); }
hr { border-color:#e8ebf1; }
.small-muted { color:#667085; font-size:.84rem; }
.footer { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--line); color:#98a2b3; font-size:.75rem; text-align:center; }
.module-hero { background:linear-gradient(135deg,#ffffff 0%,#f1f3ff 100%); border:1px solid #e1e4f2; border-radius:20px; padding:1.35rem 1.5rem; margin:.25rem 0 1rem; box-shadow:0 7px 20px rgba(48,55,110,.05); }
.module-hero-kicker { color:#6366f1; font-size:.68rem; font-weight:800; letter-spacing:.1em; margin-bottom:.3rem; }
.module-hero-title { font-family:'Manrope',sans-serif; color:var(--ink); font-size:1.65rem; font-weight:800; letter-spacing:-.035em; }
.module-hero-text { color:var(--muted); font-size:.85rem; margin-top:.25rem; }
.journey-label { color:#7a8494; font-size:.7rem; font-weight:800; letter-spacing:.08em; margin:.95rem 0 .55rem; }
.journey-card { background:#fff; border:1px solid var(--line); border-radius:14px; padding:.8rem .85rem; min-height:82px; box-shadow:0 4px 13px rgba(16,24,40,.025); }
.journey-card span { display:block; color:#6366f1; font-size:.65rem; font-weight:800; }
.journey-card strong { display:block; color:var(--ink); font-size:.85rem; margin-top:.2rem; }
.journey-card small { display:block; color:#8a93a2; font-size:.7rem; margin-top:.15rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("""
<div class="brand">
  <div class="brand-title">🧠 LogicIQ</div>
  <div class="brand-subtitle">Logic & Data Interpretation<br>Learning System</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="small-muted"><b>LEARNING PAGES</b></div>', unsafe_allow_html=True)
pages = [
    "🏠 Dashboard",
    "⏰ Clock Problems",
    "📅 Calendar Problems",
    "🔢 Pattern Recognition",
    "📊 Tabular Data Interpretation",
    "📈 Bar Graph Analysis",
    "🥧 Pie Chart Analysis",
    "📉 Line Graph Analysis",
    "🔍 Missing Data Interpretation",
    "🤖 Gemini AI Tutor",
    "📚 Practice Center",
]
page = st.sidebar.radio("Pages", pages, label_visibility="collapsed")
st.sidebar.markdown('<div class="small-muted" style="margin-top:.5rem">Each topic opens as its own focused learning page.</div>', unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown('<div class="small-muted">Current session</div>', unsafe_allow_html=True)
st.sidebar.metric("Questions Attempted", st.session_state.attempts)
accuracy = (st.session_state.correct / st.session_state.attempts * 100) if st.session_state.attempts else 0
st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")
if st.session_state.attempts:
    st.sidebar.caption(f"{st.session_state.correct} correct out of {st.session_state.attempts} attempts.")
if st.sidebar.button("Reset Session", use_container_width=True):
    reset_progress()
    st.rerun()

# ---------- Premium Learning Experience ----------
TOPICS = {
    "Clock": {"icon":"◷", "eyebrow":"REASONING", "title":"Clock Mastery", "desc":"Angles, hand movement, coincidence, mirror clocks and advanced time problems."},
    "Calendar": {"icon":"▣", "eyebrow":"REASONING", "title":"Calendar Mastery", "desc":"Odd days, leap years, weekdays, date differences and recurring calendars."},
    "Patterns": {"icon":"⌁", "eyebrow":"LOGIC", "title":"Pattern Lab", "desc":"Discover sequences, rules and hidden relationships with guided practice."},
    "Tabular": {"icon":"▤", "eyebrow":"DATA", "title":"Table Intelligence", "desc":"Read tables quickly, compare values and solve percentage-based questions."},
    "Bar Graph": {"icon":"▥", "eyebrow":"DATA", "title":"Bar Graph Studio", "desc":"Turn visual comparisons into fast, accurate calculations."},
    "Pie Chart": {"icon":"◔", "eyebrow":"DATA", "title":"Pie Chart Studio", "desc":"Master sectors, percentages, ratios and angle-based interpretation."},
    "Line Graph": {"icon":"⌁", "eyebrow":"DATA", "title":"Trend Studio", "desc":"Read trends, growth, decline and changes across time series."},
    "Missing Data": {"icon":"?", "eyebrow":"DATA", "title":"Missing Data Lab", "desc":"Recover unknown values using constraints, totals and relationships."},
}
if "view" not in st.session_state: st.session_state.view="Home"
if "topic" not in st.session_state: st.session_state.topic=None

st.markdown("""
<style>
[data-testid="stSidebar"] { width:245px !important; }
[data-testid="stSidebar"] .block-container { padding:1rem 1rem 2rem; }
.topbar {display:flex;align-items:center;justify-content:space-between;margin-bottom:1.25rem}
.topbrand {font-family:'Manrope',sans-serif;font-size:1.15rem;font-weight:800;letter-spacing:-.04em;color:#111827}.topbrand span{color:#6366f1}
.eyebrow{font-size:.68rem;font-weight:800;letter-spacing:.12em;color:#6b7280;text-transform:uppercase;margin-bottom:.5rem}
.display-title{font-family:'Manrope',sans-serif;font-size:3rem;line-height:1.02;letter-spacing:-.06em;font-weight:800;color:#111827;margin:0}
.display-sub{color:#667085;font-size:1rem;line-height:1.7;max-width:720px;margin-top:.7rem}
.hero-premium{position:relative;overflow:hidden;border-radius:28px;padding:2.5rem 2.6rem;background:linear-gradient(120deg,#111827 0%,#27315f 52%,#5c55d9 100%);color:white;box-shadow:0 24px 70px rgba(31,41,55,.18);margin:.5rem 0 1.5rem}
.hero-premium:before{content:"";position:absolute;width:340px;height:340px;border:1px solid rgba(255,255,255,.12);border-radius:50%;right:-120px;top:-150px}.hero-premium:after{content:"";position:absolute;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.08);right:70px;bottom:-120px}
.hero-pill{display:inline-block;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.1);padding:.35rem .7rem;border-radius:999px;font-size:.68rem;font-weight:800;letter-spacing:.08em}
.hero-premium h2{font-family:'Manrope',sans-serif;font-size:2.45rem;letter-spacing:-.05em;margin:.8rem 0 .55rem}.hero-premium p{max-width:700px;color:rgba(255,255,255,.78);line-height:1.65;margin:0}
.stat-tile{background:#fff;border:1px solid #e7eaf0;border-radius:20px;padding:1.15rem 1.2rem;box-shadow:0 8px 26px rgba(16,24,40,.045)}.stat-k{color:#8a93a2;font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.stat-v{font-family:'Manrope',sans-serif;color:#111827;font-size:1.8rem;font-weight:800;margin-top:.2rem}.stat-s{color:#667085;font-size:.75rem;margin-top:.15rem}
.topic-card{background:#fff;border:1px solid #e6e9ef;border-radius:22px;padding:1.25rem;min-height:170px;box-shadow:0 8px 24px rgba(16,24,40,.035)}.topic-symbol{width:46px;height:46px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:1.35rem;background:#f4f5ff;margin-bottom:1rem}.topic-eyebrow{color:#7a8494;font-size:.63rem;font-weight:800;letter-spacing:.11em}.topic-title{font-family:'Manrope',sans-serif;color:#111827;font-size:1.05rem;font-weight:800;margin:.25rem 0 .35rem}.topic-desc{color:#667085;font-size:.78rem;line-height:1.55;min-height:48px}
.section-head{display:flex;justify-content:space-between;align-items:end;margin:1.8rem 0 .85rem}.section-head h3{font-family:'Manrope',sans-serif;font-size:1.25rem;letter-spacing:-.03em;margin:0;color:#111827}.section-head p{margin:0;color:#8a93a2;font-size:.78rem}.path-card{background:#fff;border:1px solid #e7eaf0;border-radius:18px;padding:1rem 1.05rem;min-height:115px}.path-num{color:#6366f1;font-size:.65rem;font-weight:800;letter-spacing:.08em}.path-title{font-weight:800;color:#111827;margin:.25rem 0}.path-text{color:#667085;font-size:.76rem;line-height:1.5}
.focus-shell{background:#fff;border:1px solid #e5e7eb;border-radius:24px;padding:1.4rem 1.5rem;box-shadow:0 12px 30px rgba(16,24,40,.045);margin-bottom:1rem}.focus-kicker{color:#6366f1;font-size:.65rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.focus-title{font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;letter-spacing:-.05em;color:#111827;margin:.25rem 0}.focus-desc{color:#667085;max-width:760px;line-height:1.6}.nav-caption{color:#98a2b3;font-size:.68rem;line-height:1.45;margin-top:.35rem}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""<div class="brand"><div class="brand-title">◉ Logic<span style="color:#6366f1">IQ</span></div><div class="brand-subtitle">Aptitude learning workspace</div></div>""", unsafe_allow_html=True)
st.sidebar.markdown('<div class="small-muted"><b>YOUR PROGRESS</b></div>', unsafe_allow_html=True)
st.sidebar.metric("Solved", st.session_state.attempts)
st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")
if st.sidebar.button("Reset progress", use_container_width=True):
    reset_progress()
    st.rerun()
st.sidebar.markdown('<div class="nav-caption">Focused on learning, practice and review.</div>', unsafe_allow_html=True)

st.markdown('<div class="topbar"><div class="topbrand">Logic<span>IQ</span></div><div class="small-muted">Logic & Data Interpretation · OE-II</div></div>', unsafe_allow_html=True)
nav=st.columns(5)
for col,label,value in zip(nav,["⌂  Home","▦  Learn","✦  Practice","◒  Insights","✦  AI Coach"],["Home","Learn","Practice","Insights","AI Coach"]):
    with col:
        if st.button(label,key=f"nav_{value}",use_container_width=True,type="primary" if st.session_state.view==value else "secondary"):
            st.session_state.view=value
            if value!="Learn": st.session_state.topic=None
            st.rerun()

if st.session_state.view=="Home":
    st.markdown('''<div class="hero-premium"><span class="hero-pill">PERSONAL APTITUDE WORKSPACE</span><h2>Build the skill.<br>Then beat the question.</h2><p>LogicIQ turns aptitude preparation into a guided learning experience. Study a concept, see how it works, practise at your level and review exactly where you lost marks.</p></div>''',unsafe_allow_html=True)
    cols=st.columns(4)
    for col,(k,v,s) in zip(cols,[("Topics","8","learning paths"),("Solved",str(st.session_state.attempts),"this session"),("Correct",str(st.session_state.correct),"answers"),("Accuracy",f"{accuracy:.1f}%","current session")]):
        with col: st.markdown(f'<div class="stat-tile"><div class="stat-k">{k}</div><div class="stat-v">{v}</div><div class="stat-s">{s}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><div><h3>Choose your next skill</h3><p>Focused learning paths instead of a module list.</p></div></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(key,info) in enumerate(TOPICS.items()):
        with cols[i%4]:
            st.markdown(f'<div class="topic-card"><div class="topic-symbol">{info["icon"]}</div><div class="topic-eyebrow">{info["eyebrow"]}</div><div class="topic-title">{info["title"]}</div><div class="topic-desc">{info["desc"]}</div></div>',unsafe_allow_html=True)
            if st.button(f"Open {info['title']}",key=f"home_{key}",use_container_width=True):
                st.session_state.view="Learn"; st.session_state.topic=key; st.rerun()
    st.markdown('<div class="section-head"><div><h3>Your learning loop</h3><p>Built for placement and competitive aptitude preparation.</p></div></div>',unsafe_allow_html=True)
    for col,(n,t,x) in zip(st.columns(4),[("01","Understand","Learn the idea before touching the timer."),("02","Watch","Follow worked examples and methods."),("03","Solve","Practice from easy to expert."),("04","Review","Use explanations to close gaps.")]):
        with col: st.markdown(f'<div class="path-card"><div class="path-num">{n}</div><div class="path-title">{t}</div><div class="path-text">{x}</div></div>',unsafe_allow_html=True)

elif st.session_state.view=="Learn":
    if not st.session_state.topic:
        st.markdown('<div class="eyebrow">LEARNING LIBRARY</div><div class="display-title">What do you want to master?</div><div class="display-sub">Pick a skill. Each path opens with its own theory, examples, tools and practice.</div>',unsafe_allow_html=True)
        cols=st.columns(2)
        for i,(key,info) in enumerate(TOPICS.items()):
            with cols[i%2]:
                st.markdown(f'<div class="focus-shell"><div class="topic-symbol">{info["icon"]}</div><div class="focus-kicker">{info["eyebrow"]}</div><div class="focus-title">{info["title"]}</div><div class="focus-desc">{info["desc"]}</div></div>',unsafe_allow_html=True)
                if st.button(f"Start learning · {info['title']}",key=f"learn_{key}",use_container_width=True,type="primary"):
                    st.session_state.topic=key; st.rerun()
    else:
        key=st.session_state.topic; info=TOPICS[key]
        st.markdown(f'<div class="focus-shell"><div class="focus-kicker">{info["eyebrow"]} · LEARNING PATH</div><div class="focus-title">{info["title"]}</div><div class="focus-desc">{info["desc"]}</div></div>',unsafe_allow_html=True)
        if st.button("← Back to learning library",key="back_library"):
            st.session_state.topic=None; st.rerun()
        if key=="Clock": clock_page(record_result)
        elif key=="Calendar": calendar_page(record_result)
        elif key=="Patterns": patterns_page(record_result)
        elif key=="Tabular": tabular_page()
        elif key=="Bar Graph": bar_graph_page()
        elif key=="Pie Chart": pie_chart_page()
        elif key=="Line Graph": line_graph_page()
        elif key=="Missing Data": missing_data_page()

elif st.session_state.view=="Practice":
    st.markdown('<div class="eyebrow">PRACTICE ARENA</div><div class="display-title">Train under pressure.</div><div class="display-sub">Generate questions without navigating through separate topic pages.</div>',unsafe_allow_html=True)
    module=st.selectbox("Skill",["Clock","Calendar","Pattern"],label_visibility="collapsed")
    st.select_slider("Difficulty",options=["Easy","Medium","Hard","Expert"],value="Medium")
    if "practice_q" not in st.session_state or st.session_state.get("practice_module")!=module:
        st.session_state.practice_module=module; st.session_state.practice_q=None
    if st.button("Generate question",type="primary",use_container_width=True):
        st.session_state.practice_q=clock_question() if module=="Clock" else calendar_question() if module=="Calendar" else pattern_question()
    q=st.session_state.practice_q
    if q:
        st.markdown(f'<div class="focus-shell"><div class="focus-kicker">{module.upper()} · PRACTICE</div><div class="focus-title">{q["question"]}</div></div>',unsafe_allow_html=True)
        answer=st.number_input("Your answer",value=0.0,step=1.0,key="practice_answer")
        if st.button("Check answer",type="primary"):
            correct=abs(float(answer)-float(q["answer"]))<.01
            record_result(module,correct)
            if correct: st.success("Correct — keep going.")
            else: st.error(f"Not quite. Correct answer: {q['answer']}")
            with st.expander("See the solution",expanded=True): st.write(q["explanation"])

elif st.session_state.view=="Insights":
    st.markdown('<div class="eyebrow">LEARNING INSIGHTS</div><div class="display-title">See how you are improving.</div><div class="display-sub">A clean view of your current practice session.</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    a.metric("Questions",st.session_state.attempts); b.metric("Correct",st.session_state.correct); c.metric("Accuracy",f"{accuracy:.1f}%")
    if st.session_state.module_stats:
        rows=[]
        for m,s in st.session_state.module_stats.items(): rows.append({"Skill":m,"Attempts":s["attempts"],"Correct":s["correct"],"Accuracy":round(s["correct"]/s["attempts"]*100,1) if s["attempts"] else 0})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    else: st.info("Start practicing to build your first insight report.")

elif st.session_state.view=="AI Coach":
    st.markdown('<div class="eyebrow">PERSONAL AI TUTOR</div><div class="display-title">Ask. Understand. Move on.</div><div class="display-sub">Use Gemini for explanations, hints, worked solutions and revision.</div>',unsafe_allow_html=True)
    gemini_page()

st.markdown('<div class="footer">LogicIQ · Learn with structure. Practice with purpose.</div>',unsafe_allow_html=True)
