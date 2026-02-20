"""Sacraments — Full record-keeping for all 7 Catholic sacraments
Real-world fields: godparents, confirmatory couples, banns, dispensations."""

import streamlit as st
try:
    from services.save_indicator import mark_saved, show_save_status
except Exception:
    def mark_saved(x): pass
    def show_save_status(x, y=None): pass
from datetime import date

st.set_page_config(page_title="Sacraments", page_icon="✝️", layout="wide")

st.title("✝️ Sacramental Records")
st.caption("Complete record-keeping for all 7 sacraments · Real-world fields")

if "sacrament_records" not in st.session_state:
    st.session_state.sacrament_records = {
        "baptism": [], "confirmation": [], "eucharist": [],
        "reconciliation": [], "marriage": [], "holy_orders": [], "anointing": []
    }

try:
    from services.save_indicator import trust_banner
    trust_banner("sacrament")
except Exception:
    pass

tabs = st.tabs(["💧 Baptism", "🕊️ Confirmation", "🍞 First Eucharist",
                 "💍 Marriage", "🙏 Reconciliation", "✝️ Holy Orders / Vows", "🕯️ Anointing"])

# ── BAPTISM ──────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("💧 Baptism Register")
    records = st.session_state.sacrament_records["baptism"]
    if records:
        import pandas as pd
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No baptism records yet. Add one below.")

    with st.expander("➕ Record a Baptism", expanded=not records):
        with st.form("baptism_form"):
            c1, c2 = st.columns(2)
            with c1:
                child_name = st.text_input("Full Name of Person Baptised *")
                dob = st.date_input("Date of Birth", max_value=date.today())
                bap_date = st.date_input("Date of Baptism")
                place = st.text_input("Place of Baptism", placeholder="St. Mary's Parish, Nairobi")
            with c2:
                minister = st.text_input("Minister (Priest/Deacon)")
                father_name = st.text_input("Father's Name")
                mother_name = st.text_input("Mother's Name (include maiden name)")
                nationality = st.text_input("Nationality / Country of Origin")

            st.markdown("**Godparents** *(Canon 874 — must be confirmed, practicing Catholics)*")
            gc1, gc2 = st.columns(2)
            with gc1:
                godfather = st.text_input("Godfather Name")
                godfather_parish = st.text_input("Godfather's Parish")
            with gc2:
                godmother = st.text_input("Godmother Name")
                godmother_parish = st.text_input("Godmother's Parish")

            st.markdown("**Additional Details**")
            dc1, dc2 = st.columns(2)
            with dc1:
                baptism_type = st.selectbox("Type", ["Infant", "Adult (RCIA)", "Emergency", "Conditional"])
                reg_number = st.text_input("Register Number (Book/Page/Entry)")
            with dc2:
                notes = st.text_area("Notes (dispensations, special circumstances)", height=80)

            submitted = st.form_submit_button("💧 Record Baptism", type="primary")
            if submitted and child_name:
                from services.sheets import _save
                _bap = {"Name": child_name, "DOB": str(dob), "Baptism Date": str(bap_date),
                    "Place": place, "Minister": minister, "Father": father_name,
                    "Mother": mother_name, "Godfather": godfather, "Godmother": godmother,
                    "Type": baptism_type, "Register No.": reg_number}
                st.session_state.sacrament_records["baptism"].append(_bap)
                _ok = _save("sacrament_baptism", _bap)
                show_save_status("sacrament_baptism", _ok)
                st.success(f"✅ Baptism of {child_name} recorded.")
                st.balloons()

# ── CONFIRMATION ─────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("🕊️ Confirmation Register")
    records = st.session_state.sacrament_records["confirmation"]
    if records:
        import pandas as pd
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No confirmation records yet.")

    with st.expander("➕ Record a Confirmation"):
        with st.form("conf_form"):
            c1, c2 = st.columns(2)
            with c1:
                cand_name = st.text_input("Full Name of Candidate *")
                conf_date = st.date_input("Date of Confirmation")
                bishop = st.text_input("Confirming Bishop / Priest (delegated)")
                parish = st.text_input("Parish of Confirmation")
            with c2:
                baptism_ref = st.text_input("Baptism Record Reference")
                conf_name = st.text_input("Confirmation Name (saint chosen)")
                sponsor_name = st.text_input("Sponsor Name *")
                sponsor_relationship = st.selectbox("Sponsor Relationship",
                    ["Godparent (same as Baptism)", "Other Catholic (confirmed, 16+)", "Parent (exceptional)"])

            prep_completed = st.checkbox("Preparation programme completed")
            catechism_year = st.number_input("Year of Catechism Completion", min_value=1980, max_value=2030, value=date.today().year)
            notes = st.text_area("Notes")

            if st.form_submit_button("🕊️ Record Confirmation", type="primary") and cand_name:
                from services.sheets import _save
                _conf = {"Name": cand_name, "Date": str(conf_date), "Bishop": bishop,
                    "Conf. Name": conf_name, "Sponsor": sponsor_name,
                    "Prep Completed": prep_completed, "Notes": notes}
                st.session_state.sacrament_records["confirmation"].append(_conf)
                _ok = _save("sacrament_confirmation", _conf)
                show_save_status("sacrament_confirmation", _ok)
                st.success(f"✅ Confirmation of {cand_name} recorded.")

# ── FIRST EUCHARIST ───────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("🍞 First Holy Communion Register")
    records = st.session_state.sacrament_records["eucharist"]
    if records:
        import pandas as pd
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No First Communion records yet.")

    with st.expander("➕ Record First Holy Communion"):
        with st.form("eucharist_form"):
            c1, c2 = st.columns(2)
            with c1:
                child_name = st.text_input("Full Name *")
                comm_date = st.date_input("Date of First Communion")
                age = st.number_input("Age at time of reception", min_value=5, max_value=99, value=9)
            with c2:
                minister = st.text_input("Presiding Priest")
                catechist = st.text_input("Preparing Catechist")
                prep_months = st.number_input("Months of preparation", min_value=1, max_value=24, value=12)

            reconciliation_prior = st.checkbox("First Reconciliation completed prior to Communion")

            if st.form_submit_button("🍞 Record First Communion", type="primary") and child_name:
                from services.sheets import _save
                _euch = {"Name": child_name, "Date": str(comm_date), "Age": age,
                    "Priest": minister, "Catechist": catechist, "Prep Months": prep_months,
                    "Reconciliation Prior": reconciliation_prior}
                st.session_state.sacrament_records["eucharist"].append(_euch)
                _ok = _save("sacrament_eucharist", _euch)
                show_save_status("sacrament_eucharist", _ok)
                st.success(f"✅ First Communion of {child_name} recorded.")

# ── MARRIAGE ─────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("💍 Marriage Register")
    records = st.session_state.sacrament_records["marriage"]
    if records:
        import pandas as pd
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("No marriage records yet.")

    with st.expander("➕ Record a Marriage", expanded=not records):
        with st.form("marriage_form"):
            st.markdown("**Bride & Groom**")
            c1, c2 = st.columns(2)
            with c1:
                groom = st.text_input("Groom — Full Name *")
                groom_dob = st.date_input("Groom Date of Birth", max_value=date.today())
                groom_parish = st.text_input("Groom's Baptism Parish")
                groom_nationality = st.text_input("Groom's Nationality")
            with c2:
                bride = st.text_input("Bride — Full Name *")
                bride_dob = st.date_input("Bride Date of Birth", max_value=date.today())
                bride_parish = st.text_input("Bride's Baptism Parish")
                bride_nationality = st.text_input("Bride's Nationality")

            st.markdown("**Marriage Details**")
            mc1, mc2 = st.columns(2)
            with mc1:
                wed_date = st.date_input("Date of Marriage")
                wed_place = st.text_input("Church / Place of Marriage")
                minister = st.text_input("Officiating Priest / Deacon")
            with mc2:
                form = st.selectbox("Form of Marriage", [
                    "Catholic canonical form", "Dispensation from form",
                    "Mixed marriage (with permission)", "Ecumenical celebration"])
                civil_reg = st.text_input("Civil Registration Number (if applicable)")

            st.markdown("**Witnesses**")
            w1, w2 = st.columns(2)
            with w1:
                witness1 = st.text_input("Witness 1 Name")
            with w2:
                witness2 = st.text_input("Witness 2 Name")

            st.markdown("**Confirmatory / Mentor Couple** *(Common in African Catholic practice — an established married couple who vouch, witness alongside, and provide ongoing mentorship)*")
            mc1, mc2 = st.columns(2)
            with mc1:
                mentor_husband = st.text_input("Mentor Husband Name")
                mentor_years = st.number_input("Years married (mentor couple)", min_value=0, max_value=60, value=10)
            with mc2:
                mentor_wife = st.text_input("Mentor Wife Name")
                mentor_parish = st.text_input("Mentor couple's parish")

            st.markdown("**Pre-Nuptial Investigation & Dispensations**")
            d1, d2, d3 = st.columns(3)
            with d1:
                banns = st.checkbox("Banns published (×3)?")
                banns_dispensation = st.checkbox("Dispensation from banns")
            with d2:
                consanguinity = st.checkbox("Consanguinity/Affinity checked")
                disparity_of_cult = st.checkbox("Disparity of cult dispensation")
            with d3:
                mixed_religion = st.checkbox("Mixed religion permission")
                previous_marriage = st.checkbox("Previous marriage (nullity required)")

            pre_cana = st.checkbox("Pre-Cana / Marriage preparation completed")
            notes = st.text_area("Notes (impediments resolved, special circumstances)", height=70)

            if st.form_submit_button("💍 Record Marriage", type="primary") and groom and bride:
                from services.sheets import _save
                _mar = {"Groom": groom, "Bride": bride, "Date": str(wed_date),
                    "Place": wed_place, "Minister": minister, "Form": form,
                    "Witness 1": witness1, "Witness 2": witness2,
                    "Mentor Husband": mentor_husband, "Mentor Wife": mentor_wife,
                    "Pre-Cana": pre_cana, "Banns": banns, "Notes": notes}
                st.session_state.sacrament_records["marriage"].append(_mar)
                _ok = _save("sacrament_marriage", _mar)
                show_save_status("sacrament_marriage", _ok)
                st.success(f"✅ Marriage of {groom} & {bride} recorded.")
                st.balloons()

# ── RECONCILIATION ────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("🙏 Reconciliation / Confessions")
    st.info("Individual confessional records are kept under the seal — only aggregate statistics are stored here.")

    with st.expander("📊 Record Aggregate Confession Statistics"):
        with st.form("rec_form"):
            c1, c2 = st.columns(2)
            with c1:
                period = st.text_input("Period (e.g. Lent 2026, Easter 2026)")
                total_penitents = st.number_input("Total penitents", min_value=0, value=0)
                confessors = st.number_input("Number of confessors", min_value=1, value=1)
            with c2:
                sessions = st.number_input("Number of sessions", min_value=1, value=1)
                general_absolution = st.checkbox("General absolution given (exceptional circumstances)")

            if st.form_submit_button("Record Statistics", type="primary"):
                from services.sheets import _save
                _rec = {
                    "form_type": "sacrament_reconciliation",
                    "Period": period, "Penitents": total_penitents,
                    "Confessors": confessors, "Sessions": sessions,
                    "General Absolution": general_absolution,
                }
                st.session_state.sacrament_records["reconciliation"].append(_rec)
                _ok = _save("sacrament_reconciliation", _rec)
                show_save_status("sacrament_reconciliation", _ok)

# ── HOLY ORDERS / RELIGIOUS VOWS ─────────────────────────────────────────────
with tabs[5]:
    st.subheader("✝️ Holy Orders & Religious Profession")

    with st.expander("➕ Record Ordination / Profession"):
        with st.form("orders_form"):
            c1, c2 = st.columns(2)
            with c1:
                person = st.text_input("Full Name *")
                ord_date = st.date_input("Date")
                ord_type = st.selectbox("Type", [
                    "Diaconate (permanent)", "Diaconate (transitional)",
                    "Priesthood", "Episcopate (bishop)",
                    "Temporary vows (religious)", "Perpetual vows (religious)",
                    "Consecrated virgin", "Secular institute profession",
                ])
            with c2:
                ordaining_bishop = st.text_input("Ordaining Bishop / Superior")
                place = st.text_input("Place")
                diocese_congregation = st.text_input("Diocese / Religious Congregation")
                seminary = st.text_input("Seminary / Novitiate")

            if st.form_submit_button("✝️ Record", type="primary") and person:
                from services.sheets import _save
                _ord = {"Name": person, "Date": str(ord_date), "Type": ord_type,
                    "Bishop/Superior": ordaining_bishop, "Diocese/Congregation": diocese_congregation}
                st.session_state.sacrament_records["holy_orders"].append(_ord)
                _ok = _save("sacrament_holy_orders", _ord)
                show_save_status("sacrament_holy_orders", _ok)
                st.success(f"✅ {ord_type} of {person} recorded.")

# ── ANOINTING OF THE SICK ─────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("🕯️ Anointing of the Sick")
    st.caption("Can. 1004 — Given to those in danger of death from illness or old age")

    with st.expander("➕ Record Anointing"):
        with st.form("anoint_form"):
            c1, c2 = st.columns(2)
            with c1:
                person = st.text_input("Full Name *")
                anoint_date = st.date_input("Date")
                minister = st.text_input("Minister (Priest)")
                location = st.text_input("Location (hospital, home, hospice...)")
            with c2:
                reason = st.selectbox("Reason", [
                    "Serious illness", "Surgery (before)",
                    "Old age / Frailty", "Danger of death",
                    "Viaticum (last rites)", "Recovery — thanksgiving",
                ])
                viaticum = st.checkbox("Viaticum (Last Communion) administered")
                reconciliation_prior = st.checkbox("Reconciliation offered prior")
                outcome = st.text_input("Follow-up / Outcome (optional)")

            if st.form_submit_button("🕯️ Record Anointing", type="primary") and person:
                from services.sheets import _save
                _anoint = {"Name": person, "Date": str(anoint_date), "Minister": minister,
                    "Location": location, "Reason": reason, "Viaticum": viaticum}
                st.session_state.sacrament_records["anointing"].append(_anoint)
                _ok = _save("sacrament_anointing", _anoint)
                show_save_status("sacrament_anointing", _ok)
                st.success(f"✅ Anointing of {person} recorded.")

# Summary
st.divider()
st.subheader("📊 Sacramental Overview")
cols = st.columns(7)
labels = ["Baptism", "Confirmation", "Eucharist", "Marriage",
          "Reconciliation", "Orders/Vows", "Anointing"]
keys = ["baptism", "confirmation", "eucharist", "marriage",
        "reconciliation", "holy_orders", "anointing"]
for col, label, key in zip(cols, labels, keys):
    col.metric(label, len(st.session_state.sacrament_records[key]))

st.caption("💾 Records are stored for this session. Connect Google Sheets in Admin → Data Management for persistence.")
