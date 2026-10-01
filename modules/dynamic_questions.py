"""Procedural aptitude question generators for LogicIQ.
No prebuilt practice questions are used: every generated MCQ is created at runtime.
"""
import calendar as pycalendar
import math
import random
from datetime import date, timedelta

RNG = random.SystemRandom()


def _opts(answer, kind='text', spread=None):
    if kind == 'num':
        a = float(answer)
        if abs(a-round(a)) < 1e-9:
            a = int(round(a))
        candidates = {str(a)}
        if spread is None: spread = max(1, abs(a)*0.1)
        tries = 0
        while len(candidates) < 4 and tries < 100:
            tries += 1
            delta = RNG.choice([-1,1]) * RNG.choice([1,2,3,4,5]) * (1 if spread < 2 else round(spread/5) or 1)
            v = a + delta
            if isinstance(a, int): v = int(round(v))
            candidates.add(str(v))
        while len(candidates) < 4:
            candidates.add(str(a + len(candidates)))
        out = list(candidates); RNG.shuffle(out); return out, str(a)
    candidates = [str(answer)]
    pool = spread or []
    for x in pool:
        if str(x) not in candidates: candidates.append(str(x))
    while len(candidates) < 4:
        candidates.append(f"Option {len(candidates)+1}")
    out = candidates[:4]; RNG.shuffle(out); return out, str(answer)


def _clock_angle(h, m):
    d = abs((h % 12) * 30 + m * .5 - m * 6)
    return min(d, 360-d)


def _fmt_minutes(x):
    total = x % (12*60)
    h = int(total // 60) or 12
    m = total - int(total // 60)*60
    if abs(m-round(m)) < 1e-9: ms = f"{int(round(m)):02d}"
    else: ms = f"{m:.2f}"
    return f"{h}:{ms}"


def generate_clock(difficulty='Medium', qtype='All Question Types'):
    types = [
        'Angle Between Hands','Specified Angle','Coincidence','Opposite Hands','Right Angle',
        'Mirror Clock','Fast Clock','Slow Clock','Two Clocks','Fractional Time','Advanced Mixed'
    ]
    if qtype == 'All Question Types': qtype = RNG.choice(types)
    if qtype not in types: qtype = RNG.choice(types)

    if qtype == 'Angle Between Hands':
        h = RNG.randint(1,11); m = RNG.randint(0,59)
        ans = round(_clock_angle(h,m),2)
        opts, correct = _opts(ans,'num')
        return _clock_mcq(qtype,difficulty,f"What is the smaller angle between the hands at {h}:{m:02d}?",opts,correct,
            f"Minute hand = {m}×6 = {m*6}°. Hour hand = {h}×30 + {m}×0.5 = {h*30+m*.5:.1f}°. Difference = {abs(h*30+m*.5-m*6):.1f}°; take the smaller of this and 360° minus it.","|30H − 5.5M|; smaller = min(θ, 360−θ)","The hour hand moves 0.5° per minute.")

    if qtype == 'Specified Angle':
        target = RNG.choice([10,20,30,45,60,75,90,120,135,150,180])
        h = RNG.randint(0,11)
        # Solve 30h - 5.5m = ±target and choose a valid minute.
        sols=[]
        for sign in (1,-1):
            m=(30*h-sign*target)/5.5
            if 0 <= m < 60: sols.append(m)
        if not sols:
            h=(h+RNG.randint(1,10))%12
            for sign in (1,-1):
                m=(30*h-sign*target)/5.5
                if 0 <= m < 60: sols.append(m)
        m=RNG.choice(sols)
        ans=_fmt_minutes(h*60+m)
        display=f"{h or 12}:{m:04.1f}" if abs(m-round(m))>1e-8 else f"{h or 12}:{int(m):02d}"
        opts,correct=_opts(ans,'text',[f"{_fmt_minutes(h*60+m+5)}",f"{_fmt_minutes(h*60+m-5)}",f"{_fmt_minutes(h*60+m+10)}"])
        return _clock_mcq(qtype,difficulty,f"At what time between {h or 12} and {(h+1) or 12} o'clock will the hands form {target}°?",opts,correct,
            f"Use |30H−5.5M|={target}. For H={h}, one valid solution is M={m:.2f} minutes. Therefore the time is approximately {display}.","|30H − 5.5M| = θ","For specified angles, test both +θ and −θ because the hands can be on either side.")

    if qtype == 'Coincidence':
        h=RNG.randint(0,11); m=60*h/11
        ans=_fmt_minutes(m)
        opts,correct=_opts(ans,'text',[f"{_fmt_minutes(m+5)}",f"{_fmt_minutes(m-5)}",f"{_fmt_minutes(m+10)}"])
        return _clock_mcq(qtype,difficulty,f"Approximately when do the hands coincide between {h or 12} and {(h+1) or 12} o'clock?",opts,correct,
            f"At H o'clock, coincidence occurs after M=60H/11 minutes. For H={h}, M={m:.2f} minutes.","M = 60H/11","There are 11 coincidences in 12 hours and 22 in 24 hours.")

    if qtype == 'Opposite Hands':
        h=RNG.randint(0,11); sols=[]
        for sign in (1,-1):
            m=(30*h-sign*180)/5.5
            if 0<=m<60: sols.append(m)
        if not sols:
            h=(h+6)%12
            for sign in (1,-1):
                m=(30*h-sign*180)/5.5
                if 0<=m<60: sols.append(m)
        m=RNG.choice(sols); ans=_fmt_minutes(h*60+m)
        opts,correct=_opts(ans,'text',[f"{_fmt_minutes(h*60+m+4)}",f"{_fmt_minutes(h*60+m-4)}",f"{_fmt_minutes(h*60+m+8)}"])
        return _clock_mcq(qtype,difficulty,f"When are the hands exactly opposite between {h or 12} and {(h+1) or 12}?",opts,correct,
            f"Set |30H−5.5M|=180. For H={h}, the valid minute value is {m:.2f}.","|30H − 5.5M| = 180","Opposite hands occur 11 times in 12 hours.")

    if qtype == 'Right Angle':
        h=RNG.randint(0,11); target=90; sols=[]
        for sign in (1,-1):
            m=(30*h-sign*target)/5.5
            if 0<=m<60: sols.append(m)
        if not sols:
            h=(h+RNG.randint(1,11))%12
            for sign in (1,-1):
                m=(30*h-sign*target)/5.5
                if 0<=m<60: sols.append(m)
        m=RNG.choice(sols); ans=_fmt_minutes(h*60+m)
        opts,correct=_opts(ans,'text',[f"{_fmt_minutes(h*60+m+6)}",f"{_fmt_minutes(h*60+m-6)}",f"{_fmt_minutes(h*60+m+12)}"])
        return _clock_mcq(qtype,difficulty,f"At what time between {h or 12} and {(h+1) or 12} do the hands make a right angle?",opts,correct,
            f"Set |30H−5.5M|=90. With H={h}, M={m:.2f} minutes gives the required 90° separation.","|30H − 5.5M| = 90","There are 22 right-angle occurrences in 12 hours.")

    if qtype == 'Mirror Clock':
        h=RNG.randint(1,11); m=RNG.randint(0,59)
        actual=h*60+m; ans=_fmt_minutes(720-actual)
        opts,correct=_opts(ans,'text',[f"{_fmt_minutes(720-actual+20)}",f"{_fmt_minutes(720-actual-20)}",f"{_fmt_minutes(720-actual+40)}"])
        return _clock_mcq(qtype,difficulty,f"What is the mirror image time of {h}:{m:02d}?",opts,correct,
            f"Mirror time = 11:60 − actual time. 720 minutes − {actual} minutes = {720-actual} minutes, giving {ans}.","Mirror time = 11:60 − actual time","Use the 12-hour analog mirror shortcut only with the standard clock face.")

    if qtype in ('Fast Clock','Slow Clock'):
        gain = RNG.choice([2,3,5,6,10])
        real = RNG.choice([6,8,10,12,15,20,24])
        signed = gain if qtype=='Fast Clock' else -gain
        shown = real*(60+signed)/60
        delta=shown-real
        mag=abs(delta)
        ans=f"{int(mag//60)} h {int(round(mag%60)):02d} min" if mag>=60 else f"{int(round(mag))} min"
        opts,correct=_opts(ans,'text',[f"{int(mag)+5} min",f"{int(mag)+10} min",f"{int(mag)+15} min"])
        verb='gains' if signed>0 else 'loses'
        return _clock_mcq(qtype,difficulty,f"A clock {verb} {gain} minutes every hour. Over {real} real hours, by how much is its reading different from actual time?",opts,correct,
            f"Rate = {signed} minutes per real hour. Over {real} hours, difference = {real}×{signed} = {delta:.0f} minutes.","Shown/actual rate = (60 ± gain per hour)/60","Always distinguish the rate per real hour from the total accumulated error.")

    if qtype == 'Two Clocks':
        fast=RNG.choice([2,3,4,5]); slow=RNG.choice([1,2,3]);
        rel=fast+slow
        target=RNG.choice([30,60,90,120])
        hours=target/rel
        ans=f"{hours*60:.0f} minutes"
        opts,correct=_opts(ans,'text',[f"{hours*60+10:.0f} minutes",f"{max(1,hours*60-10):.0f} minutes",f"{hours*60+20:.0f} minutes"])
        return _clock_mcq(qtype,difficulty,f"Two clocks are synchronized. One gains {fast} min/hour and the other loses {slow} min/hour. After how long will their readings differ by {target} minutes?",opts,correct,
            f"Relative separation rate = {fast}+{slow}={rel} min/hour. Time = {target}/{rel} hours = {hours*60:.0f} minutes.","Relative rate = sum of gain and loss rates","When two clocks move in opposite directions, add their error rates.")

    if qtype == 'Fractional Time':
        h=RNG.randint(1,11); m=RNG.choice([7.5,12.5,17.5,22.5,27.5,32.5,37.5,42.5,47.5,52.5])
        ans=round(_clock_angle(h,m),2); opts,correct=_opts(ans,'num')
        return _clock_mcq(qtype,difficulty,f"Find the smaller angle at {h}:{m:g}.",opts,correct,
            f"Hour hand = {h}×30 + {m:g}×0.5 = {h*30+m*.5:.2f}°. Minute hand = {m:g}×6 = {m*6:.2f}°. Smaller difference = {ans:.2f}°.","|30H − 5.5M|","Do not round the fractional minute until the final answer.")

    # Advanced mixed: construct a valid multi-step angle problem.
    h=RNG.randint(1,11); m=RNG.randint(0,59); delta=RNG.choice([15,30,45,60])
    a1=_clock_angle(h,m); a2=_clock_angle(h,(m+delta)%60)
    change=round(abs(a2-a1),2); opts,correct=_opts(change,'num')
    return _clock_mcq(qtype,difficulty,f"At {h}:{m:02d} the smaller angle is {a1:.2f}°. After {delta} minutes, by how many degrees does the smaller angle change?",opts,correct,
        f"Recalculate the angle after {delta} minutes. New angle = {a2:.2f}°. Absolute change = |{a2:.2f}−{a1:.2f}| = {change:.2f}°.","θ = min(|30H−5.5M|, 360−|30H−5.5M|)","For advanced questions, calculate both states rather than assuming the angle always increases.")


def _clock_mcq(sub,diff,q,opts,correct,exp,formula,tip):
    return {'category':'Clock','subcategory':sub,'difficulty':diff,'question':q,'options':opts,'correctAnswer':correct,'explanation':exp,'formula':formula,'concept':sub,'examTip':tip,'tags':['clock','aptitude','generated']}


def _is_leap(y): return y%400==0 or (y%4==0 and y%100!=0)

def _weekday_name(d): return d.strftime('%A')


def generate_calendar(difficulty='Medium', qtype='All Question Types'):
    types=['Day of Week','Day Offset','Days Between Dates','Date Addition','Leap Year','Odd Days','Same Calendar','Century Rule','400-Year Cycle','Birthday/Age','Month-Day','Advanced Mixed']
    if qtype=='All Question Types': qtype=RNG.choice(types)
    if qtype not in types: qtype=RNG.choice(types)

    if qtype=='Day of Week':
        y=RNG.randint(1950,2099); m=RNG.randint(1,12); d=RNG.randint(1,pycalendar.monthrange(y,m)[1]); dt=date(y,m,d); ans=_weekday_name(dt)
        opts,correct=_opts(ans,'text',[x for x in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] if x!=ans])
        return _cal_mcq(qtype,difficulty,f"What day of the week was {dt.strftime('%d %B %Y')}?",opts,correct,f"Using the Gregorian calendar, {dt.strftime('%d %B %Y')} falls on {ans}.","Gregorian weekday calculation / modulo 7","Reduce date offsets modulo 7; for historical dates use the stated calendar convention.")

    if qtype=='Day Offset':
        y=RNG.randint(2020,2035); m=RNG.randint(1,12); d=RNG.randint(1,pycalendar.monthrange(y,m)[1]); base=date(y,m,d); n=RNG.randint(-500,500); target=base+timedelta(days=n); ans=_weekday_name(target)
        opts,correct=_opts(ans,'text',[x for x in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] if x!=ans])
        direction='after' if n>=0 else 'before'; mag=abs(n)
        return _cal_mcq(qtype,difficulty,f"If {base.strftime('%d %B %Y')} is a {base.strftime('%A')}, what day is {mag} days {direction}?",opts,correct,f"Only n mod 7 matters. {n} mod 7 = {n%7}. Therefore the target date is {target.strftime('%A')}.","Day shift = N mod 7","For large offsets, reduce the number of days modulo 7 first.")

    if qtype=='Days Between Dates':
        y1=RNG.randint(2000,2028); y2=RNG.randint(y1,y1+8); m1=RNG.randint(1,12); d1=RNG.randint(1,pycalendar.monthrange(y1,m1)[1]); start=date(y1,m1,d1)
        end=date(y2,RNG.randint(1,12),1); end=end.replace(day=RNG.randint(1,pycalendar.monthrange(end.year,end.month)[1]));
        if end<start: start,end=end,start
        ans=(end-start).days; opts,correct=_opts(ans,'num',spread=20)
        return _cal_mcq(qtype,difficulty,f"How many days are there between {start.strftime('%d %B %Y')} and {end.strftime('%d %B %Y')}?",opts,correct,f"Subtract the earlier date from the later date. The elapsed-day count is {ans} days. The starting date itself is not counted as an elapsed day.","Date difference = later date − earlier date","Clarify whether a question asks elapsed days or inclusive counting before calculating.")

    if qtype=='Date Addition':
        y=RNG.randint(2020,2035); m=RNG.randint(1,12); d=RNG.randint(1,pycalendar.monthrange(y,m)[1]); base=date(y,m,d); n=RNG.randint(10,800); target=base+timedelta(days=n); ans=target.strftime('%d %B %Y')
        opts,correct=_opts(ans,'text',[ (target+timedelta(days=x)).strftime('%d %B %Y') for x in (-7,7,14)])
        return _cal_mcq(qtype,difficulty,f"What date is {n} days after {base.strftime('%d %B %Y')}?",opts,correct,f"Add {n} elapsed days to the starting date. The resulting date is {ans}.","Target date = start date + N days","Move month by month only when necessary; date arithmetic is less error-prone with modulo and exact day counts.")

    if qtype=='Leap Year':
        y=RNG.choice([RNG.randint(1900,2399),1900,2000,2100,2200,2300,2400]); ans='Yes' if _is_leap(y) else 'No'
        opts,correct=_opts(ans,'text',['Yes','No','Only in century years','Cannot be determined'])
        return _cal_mcq(qtype,difficulty,f"Is {y} a Gregorian leap year?",opts,correct,f"{y}%400={y%400}, {y}%100={y%100}, {y}%4={y%4}. The rule gives {'a leap year' if _is_leap(y) else 'a non-leap year'}.","Leap iff divisible by 4, except centuries must be divisible by 400","Remember: 1900 is not leap, 2000 is leap, 2100 is not leap.")

    if qtype=='Odd Days':
        years=RNG.randint(1,400); leaps=sum(1 for y in range(2001,2001+years) if _is_leap(y)); total=years*365+leaps; ans=total%7
        opts,correct=_opts(ans,'num');
        return _cal_mcq(qtype,difficulty,f"How many odd days are there in the {years}-year period from 2001 up to the end of {2000+years}?",opts,correct,f"Total days = {years}×365 + {leaps} leap day(s) = {total}. Divide by 7; remainder = {ans} odd day(s).","Odd days = total days mod 7","Do not assume every 4-year block is identical across century years.")

    if qtype=='Same Calendar':
        y=RNG.randint(2001,2030); target=y+1
        while True:
            if _is_leap(target)==_is_leap(y) and date(target,1,1).weekday()==date(y,1,1).weekday(): break
            target+=1
        ans=str(target); opts,correct=_opts(ans,'text',[str(target-1),str(target+1),str(target+2)])
        return _cal_mcq(qtype,difficulty,f"What is the next year after {y} that has the same Gregorian calendar as {y}?",opts,correct,f"A same calendar needs the same leap/non-leap status and the same weekday for January 1. The first year satisfying both is {target}.","Same calendar: same year type + same Jan 1 weekday","A 28-year shortcut can fail around century exceptions; verify the actual weekday and leap status.")

    if qtype=='Century Rule':
        y=RNG.choice([1700,1800,1900,2000,2100,2200,2300,2400]); ans='Leap year' if _is_leap(y) else 'Not a leap year'
        opts,correct=_opts(ans,'text',['Leap year','Not a leap year','Depends on February','Only if divisible by 4'])
        return _cal_mcq(qtype,difficulty,f"Under the Gregorian rule, is {y} a leap year?",opts,correct,f"Century years are leap years only when divisible by 400. {y}%400={y%400}, so the result is {ans.lower()}.","Century leap rule: divisible by 400","The century exception is the most common calendar trap.")

    if qtype=='400-Year Cycle':
        ans=146097%7
        opts,correct=_opts(ans,'num')
        return _cal_mcq(qtype,difficulty,"How many odd days are there in a complete Gregorian 400-year cycle?",opts,correct,"A Gregorian 400-year cycle contains 97 leap years and 303 normal years: 97×366 + 303×365 = 146097 days. 146097 is divisible by 7, so the remainder is 0.","400-year cycle = 146097 days = 0 odd days","The Gregorian calendar repeats its weekday pattern every 400 years.")

    if qtype=='Birthday/Age':
        y=RNG.randint(1990,2010); m=RNG.randint(1,12); d=RNG.randint(1,pycalendar.monthrange(y,m)[1]); birth=date(y,m,d); years=RNG.randint(10,30); target=date(y+years,m,d); ans=_weekday_name(target)
        opts,correct=_opts(ans,'text',[x for x in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] if x!=ans])
        return _cal_mcq(qtype,difficulty,f"A person was born on {birth.strftime('%d %B %Y')}. What day of the week falls on their {years}-year birthday in {target.year}?",opts,correct,f"Add {years} calendar years while keeping the same month/day. {target.strftime('%d %B %Y')} is a {ans}.","Weekday = date calculation mod 7","For leap-day birthdays, state the convention if the target year is not leap.")

    if qtype=='Month-Day':
        y=RNG.randint(2020,2032); m=RNG.randint(1,12); days=pycalendar.monthrange(y,m)[1]; ans=days
        opts,correct=_opts(ans,'num')
        return _cal_mcq(qtype,difficulty,f"How many days does {date(y,m,1).strftime('%B')} have in {y}?",opts,correct,f"{date(y,m,1).strftime('%B')} has {days} days in {y}. February is the only month whose length changes with leap years.","Month-day table","Check February separately; all other month lengths are fixed.")

    # Advanced mixed: date offset across a leap boundary.
    y=RNG.randint(2010,2030); base=date(y,12,31); n=RNG.randint(30,450); target=base+timedelta(days=n); ans=_weekday_name(target)
    opts,correct=_opts(ans,'text',[x for x in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] if x!=ans])
    return _cal_mcq(qtype,difficulty,f"Starting from {base.strftime('%d %B %Y')}, what weekday is {n} days later?",opts,correct,f"Move exactly {n} days across the year boundary, accounting for leap years. The target date is {target.strftime('%d %B %Y')}, a {ans}.","Date arithmetic + modulo 7","Advanced date questions often cross February or a year boundary, so count leap days carefully.")


def _cal_mcq(sub,diff,q,opts,correct,exp,formula,tip):
    return {'category':'Calendar','subcategory':sub,'difficulty':diff,'question':q,'options':opts,'correctAnswer':correct,'explanation':exp,'formula':formula,'concept':sub,'examTip':tip,'tags':['calendar','aptitude','generated']}
