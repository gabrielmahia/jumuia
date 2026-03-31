"""Admin — Data Management: bulk import/export CSV for all modules."""

import streamlit as st

# ── Mobile CSS ──────────────────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, ".")
try:
    from services.mobile_ux import inject_mobile_css as _inj; _inj()
except Exception:
    pass

try:
    import pandas as pd
except ImportError:
    pd = None
from datetime import datetime, UTC

st.set_page_config(page_title="Admin — Data Management", page_icon="⚙️", layout="wide")
try:
    from services.roles import require_role as _require_role
    _require_role("coordinator", "Admin & Data")
except Exception:
    pass


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
    "training_log": ("📚 Training Log", None),
}

tab1, tab2, tab3 = st.tabs(["⬇️ Export Data", "⬆️ Import Data", "🗑️ Data Hygiene"])

# ── EXPORT ─────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("⬇️ Export to CSV / Excel")
    try:
        from services.sheets import is_live as _sheets_live
        if _sheets_live():
            st.success("🟢 Google Sheets connected — exported data reflects what you've entered today. Download from your sheet for full history.", icon=None)
        else:
            st.info("📋 Showing records entered this visit. Connect Google Sheets (below) to save records permanently across visits.")
    except Exception:
        pass

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
        "exported_at": datetime.now(UTC).isoformat(),
        "sacrament_records": st.session_state.get("sacrament_records", {}),
        "sccs": st.session_state.get("sccs", []),
        "catechists": st.session_state.get("catechists", []),
        "homebound": st.session_state.get("homebound", []),
        "grief": st.session_state.get("grief", []),
        "mentors": st.session_state.get("mentors", []),
        "new_members": st.session_state.get("new_members", []),
        "formation_programmes": st.session_state.get("formation_programmes", []),
        "formation_participants": st.session_state.get("formation_participants", []),
        "training_log": st.session_state.get("training_log", []),
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
                # Persist to Sheets
                _saved_count = 0
                try:
                    from services.sheets import _save as _sheets_save
                    from services.parish_identity import inject_into_record as _enrich
                    for _rec in records:
                        if _sheets_save(target_key, _enrich(_rec)):
                            _saved_count += 1
                except Exception:
                    pass
                if _saved_count:
                    st.success(f"✅ {len(records)} records imported · {_saved_count} saved to Sheets")
                else:
                    st.success(f"✅ {len(records)} records imported into {target_key} (saved for this visit)")
        except Exception:
            st.error("The file could not be read. Please check that it is a valid CSV file and try again.")

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
    st.warning("These actions clear all data entered this visit. Export first!")

    for key, (label, parent) in MODULES.items():
        if parent == "sacrament_records":
            count = len(st.session_state.get("sacrament_records", {}).get(key, []))
        else:
            count = len(st.session_state.get(key, []))

        if count > 0:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{label}** — {count} records")
            if c2.button("Clear", key=f"clr_{key}"):
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
        st.success("All records cleared for this visit.")

    st.divider()
    st.subheader("☁️ Persistence Options")
    st.markdown("""
**How to save your parish data permanently:**

🔵 **Google Sheets (Recommended)** — free, simple, no technical knowledge needed
- Your parish records save automatically to a Google Sheet you own
- See the setup guide: **More Tools → Set Up → Sheets Setup**
- Already connected? Your data is saving automatically.

🟡 **Need help setting this up?**
- Contact your parish tech coordinator, or
- Email contact@aikungfu.dev — the app developer can help
""")
