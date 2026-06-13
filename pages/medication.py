import streamlit as st
import google.generativeai as genai
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import init_db, add_medication, get_medications, log_medication, get_adherence_rate, delete_medication
from utils.health_data import COMMON_MEDICATIONS, MEDICATION_TIMES

def show():
    init_db()
    st.title(" Medication Tracker")
    st.caption("Track your daily medications and set reminders")

    tab1, tab2, tab3 = st.tabs([" My Medications", "➕ Add Medication", " Medicine Info"])

    # ── Tab 1: My Medications ─────────────────────────────────────────────────
    with tab1:
        meds = get_medications()
        if not meds:
            st.info("No medications added yet. Use the '➕ Add Medication' tab.")
        else:
            for med in meds:
                adh = get_adherence_rate(med["id"])
                adh_color = "🟢" if adh >= 80 else "🟡" if adh >= 50 else ""

                with st.expander(f" {med['name']} – {med['dosage']} | {adh_color} {adh}% adherence"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**Frequency:** {med['frequency']}")
                    c1.write(f"**Times:** {med['times']}")
                    c2.write(f"**Start Date:** {med['start_date']}")
                    c2.write(f"**End Date:** {med['end_date'] or 'Ongoing'}")
                    if med.get("notes"):
                        st.write(f"**Notes:** {med['notes']}")

                    col_a, col_b, col_c = st.columns(3)
                    if col_a.button("✅ Mark Taken", key=f"taken_{med['id']}"):
                        log_medication(med["id"], "taken")
                        st.success("Logged as taken!")
                        st.rerun()
                    if col_b.button("❌ Missed", key=f"miss_{med['id']}"):
                        log_medication(med["id"], "missed")
                        st.warning("Logged as missed.")
                        st.rerun()
                    if col_c.button("️ Remove", key=f"del_{med['id']}"):
                        delete_medication(med["id"])
                        st.success("Removed.")
                        st.rerun()

            # Adherence summary
            st.divider()
            st.subheader(" 7-Day Adherence Summary")
            import pandas as pd
            rows = []
            for med in meds:
                rows.append({
                    "Medication": med["name"],
                    "Dosage": med["dosage"],
                    "Adherence (7d)": f"{get_adherence_rate(med['id'])}%"
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Tab 2: Add Medication ─────────────────────────────────────────────────
    with tab2:
        st.subheader("Add a New Medication")
        with st.form("add_med_form"):
            name = st.text_input("Medicine Name *", placeholder="e.g. Metformin 500mg")
            col1, col2 = st.columns(2)
            dosage = col1.text_input("Dosage *", placeholder="e.g. 500mg, 1 tablet")
            frequency = col2.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily",
                                                       "Four times daily", "Every 8 hours", "As needed", "Weekly"])
            times = st.multiselect("When to take", MEDICATION_TIMES,
                                   default=["Morning (8 AM)"])
            col3, col4 = st.columns(2)
            start_date = col3.date_input("Start Date", value=date.today())
            end_date = col4.date_input("End Date (optional)", value=None)
            notes = st.text_area("Doctor's notes / Instructions", placeholder="e.g. Take after meals, avoid with dairy")
            submitted = st.form_submit_button(" Add Medication")
            if submitted:
                if not name or not dosage:
                    st.error("Medicine name and dosage are required.")
                else:
                    add_medication(
                        name=name,
                        dosage=dosage,
                        frequency=frequency,
                        times=", ".join(times),
                        start_date=str(start_date),
                        end_date=str(end_date) if end_date else "",
                        notes=notes
                    )
                    st.success(f"✅ {name} added to your medication list!")
                    st.balloons()

    # ── Tab 3: Medicine Info ──────────────────────────────────────────────────
   with tab3:
    st.subheader("📚 AI Medicine Information")
    st.caption("Search any medicine and get information using Gemini AI")

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")

        medicine_name = st.text_input(
            "🔍 Enter Medicine Name",
            placeholder="e.g. Dolo 650, Crocin, Metformin, Azee 500"
        )

        if st.button("Search Medicine"):
            if medicine_name:

                with st.spinner("Searching medicine information..."):

                    prompt = f"""
                    You are Swastha AI, a healthcare assistant.

                    Provide information about the medicine: {medicine_name}

                    Include:
                    1. Uses
                    2. Common Dosage
                    3. Side Effects
                    4. Warnings
                    5. Indian Brand Names

                    Keep the explanation simple and easy to understand.
                    Do not prescribe medicines.
                    """

                    response = model.generate_content(prompt)

                    st.markdown(response.text)

                    st.warning(
                        "⚠️ This information is for educational purposes only and should not replace professional medical advice."
                    )

    except Exception as e:
        st.error(f"Error: {str(e)}")

    st.divider()
    st.info("Need information about a medicine? Search above using AI.")
