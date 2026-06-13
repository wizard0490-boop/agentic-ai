import streamlit as st
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import init_db, get_profile, get_medications, get_fitness_logs, get_vitals
from utils.health_data import get_bmi_info, HEALTH_TIPS
import random

def show():
    init_db()
    profile = get_profile()
    today = date.today()

    st.title(" Dashboard")
    name = profile.get("name", "Friend")
    st.subheader(f"Namaste, {name}! ")
    st.caption(f"Today: {today.strftime('%A, %d %B %Y')}")

    # ── Top metrics ───────────────────────────────────────────────────────────
    meds = get_medications()
    fitness = get_fitness_logs(days=1)
    vitals = get_vitals(days=1)
    today_fitness = fitness[0] if fitness and fitness[0]["date"] == str(today) else {}
    today_vitals = vitals[0] if vitals and vitals[0]["date"] == str(today) else {}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(" Active Meds", len(meds))
    with c2:
        steps = today_fitness.get("steps", 0)
        st.metric(" Steps Today", f"{steps:,}", delta=f"{steps-8000:+,} vs 8K goal" if steps else None)
    with c3:
        water = today_fitness.get("water_ml", 0)
        target_water = int(profile.get("weight_kg", 60) * 35) if profile else 2100
        st.metric(" Water (ml)", f"{water}", delta=f"{water-target_water:+} vs target" if water else None)
    with c4:
        bp = f"{today_vitals.get('bp_systolic','—')}/{today_vitals.get('bp_diastolic','—')}" if today_vitals else "—"
        st.metric("❤️ Blood Pressure", bp)

    st.divider()

    # ── BMI card ──────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.subheader(" Health Summary")
        if profile:
            w, h = profile.get("weight_kg"), profile.get("height_cm")
            if w and h:
                bmi, cat, icon = get_bmi_info(w, h)
                st.markdown(f"""
                <div class="metric-card">
                    <strong>BMI:</strong> {bmi} {icon} <em>{cat}</em><br>
                    <strong>Weight:</strong> {w} kg &nbsp; <strong>Height:</strong> {h} cm<br>
                    <strong>Blood Group:</strong> {profile.get('blood_group','—')}<br>
                    <strong>Age:</strong> {profile.get('age','—')} | <strong>Gender:</strong> {profile.get('gender','—')}
                </div>
                """, unsafe_allow_html=True)
            conditions = profile.get("conditions", "")
            if conditions:
                st.markdown(f"**Conditions:** `{conditions}`")
        else:
            st.info(" Please set up your profile to see health summary.")

    with col_right:
        st.subheader(" Today's Medications")
        if meds:
            for med in meds[:5]:
                times = med.get("times", "")
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{med['name']}</strong> – {med['dosage']}<br>
                    <small> {times} &nbsp;|&nbsp; {med['frequency']}</small>
                </div>
                """, unsafe_allow_html=True)
            if len(meds) > 5:
                st.caption(f"+ {len(meds)-5} more — see Medication Tracker")
        else:
            st.info("No active medications. Add them in  Medication Tracker.")

    st.divider()

    # ── Health tip of the day ─────────────────────────────────────────────────
    st.subheader(" Health Tip of the Day")
    tip = HEALTH_TIPS[today.timetuple().tm_yday % len(HEALTH_TIPS)]
    st.success(tip)

    # ── Recent vitals ─────────────────────────────────────────────────────────
    recent_vitals = get_vitals(days=7)
    if recent_vitals:
        st.subheader(" Recent Vitals (Last 7 Days)")
        import pandas as pd
        df = pd.DataFrame(recent_vitals)
        display_cols = [c for c in ["date","bp_systolic","bp_diastolic","heart_rate","blood_sugar","weight_kg"] if c in df.columns]
        df = df[display_cols].rename(columns={
            "date": "Date", "bp_systolic": "BP Sys", "bp_diastolic": "BP Dia",
            "heart_rate": "Heart Rate", "blood_sugar": "Blood Sugar (mg/dL)", "weight_kg": "Weight (kg)"
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Quick log ─────────────────────────────────────────────────────────────
    st.subheader("⚡ Quick Log Today's Vitals")
    with st.expander("Log vitals now"):
        v1, v2, v3, v4 = st.columns(4)
        bp_sys = v1.number_input("BP Systolic", 80, 200, 120)
        bp_dia = v2.number_input("BP Diastolic", 50, 130, 80)
        hr = v3.number_input("Heart Rate", 40, 200, 72)
        sugar = v4.number_input("Blood Sugar (mg/dL)", 50, 500, 100)
        if st.button("Save Vitals"):
            from utils.db import log_vitals
            log_vitals(str(today), bp_sys, bp_dia, hr, sugar)
            st.success("✅ Vitals saved!")
            st.rerun()
