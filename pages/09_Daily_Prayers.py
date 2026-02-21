try:
    from services.settings import get as _get_setting
    _SCRIPTURE_TRANSLATION = _get_setting('scripture_translation') or 'RSVCE'
except Exception:
    _SCRIPTURE_TRANSLATION = 'RSVCE'

"""Daily Prayers — Complete Catholic Prayer Library
Rosary (all 4 mysteries), essential prayers, multilingual."""

import streamlit as st

st.set_page_config(page_title="Daily Prayers", page_icon="🙏", layout="wide")

st.title("🙏 Daily Prayers")
st.caption("Essential Catholic prayers · Rosary · Chaplets · Multilingual")

# ── Today's Readings Banner ────────────────────────────────────────────────────
try:
    from services.lectionary import get_reading
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
    TODAY · {r["season"].upper()} — WEEK {r["week"]} · LITURGICAL YEAR {r["cycle"]}
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
    "fr": {
        "our_father": (
            "Notre Père, qui es aux cieux,\nque ton nom soit sanctifié;\nque ton règne vienne;\n"
            "que ta volonté soit faite sur la terre comme au ciel.\nDonne-nous aujourd'hui notre pain quotidien;\n"
            "pardonne-nous nos offenses,\ncomme nous pardonnons à ceux qui nous ont offensés;\n"
            "et ne nous laisse pas entrer en tentation,\nmais délivre-nous du mal. Amen."
        ),
        "hail_mary": (
            "Je vous salue, Marie, pleine de grâce,\nle Seigneur est avec vous;\nvous êtes bénie entre toutes les femmes,\n"
            "et Jésus, le fruit de vos entrailles, est béni.\nSainte Marie, Mère de Dieu,\n"
            "priez pour nous, pauvres pécheurs,\nmaintenant et à l'heure de notre mort. Amen."
        ),
        "glory_be": (
            "Gloire au Père, et au Fils, et au Saint-Esprit;\n"
            "comme il était au commencement, maintenant et toujours,\ndans les siècles des siècles. Amen."
        ),
    },
    "es": {
        "our_father": (
            "Padre nuestro, que estás en el cielo,\nsantificado sea tu nombre;\nvenga a nosotros tu reino;\n"
            "hágase tu voluntad en la tierra como en el cielo.\nDanos hoy nuestro pan de cada día;\n"
            "y perdona nuestras ofensas,\ncomo también nosotros perdonamos a los que nos ofenden;\n"
            "y no nos dejes caer en la tentación,\ny líbranos del mal. Amén."
        ),
        "hail_mary": (
            "Dios te salve, María, llena eres de gracia,\nel Señor es contigo;\nbendita tú eres entre todas las mujeres,\n"
            "y bendito es el fruto de tu vientre, Jesús.\nSanta María, Madre de Dios,\n"
            "ruega por nosotros, los pecadores,\nahora y en la hora de nuestra muerte. Amén."
        ),
        "glory_be": (
            "Gloria al Padre, y al Hijo, y al Espíritu Santo;\n"
            "como era en el principio, ahora y siempre,\npor los siglos de los siglos. Amén."
        ),
    },
    "pt": {
        "our_father": (
            "Pai nosso, que estais no céu,\nsantificado seja o vosso nome;\nvenha a nós o vosso reino;\n"
            "seja feita a vossa vontade,\nassim na terra como no céu.\nO pão nosso de cada dia nos dai hoje;\n"
            "e perdoai as nossas ofensas,\nassim como nós perdoamos a quem nos tem ofendido;\n"
            "e não nos deixeis cair em tentação,\nmas livrai-nos do mal. Amém."
        ),
        "hail_mary": (
            "Ave Maria, cheia de graça,\no Senhor é convosco;\nbendita sois vós entre as mulheres,\n"
            "e bendito é o fruto do vosso ventre, Jesus.\nSanta Maria, Mãe de Deus,\n"
            "rogai por nós pecadores,\nagora e na hora de nossa morte. Amém."
        ),
        "glory_be": (
            "Glória ao Pai, ao Filho e ao Espírito Santo,\n"
            "como era no princípio, agora e sempre,\npor todos os séculos dos séculos. Amém."
        ),
    },
    "de": {
        "our_father": (
            "Vater unser im Himmel,\ngeheiligt werde dein Name.\nDein Reich komme.\n"
            "Dein Wille geschehe, wie im Himmel, so auf Erden.\nUnser tägliches Brot gib uns heute.\n"
            "Und vergib uns unsere Schuld, wie auch wir vergeben unsern Schuldigern.\n"
            "Und führe uns nicht in Versuchung,\nsondern erlöse uns von dem Bösen. Amen."
        ),
        "hail_mary": (
            "Gegrüßet seist du, Maria, voll der Gnade,\nder Herr ist mit dir;\ndu bist gebenedeit unter den Frauen,\n"
            "und gebenedeit ist die Frucht deines Leibes, Jesus.\nHeilige Maria, Mutter Gottes,\n"
            "bitte für uns Sünder,\njetzt und in der Stunde unseres Todes. Amen."
        ),
        "glory_be": (
            "Ehre sei dem Vater und dem Sohn und dem Heiligen Geist,\n"
            "wie es war im Anfang, jetzt und in Ewigkeit,\nvon Ewigkeit zu Ewigkeit. Amen."
        ),
    },
    "tl": {
        "our_father": (
            "Ama namin, sumasalangit ka,\nsambahin ang ngalan mo.\nMapasakamin ang kaharian mo.\n"
            "Sundin ang loob mo, dito sa lupa para nang sa langit.\nBigyan mo kami ngayon ng aming kakanin sa araw-araw.\n"
            "At patawarin mo kami sa aming mga sala,\npara nang pagpapatawad namin sa nagkakasala sa amin.\n"
            "At huwag mo kaming ipahintulot sa tukso,\nkundi iligtas mo kami sa lahat ng masama. Amen."
        ),
        "hail_mary": (
            "Aba Ginoong Maria, napupuno ka ng grasya,\nang Panginoon ay nasa iyo;\nbukod kang pinagpala sa babaeng lahat,\n"
            "at pinagpala rin ang iyong anak na si Hesus.\nSanta Mariang Ina ng Diyos,\n"
            "ipanalangin mo kaming mga makasalanan,\ngayon at kung kami'y mamamatay. Amen."
        ),
        "glory_be": (
            "Luwalhati sa Ama, at sa Anak, at sa Espiritu Santo;\n"
            "kagaya noong una, ngayon at magpakailan man,\nmagpakailanman. Amen."
        ),
    },
    "it": {
        "our_father": (
            "Padre nostro, che sei nei cieli,\nsia santificato il tuo nome;\nvenga il tuo regno;\n"
            "sia fatta la tua volontà, come in cielo così in terra.\nDacci oggi il nostro pane quotidiano;\n"
            "e rimetti a noi i nostri debiti,\ncome noi li rimettiamo ai nostri debitori;\n"
            "e non indurci in tentazione,\nma liberaci dal male. Amen."
        ),
        "hail_mary": (
            "Ave Maria, piena di grazia,\nil Signore è con te;\ntu sei benedetta fra le donne\n"
            "e benedetto è il frutto del tuo seno, Gesù.\nSanta Maria, Madre di Dio,\n"
            "prega per noi peccatori,\nadesso e nell'ora della nostra morte. Amen."
        ),
        "glory_be": (
            "Gloria al Padre e al Figlio e allo Spirito Santo,\n"
            "come era nel principio e ora e sempre,\nnei secoli dei secoli. Amen."
        ),
    },
    "ig": {
        "our_father": (
            "Nna anyị, biri n'elu igwe,\nka aha gị dị nsọ;\nka alaeze gị bịa;\n"
            "ka ọchịchọ gị mee n'ụwa, dị ka ọ dị n'elu igwe.\nNye anyị taa nri anyị nke ụbọchị a;\n"
            "wepụ mmehie anyị,\ndị ka anyị si ewepụ nke ndị metụtara anyị;\n"
            "ekwela ka anyị banye n'ọnọdụ nnwale,\nkama zọpụta anyị n'ihe ọjọọ. Amen."
        ),
        "hail_mary": (
            "Nsọpụrụ gị, Mariam, ọ zụ gị ojii ọma,\nOnye Nwe anyị nọ n'ebe i nọ;\nọ dụọ gị ngọzi n'etiti ụmụnwanyị nile,\n"
            "a họpụtara ọ dụọ ngọzi mkpụrụ afọ gị, Jizọs.\nOnye nso Mariam, Nne Chukwu,\n"
            "biko kpee anyị ndị nwere mmehie ekpere,\nugbu a na n'oge ọnwụ anyị. Amen."
        ),
        "glory_be": (
            "Otuto dị ka Nna, na Nwa, na Mmụọ Nsọ;\n"
            "dị ka ọ dị n'oge mbido, ugbu a na mgbe nile,\nwe rue mgbe ebighi ebi. Amen."
        ),
    },
}

def _fmt(text: str) -> str:
    """Render prayer text as readable italic markdown with line breaks."""
    lines = text.strip().split("\n")
    return "\n\n".join(f"*{line}*" if line.strip() else "" for line in lines)

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
lang_map = {
    "English": "en",
    "Kiswahili": "sw",
    "Luganda": "lg",
    "Français": "fr",
    "Español": "es",
    "Português": "pt",
    "Deutsch": "de",
    "Tagalog": "tl",
    "Italiano": "it",
    "Igbo": "ig",
}
lang_display = st.sidebar.selectbox("🌍 Language / Lugha", list(lang_map.keys()))
lang = lang_map[lang_display]
prayers = PRAYERS.get(lang, PRAYERS["en"])

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📿 Essential Prayers", "📿 The Rosary", "🩸 Divine Mercy", "✝️ Stations", "🌅 Daily Rhythm"]
)

with tab1:
    lang_native = {
        "English": "Essential Catholic Prayers",
        "Kiswahili": "Sala za Kikatoliki",
        "Luganda": "Emiwoowo egy'Ekikatoli",
        "Français": "Prières Catholiques Essentielles",
        "Español": "Oraciones Católicas Esenciales",
        "Português": "Orações Católicas Essenciais",
        "Deutsch": "Grundlegende Katholische Gebete",
        "Tagalog": "Mga Pangunahing Panalangin",
        "Italiano": "Preghiere Cattoliche Fondamentali",
        "Igbo": "Ekpere Ndị Katọlik",
    }.get(lang_display, "Essential Catholic Prayers")
    st.subheader(f"{lang_native}")
    if lang_display != "English":
        st.caption(f"Prayers in {lang_display} · Rosary, Divine Mercy and Stations shown in English")
    with st.expander("🙏 Our Father (Pater Noster)", expanded=True):
        st.markdown(_fmt(prayers.get('our_father', PRAYERS['en']['our_father'])))
    with st.expander("🌹 Hail Mary (Ave Maria)"):
        st.markdown(_fmt(prayers.get('hail_mary', PRAYERS['en']['hail_mary'])))
    with st.expander("✨ Glory Be (Gloria Patri)"):
        st.markdown(_fmt(prayers.get('glory_be', PRAYERS['en']['glory_be'])))
    if lang == "en":
        with st.expander("📜 Apostles' Creed"):
            st.markdown(_fmt(PRAYERS['en']['apostles_creed']))
        with st.expander("👑 Hail Holy Queen (Salve Regina)"):
            st.markdown(_fmt(PRAYERS['en']['hail_holy_queen']))

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
                "_We adore You, O Christ, and we praise You._\n\n"
                "_Because by Your holy cross You have redeemed the world._"
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
