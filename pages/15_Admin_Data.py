"""Admin — Data Management: bulk import/export CSV for all modules."""

import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Admin — Data Management", page_icon="⚙️", layout="wide")

st.title("⚙️ Admin — Data Management")
st.caption("Bulk import/export · CSV/Excel · Session data · Backup & restore")

MODULES = {
    "baptism": ("💧 Baptism", "sacrament_records"),
    "confirmation": ("🕊️ Confirmation", "sacrament_records"),
    "marriage": ("💍 Marriage", "sacrament_records"),
    "sccs": ("👥 SCCs", None),
    "catechists": ("📚 Catechists", None),
    "homebound": ("🏠 Homebound", None),
    "grief": ("💔 Grief Support", None),
    "mentors": ("🤝 Mentorship", None),
    "new_members": ("🆕 New Members", None),
    "formation_programmes": ("🎓 Formation Programmes", None),
    "formation_participants": ("🎓 Participants", None),
}

tab1, tab2, tab3 = st.tabs(["⬇️ Export Data", "⬆️ Import Data", "🗑️ Data Hygiene"])

# ── EXPORT ─────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("⬇️ Export to CSV / Excel")
    st.info("All data is from the current session. Connect a database (Google Sheets or SQLite) for persistence.")

    for key, (label, parent) in MODULES.items():
        if parent == "sacrament_records":
            records = st.session_state.get("sacrament_records", {}).get(key, [])
        else:
            records = st.session_state.get(key, [])

        if records:
            df = pd.DataFrame(records)
            csv = df.to_csv(index=False).encode("utf-8")
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{label}** — {len(records)} records")
            col2.download_button(
                label="⬇️ CSV",
                data=csv,
                file_name=f"{key}_{datetime.today().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key=f"dl_{key}",
            )
        else:
            st.markdown(f"**{label}** — _No records_")

    st.divider()
    # Full backup as JSON
    import json
    backup = {
        "exported_at": datetime.utcnow().isoformat(),
        "sacrament_records": st.session_state.get("sacrament_records", {}),
        "sccs": st.session_state.get("sccs", []),
        "catechists": st.session_state.get("catechists", []),
        "homebound": st.session_state.get("homebound", []),
        "grief": st.session_state.get("grief", []),
        "mentors": st.session_state.get("mentors", []),
        "new_members": st.session_state.get("new_members", []),
        "formation_programmes": st.session_state.get("formation_programmes", []),
        "formation_participants": st.session_state.get("formation_participants", []),
    }
    json_bytes = json.dumps(backup, indent=2, default=str).encode("utf-8")
    st.download_button(
        label="💾 Full Backup (JSON)",
        data=json_bytes,
        file_name=f"parish_backup_{datetime.today().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
    )

# ── IMPORT ─────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("⬆️ Import from CSV")
    st.warning("Importing will **add** records to the existing list (no duplicates check yet). Always export first as backup.")

    target = st.selectbox("Import into module", [f"{label} ({key})" for key, (label, _) in MODULES.items()])
    target_key = target.split("(")[-1].rstrip(")")

    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(5), use_container_width=True)
            st.markdown(f"**{len(df)} rows detected**")

            if st.button("⬆️ Import records", type="primary"):
                records = df.to_dict(orient="records")
                parent = MODULES.get(target_key, ("", None))[1]
                if parent == "sacrament_records":
                    if "sacrament_records" not in st.session_state:
                        st.session_state.sacrament_records = {}
                    existing = st.session_state.sacrament_records.get(target_key, [])
                    st.session_state.sacrament_records[target_key] = existing + records
                else:
                    existing = st.session_state.get(target_key, [])
                    st.session_state[target_key] = existing + records
                st.success(f"✅ {len(records)} records imported into {target_key}.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    st.divider()
    st.subheader("📋 CSV Templates")
    st.caption("Download blank templates with correct column headers")

    TEMPLATES = {
        "sccs": ["Name","Zone","Leader","Phone","Meeting Day","Meeting Time","Location","Families","Status","Focus","Notes"],
        "catechists": ["Name","Email","Phone","Level","Ministry","Start Date","Hours Completed","Hours Required","Status","Background Check","Renewal Due","Notes"],
        "homebound": ["Name","Condition","Address","Phone","Emergency Contact","Freq","Minister","Last Visit","Communion","Notes"],
        "baptism": ["Name","DOB","Baptism Date","Place","Minister","Father","Mother","Godfather","Godmother","Type","Register No."],
        "marriage": ["Groom","Bride","Date","Place","Minister","Form","Witness 1","Witness 2","Mentor Husband","Mentor Wife","Pre-Cana","Banns","Notes"],
    }

    for tkey, cols in TEMPLATES.items():
        label = MODULES.get(tkey, (tkey, ""))[0]
        template_df = pd.DataFrame(columns=cols)
        csv = template_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📋 {label} template",
            data=csv,
            file_name=f"template_{tkey}.csv",
            mime="text/csv",
            key=f"tmpl_{tkey}",
        )

# ── DATA HYGIENE ───────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🗑️ Data Hygiene")
    st.warning("These actions clear session data. Export first!")

    for key, (label, parent) in MODULES.items():
        if parent == "sacrament_records":
            count = len(st.session_state.get("sacrament_records", {}).get(key, []))
        else:
            count = len(st.session_state.get(key, []))

        if count > 0:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{label}** — {count} records")
            if c2.button(f"Clear", key=f"clr_{key}"):
                if parent == "sacrament_records":
                    st.session_state.sacrament_records[key] = []
                else:
                    st.session_state[key] = []
                st.rerun()

    st.divider()
    if st.button("⚠️ Clear ALL session data", type="secondary"):
        for key, (_, parent) in MODULES.items():
            if parent == "sacrament_records":
                if "sacrament_records" in st.session_state:
                    st.session_state.sacrament_records[key] = []
            else:
                st.session_state[key] = []
        st.success("All session data cleared.")

    st.divider()
    st.subheader("☁️ Persistence Options")
    st.markdown("""
**For production use, connect one of these backends:**

🔵 **Google Sheets** — free, collaborative, no server needed
- Add `GOOGLE_SHEETS_URL` to Streamlit secrets
- Use `gspread` library (add to requirements.txt)

🟢 **SQLite** — local file database, no external service
- Use `sqlite3` (built into Python)
- Store in `/data/parish.db`

🟡 **Supabase** — free Postgres backend, REST API
- Add `SUPABASE_URL` + `SUPABASE_KEY` to secrets

🔴 **Firebase Firestore** — Google's document DB, realtime
- Good for multi-parish sync
""")
