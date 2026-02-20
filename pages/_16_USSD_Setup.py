"""
USSD Setup Guide — for parishes and dioceses
"""
import streamlit as st

st.set_page_config(page_title="Set Up USSD | Parish Steward", page_icon="📱")

st.title("📱 Bring *384*248724# to Your Parish")
st.caption("A guide for parish administrators, diocesan offices, and pastoral coordinators")

st.info(
    "**Why this matters:** A parishioner in Samburu or Turkana with a basic phone "
    "and no internet can dial a USSD code and get Mass times, today's reading, and "
    "emergency pastoral contacts in seconds. No smartphone. No data. No literacy barrier. "
    "But activating this for real phones requires a registered organization — a parish, "
    "diocese, or Catholic NGO — to complete a one-time setup.",
    icon="🌍"
)

st.markdown("---")

st.header("What your parish gets")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Dial code", "*384*248724#")
    st.caption("Works on any Safaricom or Airtel phone in Kenya")
with col2:
    st.metric("Cost to parish", "~KES 1–2")
    st.caption("Per session. Parishioner pays nothing extra.")
with col3:
    st.metric("Setup time", "3–7 days")
    st.caption("After submitting documents to Africa's Talking")

st.markdown("---")

st.header("Step-by-step setup")

with st.expander("**Step 1 — Register your organization on Africa's Talking**", expanded=True):
    st.markdown("""
Go to [account.africastalking.com](https://account.africastalking.com) and create an account 
using your parish or diocesan email address.

On the home screen, click **New Team** and name it after your parish or diocese 
(e.g. "Archdiocese of Nairobi" or "St Joseph Parish Wajir").

Inside the team, click **Create App** and fill in:
- **App name:** your parish name
- **Country:** Kenya  
- **Currency:** KES

You will need to top up the wallet with at least **KES 500** before going live. 
You can do this via M-Pesa.
""")

with st.expander("**Step 2 — Gather your documents**"):
    st.markdown("""
Kenya's Communications Authority requires the following for any USSD service. 
Have these ready as scanned PDF or JPG files:

**If registering as a parish or diocese:**
- Certificate of Registration (from the Registrar of Societies or NGO Board)
- KRA PIN certificate of the organization
- National ID of the authorized representative (parish priest or diocesan chancellor)
- Letter of Authorization on official letterhead

**If you need help getting these documents**, contact your diocesan chancery — 
they typically hold registration certificates for all parishes in the diocese.

**Already registered with the government?** The Catholic Secretariat of Kenya 
and most dioceses are registered entities and have all of these documents on file.
""")

with st.expander("**Step 3 — Submit the USSD application**"):
    st.markdown("""
Inside your AT app, go to **USSD → Service Codes → application form**.

Fill in:
- **Country:** Kenya
- **Product type:** Shared
- **Channel number:** `248724` *(this keeps the same dial code parishioners already know)*
- **Callback URL:** `https://cnt-ussd-860570427256.africa-south1.run.app/ussd`
- **Operators:** Safaricom + Airtel Kenya

Upload your documents and submit. Africa's Talking reviews shared code applications 
within **3–7 business days** and will email you when approved.
""")

with st.expander("**Step 4 — Notify us so we activate your account**"):
    st.markdown("""
Once Africa's Talking approves your channel, send us your:
- **AT username** (shown in your app dashboard)
- **Organization name**

Email: [contact@aikungfu.dev](mailto:contact@aikungfu.dev)  
Subject: **USSD Activation — [Your Parish Name]**

We will update the service within 24 hours and your parishioners can start dialing immediately.
""")

st.markdown("---")

st.header("Which organization should apply?")

st.markdown("""
The fastest path is through an organization that is **already registered** with the 
Kenyan government and has all documents on file:

| Organization | Advantage |
|---|---|
| **Archdiocese / Diocese** | Already registered, has legal standing, can serve all parishes |
| **Catholic Secretariat of Kenya** | National reach, single application covers all dioceses |
| **Individual parish** | Direct control, faster decision-making |
| **Caritas Kenya** | Registered NGO, strong for emergency/pastoral use cases |

**Our recommendation:** Approach the diocesan chancery first. A single application 
at the diocese level serves every parish in the region without each parish needing 
to register separately.
""")

st.markdown("---")

st.header("Questions?")
st.markdown("""
**Email:** [contact@aikungfu.dev](mailto:contact@aikungfu.dev)  
**Subject line:** USSD Parish Setup  

We respond within 24 hours and can guide your diocesan administrator through 
the entire process at no cost.
""")

with st.sidebar:
    st.markdown("### 📱 USSD Access")
    st.info(
        "This service is already built and tested. "
        "Your parish just needs to complete the "
        "Africa's Talking registration to activate "
        "it for real phones.",
        icon="✅"
    )
