# LogicIQ – Logic & Data Interpretation Learning System

A Python + Streamlit educational application for the Logic and Data Interpretation – II (OE-II) case study.

## Implemented modules
1. Clock Problems
2. Calendar Problems
3. Figures & Pattern Recognition
4. Tabular Data Interpretation
5. Bar Graph Analysis
6. Pie Chart Analysis
7. Line Graph Analysis
8. Missing Data Interpretation

Additional features:
- Interactive dashboard
- Practice mode with randomized questions
- Automatic scoring
- Explanations
- Data visualization
- CSV upload for tabular data
- Input validation
- Session performance tracking

## Run
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
streamlit run app.py
```

The application opens at:
http://localhost:8501


## Clock & Calendar Learning System (v2.0)
The Clock and Calendar modules now include:
- Large analog clock visualization with continuously moving hour/minute/second hands.
- Complete exam-oriented theory, definitions, formulas, derivations, shortcuts, common mistakes and exam tips.
- 20 solved examples per topic with step-by-step solutions.
- 200 application-ready MCQs: 100 Clock + 100 Calendar.
- Difficulty distribution for each topic: 30 Easy, 30 Medium, 25 Hard, 15 Expert.
- Exactly four options per MCQ and one correct answer.
- Immediate answer checking with explanation, formula and exam tip.
- Content is stored in `data/clock_calendar_content.json` for easy reuse/export.
- Existing calculator and Practice Center interfaces remain available.


## New Learning + AI Features

- Every syllabus module now contains an in-app theory section with core concepts, formulas, examples, common mistakes, and exam tips.
- Clock and Calendar include the full structured learning system and 200 validated MCQs (100 each).
- The Clock module includes a large live analog clock visualization.
- Gemini AI Tutor is available from the sidebar. Set `GEMINI_API_KEY` as an environment variable or enter a key in the AI Tutor page.
- The AI Tutor uses Google's current `google-genai` Python SDK and a configurable Gemini model.

## Dynamic Practice Engine
Clock and Calendar practice no longer reads a fixed question bank. Each time **Generate New Question** is pressed, LogicIQ procedurally creates a new MCQ with four options, a verified answer, explanation, formula, and exam tip. Difficulty and question type can be selected independently.

Clock types include angle, specified angle, coincidence, opposite hands, right angle, mirror clock, fast/slow clocks, two clocks, fractional time, and advanced mixed problems.
Calendar types include day of week, day offset, date difference, date addition, leap year, odd days, same calendar, century rules, 400-year cycle, birthday/age, month-day, and advanced mixed problems.
