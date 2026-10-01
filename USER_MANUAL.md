# LogicIQ User Manual

## 1. Start the application
Open a terminal in the project folder and run:

`streamlit run app.py`

## 2. Dashboard
The dashboard shows:
- number of modules
- questions attempted
- correct answers
- accuracy
- per-module performance

## 3. Logic modules
### Clock
Enter hour and minute to calculate the smaller angle between clock hands.

### Calendar
Select a date, calculate its weekday and add/subtract days.

### Pattern Recognition
Generate numerical pattern questions and submit an answer.

## 4. Data Interpretation modules
### Tabular DI
Edit the table or upload a CSV. The application calculates descriptive statistics and percentage change.

### Bar Graph
Edit categories and values to generate a bar graph and contribution percentages.

### Pie Chart
Edit category values to calculate percentage contribution and sector angles.

### Line Graph
Edit periods and values to inspect trends and period-to-period changes.

### Missing Data
Use known totals and known values to calculate an unknown value.

## 5. Practice Center
Generate randomized Clock, Calendar and Pattern questions. Submit answers and view explanations.

## 6. Reset
Use the sidebar's Reset Progress button to clear the current session's practice statistics.


### Clock & Calendar Learning System
Open **Clock Problems** or **Calendar Problems**. Each module presents its interactive calculator/reference first, followed by:
1. Theory
2. Formula & shortcut sheet
3. 20 solved examples
4. Practice Question Bank

The Question Bank supports **All, Easy, Medium, Hard and Expert** difficulty levels. After submitting an answer, LogicIQ displays the correct answer, explanation, formula and exam tip.


## Gemini AI Tutor
1. Install dependencies with `pip install -r requirements.txt`.
2. Set `GEMINI_API_KEY` in your environment, or open **🤖 Gemini AI Tutor** and enter the key for the current session.
3. Select a module and choose Explain, Hint, Step-by-step Solve, Practice Questions, Solution Check, or Revision Notes.
4. Click **Ask Gemini**.

The AI feature is optional; all normal LogicIQ modules work without a Gemini key.
