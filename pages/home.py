"""Catholic Parish Steward — Homepage"""
import streamlit as st

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap');

.cps-home-hero {
    background: linear-gradient(135deg, #0B1F3A 0%, #1a3a6b 100%);
    border-radius: 16px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.cps-home-hero::before {
    content:'✝';
    position:absolute; right:2.5rem; top:50%; transform:translateY(-50%);
    font-size:8rem; color:rgba(201,168,76,0.10); font-family:serif;
    line-height:1;
}
.cps-home-title {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:2.8rem; font-weight:400;
    color:white; margin:0 0 0.5rem; line-height:1.1;
}
.cps-home-sub {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:1.1rem; color:rgba(240,217,138,0.85);
    margin:0 0 1.5rem;
}
.cps-home-verse {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:0.95rem; font-style:italic;
    color:rgba(255,255,255,0.5); margin:0;
}
.cps-action-card {
    border: 1px solid rgba(11,31,58,0.10);
    border-radius: 14px;
    padding: 2rem 1.75rem 1.75rem;
    background: #F8F4EC;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.cps-action-card::after {
    content:'';
    position:absolute; bottom:0; left:0; right:0; height:4px;
    border-radius:0 0 14px 14px;
}
.cps-action-card.church::after { background: #C9A84C; }
.cps-action-card.readings::after { background: #1A5C3A; }
.cps-action-card.ai::after { background: #1a3a6b; }
.cps-card-icon { font-size:2.5rem; margin-bottom:1rem; display:block; }
.cps-card-title {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:1.4rem; font-weight:400;
    color:#0B1F3A; margin:0 0 0.5rem;
}
.cps-card-desc {
    font-family:'DM Sans',system-ui,sans-serif;
    font-size:0.92rem; color:#4A5568;
    line-height:1.6; margin:0 0 1.25rem;
}
.cps-card-examples { font-size:0.78rem; color:#6B7280; }
.cps-card-examples span {
    display:inline-block;
    background:rgba(11,31,58,0.06);
    border-radius:4px; padding:0.15rem 0.45rem;
    margin:0.15rem 0.15rem 0 0;
}
.cps-stats {
    display:flex; gap:2rem; flex-wrap:wrap;
    margin-top:1.5rem; padding-top:1.5rem;
    border-top:1px solid rgba(11,31,58,0.08);
}
.cps-stat-num {
    font-family:'DM Serif Display',Georgia,serif;
    font-size:1.6rem; color:#0B1F3A; display:block; line-height:1;
}
.cps-stat-label {
    font-size:0.72rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.07em; color:#9CA3AF; display:block; margin-top:0.2rem;
}
@media (prefers-color-scheme: dark) {
    .cps-action-card { background: rgba(255,255,255,0.04); }
    .cps-card-title  { color: #F0D98A; }
    .cps-card-desc   { color: #D1D5DB; }
    .cps-stat-num    { color: #F0D98A; }
}
@media (max-width:640px) {
    .cps-home-title { font-size:2rem; }
    .cps-home-hero::before { display:none; }
    .cps-home-hero { padding:2rem 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cps-home-hero">
  <div class="cps-home-title">Catholic Parish Steward</div>
  <div class="cps-home-sub">
    Find your church · Follow the daily readings · Ask a question in any language
  </div>
  <div class="cps-home-verse">
    "Whatever you did for the least of these, you did for me." — Matthew 25:40
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
<div class="cps-action-card church">
  <span class="cps-card-icon">🗺️</span>
  <div class="cps-card-title">Find a Church</div>
  <div class="cps-card-desc">Search 40,000+ Catholic churches worldwide by name, city, or region.</div>
  <div class="cps-card-examples">
    <span>Nairobi</span><span>Samburu</span><span>Consolata Shrine</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("🗺️ Find a Church", type="primary", use_container_width=True):
        st.switch_page("pages/07_Parish_Directory.py")

with c2:
    st.markdown("""
<div class="cps-action-card readings">
  <span class="cps-card-icon">📖</span>
  <div class="cps-card-title">Daily Readings</div>
  <div class="cps-card-desc">Today's Mass readings, Rosary, Divine Mercy, Stations of the Cross.</div>
  <div class="cps-card-examples">
    <span>Rosary</span><span>Divine Mercy</span><span>Kiswahili</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("📖 Daily Readings & Prayers", type="primary", use_container_width=True):
        st.switch_page("pages/09_Daily_Prayers.py")

with c3:
    st.markdown("""
<div class="cps-action-card ai">
  <span class="cps-card-icon">🤖</span>
  <div class="cps-card-title">Ask the Assistant</div>
  <div class="cps-card-desc">Questions about Mass, sacraments, translate a bulletin into Kiswahili.</div>
  <div class="cps-card-examples">
    <span>Mass times</span><span>Translation</span><span>Homily prep</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.write("")
    if st.button("🤖 AI Parish Assistant", type="primary", use_container_width=True):
        st.switch_page("pages/06_AI_Assistant.py")

st.markdown("""
<div class="cps-stats">
  <div><span class="cps-stat-num">40,000+</span><span class="cps-stat-label">Churches searchable</span></div>
  <div><span class="cps-stat-num">150+</span><span class="cps-stat-label">Countries</span></div>
  <div><span class="cps-stat-num">6</span><span class="cps-stat-label">Languages</span></div>
  <div><span class="cps-stat-num">1.3B</span><span class="cps-stat-label">Catholics worldwide</span></div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.caption(
    "Catholic Parish Steward · "
    "[GitHub](https://github.com/gabrielmahia/catholic-network-tools) · "
    "Built on the AMECEA tradition of Small Christian Communities · "
    "Data: OpenStreetMap contributors"
)
