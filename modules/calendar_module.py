from modules.theory import show_module_theory
from modules.dynamic_questions import generate_calendar
import streamlit as st
from datetime import date, timedelta
import calendar
import random
import json
import os
import pandas as pd

_CONTENT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "clock_calendar_content.json")

@st.cache_data
def load_clock_calendar_content():
    with open(_CONTENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def calendar_question():
    """Generate a fresh numeric Calendar question for Practice Center."""
    q=generate_calendar(random.choice(["Easy","Medium","Hard","Expert"]),"Day Offset")
    # Preserve the old numeric Practice Center interface. Use weekday number.
    import datetime as _dt
    base=_dt.date(random.randint(2024,2032),random.randint(1,12),1)
    last=calendar.monthrange(base.year,base.month)[1]
    base=base.replace(day=random.randint(1,last))
    offset=random.randint(-500,500)
    target=base+timedelta(days=offset)
    return {"question":f"What is the weekday number of {target.strftime('%d %B %Y')}? (Monday=0)","answer":target.weekday(),"explanation":f"The generated date is {target.strftime('%d %B %Y')}, which is {target.strftime('%A')}. Monday=0 gives {target.weekday()}."}


def _show_theory(topic):
    st.subheader("📘 Learn")
    for item in topic["theory"]:
        with st.expander(f"{item['title']} · {item['level']}"):
            st.markdown(item["theory"])
            st.markdown("**Formulas**")
            for x in item["formulas"]: st.markdown(f"- {x}")
            st.markdown("**Quick shortcuts**")
            for x in item["shortcuts"]: st.markdown(f"- {x}")
            if item.get("examples"):
                st.markdown("**Example**")
                for ex in item["examples"]:
                    st.markdown(f"**Question:** {ex['question']}")
                    st.markdown(f"**Solution:** {ex['solution']}")
                    st.markdown(f"**Answer:** {ex['answer']}")
            st.markdown("**Common mistakes**")
            for x in item["commonMistakes"]: st.markdown(f"- {x}")
            st.markdown("**Exam tips**")
            for x in item["examTips"]: st.markdown(f"- {x}")

def _show_reference(topic):
    c1,c2=st.columns(2)
    with c1:
        st.subheader("🧮 Formula Sheet")
        for f in topic["formulas"]: st.markdown(f"- `{f}`")
    with c2:
        st.subheader("⚡ Quick Tricks")
        for s in topic["shortcuts"]: st.markdown(f"- {s}")

def _show_examples(topic):
    st.subheader("📝 20 Solved Examples")
    for i,ex in enumerate(topic["solvedExamples"],1):
        with st.expander(f"{i:02d}. {ex['question']}"):
            st.markdown(f"**Concept:** {ex['concept']}")
            st.markdown(f"**Formula:** `{ex['formula']}`")
            st.markdown(f"**Step 1:** {ex['step1']}")
            st.markdown(f"**Step 2:** {ex['step2']}")
            st.markdown(f"**Step 3:** {ex['step3']}")
            st.success(f"Final Answer: {ex['answer']}")
            st.info(f"Exam Tip: {ex['examTip']}")

def _practice_bank(topic, record_result):
    st.subheader("🎯 Infinite Mixed Practice")
    st.caption("Every question is generated at runtime. Mixed Practice automatically rotates through different question types and avoids repeating the recent types.")
    difficulties=["Easy","Medium","Hard","Expert"]
    types=["All Question Types","Day of Week","Day Offset","Days Between Dates","Date Addition","Leap Year","Odd Days","Same Calendar","Century Rule","400-Year Cycle","Birthday/Age","Month-Day","Advanced Mixed"]
    c1,c2=st.columns(2)
    with c1:
        difficulty=st.selectbox("Difficulty",difficulties,key="calendar_difficulty_dynamic")
    with c2:
        qtype=st.selectbox("Question Type",types,key="calendar_type_dynamic")

    if st.button("✨ Generate New Question",type="primary",use_container_width=True,key="calendar_generate"):
        # Mixed Practice rotates across different calendar concepts instead of
        # repeatedly producing the same type.
        if qtype == "All Question Types":
            all_types = [
                "Day of Week","Day Offset","Days Between Dates","Date Addition",
                "Leap Year","Odd Days","Same Calendar","Century Rule",
                "400-Year Cycle","Birthday/Age","Month-Day","Advanced Mixed"
            ]
            recent = st.session_state.get("Calendar_recent_types", [])
            available = [t for t in all_types if t not in recent[-4:]] or [t for t in all_types if t != (recent[-1] if recent else None)]
            selected_type = random.choice(available)
            q = generate_calendar(difficulty, selected_type)
            recent.append(selected_type)
            st.session_state["Calendar_recent_types"] = recent[-4:]
        else:
            q = generate_calendar(difficulty,qtype)
        st.session_state["Calendar_dynamic_q"] = q
        st.session_state["Calendar_dynamic_answer"] = None
        st.session_state.pop("Calendar_dynamic_choice", None)

    q=st.session_state.get("Calendar_dynamic_q")
    if not q:
        st.info("Choose a difficulty and question type, then click **Generate New Question**.")
        return

    st.caption(f"Generated now · {q['subcategory']} · {q['difficulty']}")
    st.markdown(f"### {q['question']}")
    choice=st.radio("Choose one answer",q["options"],key="Calendar_dynamic_choice")
    if st.button("Check Answer",type="primary",key="Calendar_dynamic_check"):
        ok=choice==q["correctAnswer"]
        record_result("Calendar",ok)
        if ok: st.success("✅ Correct")
        else: st.error(f"❌ Incorrect. Correct answer: {q['correctAnswer']}")
        with st.expander("Step-by-step explanation",expanded=True):
            st.write(q["explanation"])
            st.markdown(f"**Formula:** `{q['formula']}`")
            st.markdown(f"**Exam Tip:** {q['examTip']}")


def calendar_page(record_result):
    data=load_clock_calendar_content()["topics"]["calendar"]
    st.title("📅 Calendar Problems")
    st.write("Master weekdays, leap years, odd days, date differences and advanced calendar reasoning.")

    show_module_theory('Calendar Problems')

    with st.expander("📆 Month-Day Reference",expanded=True):
        df=pd.DataFrame({
            "Month":["January","February","March","April","May","June","July","August","September","October","November","December"],
            "Days":["31","28 / 29","31","30","31","30","31","31","30","31","30","31"]
        })
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.info("Gregorian leap-year rule: divisible by 4, except century years unless divisible by 400.")

    d=st.date_input("Select a date",value=date(2026,1,1),key="cal_date_main")
    st.success(f"**{d.strftime('%d %B %Y')}** is a **{d.strftime('%A')}**.")
    n=st.number_input("Days to add (negative = subtract)",min_value=-3650,max_value=3650,value=100,step=1,key="cal_offset_main")
    result=d+timedelta(days=int(n))
    st.info(f"Date after {n} days: **{result.strftime('%d %B %Y (%A)')}**")

    st.subheader("📆 Month Calendar")
    year=st.number_input("Year",min_value=1900,max_value=2100,value=d.year,key="cal_year")
    month=st.number_input("Month",min_value=1,max_value=12,value=d.month,key="cal_month")
    cal_data=calendar.monthcalendar(int(year),int(month))
    df=pd.DataFrame(cal_data,columns=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    st.dataframe(df,use_container_width=True,hide_index=True)

    st.divider()
    st.header("1. THEORY")
    _show_theory(data)
    st.divider()
    st.header("2. FORMULAS & SHORTCUTS")
    _show_reference(data)
    st.divider()
    st.header("3. SOLVED EXAMPLES")
    _show_examples(data)
    st.divider()
    st.header("4. PRACTICE QUESTION BANK")
    _practice_bank(data,record_result)
