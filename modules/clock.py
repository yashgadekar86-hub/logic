from modules.theory import show_module_theory
from modules.dynamic_questions import generate_clock
import streamlit as st
import random
import math
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

_CONTENT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "clock_calendar_content.json")

@st.cache_data
def load_clock_calendar_content():
    with open(_CONTENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def clock_angle(hour, minute):
    h = hour % 12
    minute_angle = minute * 6
    hour_angle = h * 30 + minute * 0.5
    diff = abs(hour_angle - minute_angle)
    return min(diff, 360 - diff)

def clock_question():
    """Generate a fresh numeric Clock question for Practice Center."""
    q=generate_clock(random.choice(["Easy","Medium","Hard","Expert"]),"Angle Between Hands")
    try: ans=float(str(q["correctAnswer"]).replace("°",""))
    except ValueError: ans=0.0
    return {"question":q["question"],"answer":ans,"explanation":q["explanation"]}


def _draw_big_clock():
    now = datetime.now()
    h = now.hour % 12
    m = now.minute
    s = now.second
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_aspect("equal")
    ax.set_xlim(-1.18,1.18); ax.set_ylim(-1.18,1.18)
    ax.axis("off")
    circle=plt.Circle((0,0),1,fill=False,linewidth=3)
    ax.add_patch(circle)
    # ticks and numbers
    for i in range(60):
        ang=math.radians(90-i*6)
        r1=0.93 if i%5 else 0.86
        r2=0.98
        ax.plot([r1*math.cos(ang),r2*math.cos(ang)],[r1*math.sin(ang),r2*math.sin(ang)],
                linewidth=2 if i%5==0 else 0.7)
    for n in range(1,13):
        ang=math.radians(90-n*30)
        ax.text(0.76*math.cos(ang),0.76*math.sin(ang),str(n),
                ha="center",va="center",fontsize=18,fontweight="bold")
    # hands
    for value, length, width in [
        (h*30+m*0.5,0.55,7),
        (m*6+s*0.1,0.78,5),
        (s*6,0.86,2)
    ]:
        ang=math.radians(90-value)
        ax.plot([0,length*math.cos(ang)],[0,length*math.sin(ang)],linewidth=width,solid_capstyle="round")
    ax.scatter([0],[0],s=80,zorder=5)
    ax.text(0,-1.10,now.strftime("%I:%M:%S %p"),ha="center",va="center",fontsize=16,fontweight="bold")
    return fig

def _show_theory(topic):
    st.subheader("📘 Learn")
    for item in topic["theory"]:
        with st.expander(f"{item['title']} · {item['level']}"):
            st.markdown(item["theory"])
            st.markdown("**Formulas**")
            for x in item["formulas"]:
                st.markdown(f"- {x}")
            st.markdown("**Quick shortcuts**")
            for x in item["shortcuts"]:
                st.markdown(f"- {x}")
            if item.get("examples"):
                st.markdown("**Example**")
                for ex in item["examples"]:
                    st.markdown(f"**Question:** {ex['question']}")
                    st.markdown(f"**Solution:** {ex['solution']}")
                    st.markdown(f"**Answer:** {ex['answer']}")
            st.markdown("**Common mistakes**")
            for x in item["commonMistakes"]:
                st.markdown(f"- {x}")
            st.markdown("**Exam tips**")
            for x in item["examTips"]:
                st.markdown(f"- {x}")

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

def _practice_bank(topic, record_result, module_name):
    st.subheader("🎯 Infinite Mixed Practice")
    st.caption("Every question is generated at runtime. Mixed Practice automatically rotates through different question types and avoids repeating the recent types.")
    difficulties=["Easy","Medium","Hard","Expert"]
    types=["All Question Types","Angle Between Hands","Specified Angle","Coincidence","Opposite Hands","Right Angle","Mirror Clock","Fast Clock","Slow Clock","Two Clocks","Fractional Time","Advanced Mixed"]
    c1,c2=st.columns(2)
    with c1:
        difficulty=st.selectbox("Difficulty",difficulties,key=f"{module_name}_difficulty_dynamic")
    with c2:
        qtype=st.selectbox("Question Type",types,key=f"{module_name}_type_dynamic")

    if st.button("✨ Generate New Question",type="primary",use_container_width=True,key=f"{module_name}_generate"):
        # Mixed Practice must not repeat the same question type consecutively.
        if qtype == "All Question Types":
            all_types = [
                "Angle Between Hands","Specified Angle","Coincidence","Opposite Hands",
                "Right Angle","Mirror Clock","Fast Clock","Slow Clock","Two Clocks",
                "Fractional Time","Advanced Mixed"
            ]
            recent = st.session_state.get(f"{module_name}_recent_types", [])
            available = [t for t in all_types if t not in recent[-4:]] or [t for t in all_types if t != (recent[-1] if recent else None)]
            selected_type = random.choice(available)
            q = generate_clock(difficulty, selected_type)
            recent.append(selected_type)
            st.session_state[f"{module_name}_recent_types"] = recent[-4:]
        else:
            q = generate_clock(difficulty,qtype)
        st.session_state[f"{module_name}_dynamic_q"] = q
        st.session_state[f"{module_name}_dynamic_answer"] = None
        # Clear the previous radio selection so every generated question starts fresh.
        st.session_state.pop(f"{module_name}_dynamic_choice", None)

    q=st.session_state.get(f"{module_name}_dynamic_q")
    if not q:
        st.info("Choose a difficulty and question type, then click **Generate New Question**.")
        return

    st.caption(f"Generated now · {q['subcategory']} · {q['difficulty']}")
    st.markdown(f"### {q['question']}")
    choice=st.radio("Choose one answer",q["options"],key=f"{module_name}_dynamic_choice")
    if st.button("Check Answer",type="primary",key=f"{module_name}_dynamic_check"):
        ok=choice==q["correctAnswer"]
        record_result(module_name,ok)
        if ok: st.success("✅ Correct")
        else: st.error(f"❌ Incorrect. Correct answer: {q['correctAnswer']}")
        with st.expander("Step-by-step explanation",expanded=True):
            st.write(q["explanation"])
            st.markdown(f"**Formula:** `{q['formula']}`")
            st.markdown(f"**Exam Tip:** {q['examTip']}")


def clock_page(record_result):
    data=load_clock_calendar_content()["topics"]["clock"]
    st.title("⏰ Clock Problems")
    st.write("Learn clock reasoning from fundamentals to expert aptitude problems.")

    show_module_theory('Clock Problems')

    st.markdown("### 🕐 Live Analog Clock")
    st.caption("Large visual clock for understanding hand movement. The second hand and hour hand move continuously.")
    fig=_draw_big_clock()
    st.pyplot(fig,use_container_width=False)
    plt.close(fig)

    hcol,mcol=st.columns(2)
    with hcol:
        hour=st.number_input("Hour (1–12)",min_value=1,max_value=12,value=3,key="clock_hour_calc")
    with mcol:
        minute=st.number_input("Minute (0–59)",min_value=0,max_value=59,value=30,key="clock_min_calc")
    if st.button("Calculate Angle",type="primary"):
        ans=clock_angle(hour,minute)
        st.success(f"Smaller angle = **{ans:.2f}°**")
        st.write(f"Hour hand position = {((hour%12)*30+minute*.5):.2f}°")
        st.write(f"Minute hand position = {minute*6:.2f}°")

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
    _practice_bank(data,record_result,"Clock")
