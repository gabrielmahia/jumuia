"""Daily Prayers — Complete Catholic Prayer Library
Rosary (all 4 mysteries), essential prayers, multilingual."""

import streamlit as st

st.set_page_config(page_title="Daily Prayers", page_icon="🙏", layout="wide")

st.title("🙏 Daily Prayers")
st.caption("Essential Catholic prayers · Rosary · Chaplets · Multilingual")

# ── Today's Readings Banner ────────────────────────────────────────────────────
try:
    from services.lectionary import get_reading, liturgical_color
    from datetime import date
    r = get_reading()
    season_color = {"Advent": "#6B21A8", "Lent": "#7C3AED", "Easter": "#D97706",
                    "Christmas": "#FFFFFF", "Ordinary": "#15803D"}.get(r["season"], "#15803D")
    feast_line = f"**{r['feast']}** — " if r["feast"] else ""
    refs = " · ".join(r["readings"]) if r["readings"] else ""
    link = f"[Full readings →](https://{r['link']})"
    
    st.markdown(f"""
<div style="background:rgba(11,31,58,0.06);border-left:4px solid {season_color};
     border-radius:0 8px 8px 0;padding:0.9rem 1.2rem;margin-bottom:1.5rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
       letter-spacing:0.1em;color:#6B7280;margin-bottom:0.3rem;">
    TODAY · {r["season"].upper()} WEEK {r["week"]} · YEAR {r["cycle"]}
  </div>
  <div style="font-size:1rem;color:#1F2937;line-height:1.5;">
    {feast_line}{refs}
  </div>
</div>
""", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col2:
        st.link_button("Full readings (USCCB) →", f"https://{r['link']}", use_container_width=True)
except Exception:
    pass

PRAYERS = {
    "en": {
        "our_father": (
            "Our Father, who art in heaven,\nhallowed be Thy name;\nThy kingdom come;\n"
            "Thy will be done on earth as it is in heaven.\nGive us this day our daily bread;\n"
            "and forgive us our trespasses,\nas we forgive those who trespass against us;\n"
            "and lead us not into temptation,\nbut deliver us from evil. Amen."
        ),
        "hail_mary": (
            "Hail Mary, full of grace, the Lord is with thee;\nblessed art thou among women,\n"
            "and blessed is the fruit of thy womb, Jesus.\nHoly Mary, Mother of God,\n"
            "pray for us sinners,\nnow and at the hour of our death. Amen."
        ),
        "glory_be": (
            "Glory be to the Father, and to the Son, and to the Holy Spirit;\n"
            "as it was in the beginning, is now, and ever shall be,\nworld without end. Amen."
        ),
        "apostles_creed": (
            "I believe in God, the Father Almighty, Creator of Heaven and earth;\n"
            "and in Jesus Christ, His only Son, Our Lord,\nwho was conceived by the Holy Spirit,\n"
            "born of the Virgin Mary, suffered under Pontius Pilate,\n"
            "was crucified, died and was buried.\nHe descended into Hell;\n"
            "on the third day He rose again from the dead;\nHe ascended into Heaven,\n"
            "and is seated at the right hand of God the Father Almighty;\n"
            "from thence He shall come to judge the living and the dead.\n"
            "I believe in the Holy Spirit, the holy Catholic Church,\n"
            "the communion of Saints, the forgiveness of sins,\n"
            "the resurrection of the body, and life everlasting. Amen."
        ),
        "hail_holy_queen": (
            "Hail, Holy Queen, Mother of Mercy,\nour life, our sweetness, and our hope.\n"
            "To thee do we cry, poor banished children of Eve.\nTo thee do we send up our sighs,\n"
            "mourning and weeping in this vale of tears.\nTurn then, most gracious advocate,\n"
            "thine eyes of mercy toward us,\nand after this our exile, show unto us\n"
            "the blessed fruit of thy womb, Jesus.\nO clement, O loving, O sweet Virgin Mary.\n"
            "Pray for us, O Holy Mother of God,\nthat we may be made worthy of the promises of Christ. Amen."
        ),
    },
    "sw": {
        "our_father": (
            "Baba yetu uliye mbinguni,\nJina lako litakaswe;\nUfalme wako uje;\n"
            "Mapenzi yako yatimizwe duniani kama mbinguni.\nUtupe leo mkate wetu wa kila siku;\n"
            "na utusamehe makosa yetu,\nkama sisi tunavyowasamehe wale wanaotukosea;\n"
            "na usitutie katika majaribu,\nbali utuokoe na yule mwovu. Amen."
        ),
        "hail_mary": (
            "Salamu Maria, umejaa neema, Bwana yu nawe;\nunastahili sifa zaidi ya wanawake wote,\n"
            "na uzao wa tumbo lako Yesu anastahili sifa.\nMaria Mtakatifu, Mama wa Mungu,\n"
            "tuombee sisi wenye dhambi,\nsasa na saa ya mauti yetu. Amen."
        ),
        "glory_be": (
            "Utukufu kwa Baba, na kwa Mwana, na kwa Roho Mtakatifu;\n"
            "kama ulivyokuwa tangu mwanzo, sasa uko, na utakuwa daima,\nDunia bila mwisho. Amen."
        ),
    },
    "lg": {
        "our_father": (
            "Kitaffe ali mu ggulu,\neriinya lyo litukuzibwe;\nombaire yo ejje;\n"
            "by'oyagala bikolwe ku nsi nga bwe bikolwa mu ggulu.\nOtuwe leero emmere yaffe;\n"
            "nutusonyiwe ebibi byaffe,\nga naffe bwe tususonyiwa abatubikola;\n"
            "ne totutwale mu kuyingizibwa,\nnaye otulokole eri omubi. Amen."
        ),
        "hail_mary": (
            "Nkusiimbye Maliya, ojjudde ekisa,\nRabbi ali nawe;\nwatukuzibwa mu bakazi bonna,\n"
            "era natukuzibwa kibala ky'olubuto lwo Yezu.\nMaliya Mutukuvu, Maama wa Katonda,\n"
            "tubeelangirire ffe abalyamu,\nnoolwanda ne ku luzzi lwa okufa kwaffe. Amen."
        ),
    },
}

ROSARY_MYSTERIES = {
    "Joyful Mysteries (Monday & Saturday)": [
        ("The Annunciation", "The Angel Gabriel announces to Mary that she will conceive and bear the Son of God. Fruit: Humility."),
        ("The Visitation", "Mary visits her cousin Elizabeth, who is filled with the Holy Spirit. Fruit: Love of neighbour."),
        ("The Nativity", "Jesus is born in a manger in Bethlehem. Fruit: Poverty of spirit / Detachment from worldly things."),
        ("The Presentation", "Mary and Joseph present the child Jesus in the Temple. Fruit: Obedience / Purity."),
        ("Finding Jesus in the Temple", "After three days, Mary and Joseph find Jesus discussing with the teachers. Fruit: Piety / Joy in finding Jesus."),
    ],
    "Luminous Mysteries (Thursday)": [
        ("The Baptism of Jesus", "Jesus is baptised in the Jordan by John; the Father's voice is heard, the Spirit descends. Fruit: Openness to the Holy Spirit."),
        ("The Wedding at Cana", "At Mary's intercession, Jesus performs his first miracle. Fruit: To Jesus through Mary."),
        ("Proclamation of the Kingdom", "Jesus calls all to conversion and forgiveness of sins. Fruit: Repentance / Trust in God."),
        ("The Transfiguration", "Jesus is transfigured on Mount Tabor before Peter, James, and John. Fruit: Desire for holiness."),
        ("Institution of the Eucharist", "At the Last Supper, Jesus gives us his Body and Blood. Fruit: Adoration."),
    ],
    "Sorrowful Mysteries (Tuesday & Friday)": [
        ("The Agony in the Garden", "Jesus prays in anguish in Gethsemane; his sweat falls like drops of blood. Fruit: Sorrow for sin / Conformity to God's will."),
        ("The Scourging at the Pillar", "Jesus is bound to a pillar and mercilessly scourged. Fruit: Purity / Mortification."),
        ("The Crowning with Thorns", "Soldiers press a crown of thorns upon Jesus' head. Fruit: Moral courage."),
        ("The Carrying of the Cross", "Jesus carries the heavy cross toward Golgotha. Fruit: Patience."),
        ("The Crucifixion", "Jesus is nailed to the cross and dies after three hours of agony. Fruit: Salvation / Forgiveness."),
    ],
    "Glorious Mysteries (Wednesday & Sunday)": [
        ("The Resurrection", "On the third day, Jesus rises gloriously from the dead. Fruit: Faith."),
        ("The Ascension", "Forty days after his Resurrection, Jesus ascends into heaven. Fruit: Hope / Desire for heaven."),
        ("The Descent of the Holy Spirit", "Ten days after the Ascension, the Holy Spirit descends on Mary and the Apostles. Fruit: Gifts of the Holy Spirit."),
        ("The Assumption", "At the end of her earthly life, Mary is assumed body and soul into heaven. Fruit: Grace of a happy death."),
        ("The Coronation", "Mary is crowned Queen of Heaven and Earth. Fruit: Perseverance / Trust in Mary's intercession."),
    ],
}

DIVINE_MERCY = {
    "Opening": "You expired, Jesus, but the source of life gushed forth for souls, and the ocean of mercy opened up for the whole world.",
    "Chaplet_verse": (
        "For the sake of His sorrowful Passion,\nhave mercy on us and on the whole world.\n\n"
        "(On each small bead:)\nEternal God, in whom mercy is endless and the treasury of compassion inexhaustible, "
        "look kindly upon us and increase Your mercy in us, that in difficult moments we might not despair "
        "nor become despondent, but with great confidence submit ourselves to Your holy will, "
        "which is Love and Mercy itself."
    ),
    "Closing": "Holy God, Holy Mighty One, Holy Immortal One, have mercy on us and on the whole world. (× 3)",
}

STATIONS = [
    "Jesus is condemned to death",
    "Jesus takes up his cross",
    "Jesus falls the first time",
    "Jesus meets his mother Mary",
    "Simon of Cyrene helps Jesus carry the cross",
    "Veronica wipes the face of Jesus",
    "Jesus falls the second time",
    "Jesus meets the women of Jerusalem",
    "Jesus falls the third time",
    "Jesus is stripped of his garments",
    "Jesus is nailed to the cross",
    "Jesus dies on the cross",
    "Jesus is taken down from the cross",
    "Jesus is laid in the tomb",
]

# ── Language selector ─────────────────────────────────────────────────────────
lang_map = {"English": "en", "Kiswahili": "sw", "Luganda": "lg"}
lang_display = st.sidebar.selectbox("🌍 Language / Lugha", list(lang_map.keys()))
lang = lang_map[lang_display]
prayers = PRAYERS.get(lang, PRAYERS["en"])

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📿 Essential Prayers", "📿 The Rosary", "🩸 Divine Mercy", "✝️ Stations", "🌅 Daily Rhythm"]
)

with tab1:
    st.subheader(f"Essential Catholic Prayers — {lang_display}")
    with st.expander("🙏 Our Father (Pater Noster)", expanded=True):
        st.markdown(f"```\n{prayers.get('our_father', PRAYERS['en']['our_father'])}\n```")
    with st.expander("🌹 Hail Mary (Ave Maria)"):
        st.markdown(f"```\n{prayers.get('hail_mary', PRAYERS['en']['hail_mary'])}\n```")
    with st.expander("✨ Glory Be (Gloria Patri)"):
        st.markdown(f"```\n{prayers.get('glory_be', PRAYERS['en']['glory_be'])}\n```")
    if lang == "en":
        with st.expander("📜 Apostles' Creed"):
            st.markdown(f"```\n{PRAYERS['en']['apostles_creed']}\n```")
        with st.expander("👑 Hail Holy Queen (Salve Regina)"):
            st.markdown(f"```\n{PRAYERS['en']['hail_holy_queen']}\n```")

with tab2:
    st.subheader("📿 The Most Holy Rosary")
    st.info(
        "The Rosary is a Scripture-based prayer that meditates on the life of Christ through Mary. "
        "Begin with the Apostles' Creed, 1 Our Father, 3 Hail Marys, Glory Be, then the 5 decades."
    )
    chosen = st.selectbox("Choose mysteries", list(ROSARY_MYSTERIES.keys()))
    mysteries = ROSARY_MYSTERIES[chosen]
    for i, (name, description) in enumerate(mysteries, 1):
        with st.expander(f"Mystery {i}: {name}"):
            st.write(description)
            st.markdown("**Decade:** 1 Our Father · 10 Hail Marys · 1 Glory Be · Fátima prayer")
    st.markdown("---")
    st.markdown("**Fátima Prayer (after each decade):**")
    st.code("O my Jesus, forgive us our sins, save us from the fires of Hell, "
            "lead all souls to Heaven, especially those most in need of Thy mercy. Amen.")

with tab3:
    st.subheader("🩸 Chaplet of Divine Mercy")
    st.caption("Revealed to Saint Faustina Kowalska · Pray at 3:00 PM (the Hour of Mercy)")
    st.markdown(f"**Opening:**\n\n_{DIVINE_MERCY['Opening']}_")
    st.markdown("---")
    st.code(DIVINE_MERCY["Chaplet_verse"])
    st.markdown("---")
    st.markdown(f"**Closing (3×):**\n\n_{DIVINE_MERCY['Closing']}_")

with tab4:
    st.subheader("✝️ Stations of the Cross")
    st.caption("Pray during Lent and Fridays throughout the year")
    for i, station in enumerate(STATIONS, 1):
        with st.expander(f"Station {i}: {station}"):
            st.markdown(
                f"_We adore You, O Christ, and we praise You._\n\n"
                f"_Because by Your holy cross You have redeemed the world._"
            )
            if i < 14:
                st.caption(f"Meditate on {station.lower()} · Pray: Our Father, Hail Mary, Glory Be")

with tab5:
    st.subheader("🌅 Daily Prayer Rhythm")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Morning Prayer**")
        st.code(
            "Act of Offering:\nO Jesus, through the Immaculate Heart of Mary,\n"
            "I offer You my prayers, works, joys and sufferings of this day\n"
            "for all the intentions of Your Sacred Heart,\nin union with the Holy Sacrifice of the Mass\n"
            "throughout the world, in reparation for my sins,\nfor the intentions of all my associates,\n"
            "and in particular for the intentions of the Holy Father. Amen."
        )
        st.markdown("**Before Meals**")
        st.code("Bless us, O Lord, and these Thy gifts,\nwhich we are about to receive from Thy bounty,\nthrough Christ our Lord. Amen.")
    with col2:
        st.markdown("**Evening Examen (5 minutes)**")
        st.markdown(
            "1. **Gratitude** — Give thanks for the day's gifts\n"
            "2. **Review** — Walk through the day with God\n"
            "3. **Sorrow** — Notice where you fell short\n"
            "4. **Forgiveness** — Ask for mercy\n"
            "5. **Renewal** — Look forward to tomorrow"
        )
        st.markdown("**Night Prayer**")
        st.code(
            "Act of Contrition:\nO my God, I am heartily sorry for having offended Thee,\n"
            "and I detest all my sins because of Thy just punishments,\n"
            "but most of all because they offend Thee, my God,\nwho art all good and deserving of all my love.\n"
            "I firmly resolve, with the help of Thy grace,\nto sin no more and to avoid the near occasions of sin. Amen."
        )

st.divider()
st.caption("📿 Prayers sourced from traditional Catholic tradition | No copyright claimed on liturgical texts")
