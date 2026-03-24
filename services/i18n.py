"""
Internationalisation (i18n) — Jumuia — Parish Community
======================================================
UI string translations for major Catholic-population languages.

Languages selected by Catholic population density + regional reach:
  en  — English         (global default)
  es  — Spanish         (Latin America — 425M Catholics)
  pt  — Portuguese      (Brazil, Mozambique, Angola — 175M)
  fr  — French          (West/Central Africa, France — 80M)
  sw  — Kiswahili       (East Africa — Kenya, Tanzania, Uganda)
  tl  — Tagalog         (Philippines — 85M Catholics, 3rd largest)
  ig  — Igbo            (Nigeria — 25M Catholics)
  hi  — Hindi           (India — 19M Catholics)
  pl  — Polish          (Poland, diaspora — 33M)
  it  — Italian         (Italy, diaspora — 35M)
  ar  — Arabic          (Middle East/North Africa Catholics)
  lg  — Luganda         (Uganda — 15M Catholics)

Usage:
    from services.i18n import t, lang_selector
    lang_selector()          # renders the selectbox in sidebar
    t("find_church")         # returns translated string
"""

import streamlit as st

# ── Language registry ─────────────────────────────────────────────────────────
LANGUAGES = {
    "en": "English",
    "es": "Español",
    "pt": "Português",
    "fr": "Français",
    "sw": "Kiswahili",
    "tl": "Tagalog",
    "ig": "Igbo",
    "hi": "हिन्दी",
    "pl": "Polski",
    "it": "Italiano",
    "de": "Deutsch",
    "ar": "العربية",
    "lg": "Luganda",
    "sv": "Svenska",
}

# ── Translation strings ───────────────────────────────────────────────────────
# Structure: STRINGS[key][lang_code] = translated string
STRINGS: dict[str, dict[str, str]] = {

    # ── Sidebar navigation ────────────────────────────────────────────────────
    "nav_parishioners": {
        "en": "For Parishioners",
        "es": "Para Feligreses",
        "pt": "Para Paroquianos",
        "fr": "Pour les Fidèles",
        "sw": "Kwa Waumini",
        "tl": "Para sa mga Parokiano",
        "ig": "Maka ndị Ọchịchọ",
        "hi": "पैरिशियनों के लिए",
        "pl": "Dla Parafian",
        "it": "Per i Parrocchiani",
        "de": "Für Pfarrmitglieder",
        "ar": "للمؤمنين",
        "lg": "Ababiri b'ekkanisa",
        "sv": "För församlingsbor",
    },
    "nav_coordinators": {
        "en": "Parish Coordinators",
        "es": "Coordinadores",
        "pt": "Coordenadores",
        "fr": "Coordinateurs",
        "sw": "Waratibu wa Parokia",
        "tl": "Mga Koordinador",
        "ig": "Ndị Nhazi Ọchịchọ",
        "hi": "पैरिश समन्वयक",
        "pl": "Koordynatorzy",
        "it": "Coordinatori",
        "de": "Pfarrkoordinatoren",
        "ar": "منسقو الرعية",
        "lg": "Abakulembeze",
        "sv": "Församlingskoordinatorer",
    },
    "nav_more": {
        "en": "More Tools",
        "es": "Más Herramientas",
        "pt": "Mais Ferramentas",
        "fr": "Plus d'Outils",
        "sw": "Zana Zaidi",
        "tl": "Mga Karagdagang Kasangkapan",
        "ig": "Ngwa ndị ọzọ",
        "hi": "और उपकरण",
        "pl": "Więcej Narzędzi",
        "it": "Altri Strumenti",
        "de": "Weitere Tools",
        "ar": "أدوات إضافية",
        "lg": "Ebikozesebwa ebirala",
        "sv": "Fler verktyg",
    },

    # ── Page titles ───────────────────────────────────────────────────────────
    "find_church": {
        "en": "Find a Church",
        "es": "Encontrar una Iglesia",
        "pt": "Encontrar uma Igreja",
        "fr": "Trouver une Église",
        "sw": "Tafuta Kanisa",
        "tl": "Humanap ng Simbahan",
        "ig": "Chọọ Ụlọ Ụka",
        "hi": "चर्च खोजें",
        "pl": "Znajdź Kościół",
        "it": "Trova una Chiesa",
        "ar": "ابحث عن كنيسة",
        "lg": "Nonya Ekkanisa",
        "sv": "Hitta en kyrka",
    },
    "daily_prayers": {
        "en": "Daily Prayers",
        "es": "Oraciones Diarias",
        "pt": "Orações Diárias",
        "fr": "Prières Quotidiennes",
        "sw": "Sala za Kila Siku",
        "tl": "Pang-araw-araw na Panalangin",
        "ig": "Ekpere Ụbọchị",
        "hi": "दैनिक प्रार्थनाएं",
        "pl": "Codzienne Modlitwy",
        "it": "Preghiere Quotidiane",
        "de": "Tägliche Lesungen & Gebete",
        "ar": "الصلوات اليومية",
        "lg": "Okusaba olwa buli lunaku",
        "sv": "Dagliga böner",
    },
    "ai_assistant": {
        "en": "AI Assistant",
        "es": "Asistente IA",
        "pt": "Assistente IA",
        "fr": "Assistant IA",
        "sw": "Msaidizi wa AI",
        "tl": "AI Katulong",
        "ig": "Onye Enyemaka AI",
        "hi": "AI सहायक",
        "pl": "Asystent AI",
        "it": "Assistente IA",
        "de": "KI-Assistent",
        "ar": "المساعد الذكي",
        "lg": "Omuyambi wa AI",
        "sv": "AI-assistent",
    },

    # ── Home page ─────────────────────────────────────────────────────────────
    "home_subtitle": {
        "en": "Find your church · Follow the daily readings · Ask a question in any language",
        "es": "Encuentra tu iglesia · Sigue las lecturas diarias · Pregunta en cualquier idioma",
        "pt": "Encontre sua igreja · Siga as leituras diárias · Pergunte em qualquer idioma",
        "fr": "Trouvez votre église · Suivez les lectures · Posez une question dans n'importe quelle langue",
        "sw": "Tafuta kanisa lako · Fuata masomo ya kila siku · Uliza swali kwa lugha yoyote",
        "tl": "Hanapin ang iyong simbahan · Sundan ang pang-araw-araw na pagbasa · Magtanong sa anumang wika",
        "ig": "Chọọ ụlọ ụka gị · Soro ihe ọgụgụ · Jụọ ajụjụ n'asụsụ ọ bụla",
        "hi": "अपना चर्च खोजें · दैनिक पाठ का पालन करें · किसी भी भाषा में प्रश्न पूछें",
        "pl": "Znajdź swój kościół · Śledź codzienne czytania · Zadaj pytanie w dowolnym języku",
        "it": "Trova la tua chiesa · Segui le letture quotidiane · Fai una domanda in qualsiasi lingua",
        "ar": "ابحث عن كنيستك · تابع القراءات اليومية · اطرح سؤالاً بأي لغة",
        "lg": "Nonya ekkanisa lyo · Goberera ebibuuzo bya buli lunaku · Buuza ekibuuzo mu lulimi lw'okwagala",
    },
    "verse": {
        "en": "\"Whatever you did for the least of these, you did for me.\" — Matthew 25:40",
        "es": "«Lo que hicieron por uno de estos hermanos míos más pequeños, por mí lo hicieron.» — Mateo 25:40",
        "pt": "«O que fizestes a um destes meus irmãos mais pequeninos, foi a mim que o fizestes.» — Mateus 25:40",
        "fr": "«Ce que vous avez fait à l'un de ces plus petits, c'est à moi que vous l'avez fait.» — Matthieu 25:40",
        "sw": "«Mlichofanya kwa mmoja wa hawa ndugu zangu wadogo, mlifanya kwangu.» — Mathayo 25:40",
        "tl": "«Ang ginawa ninyo sa isa sa pinakamaliit na mga ito, sa akin ninyo ginawa.» — Mateo 25:40",
        "ig": "«Ihe ọ bụla ị mere maka otu n'ime ụmụnne m ndị nta ndị a, i mere ya maka m.» — Matiu 25:40",
        "hi": "«जो तुमने इन मेरे भाइयों में से किसी एक के लिए किया, मेरे लिए किया।» — मत्ती 25:40",
        "pl": "«Cokolwiek uczyniliście jednemu z tych braci moich najmniejszych, Mnie uczyniliście.» — Mateusz 25:40",
        "it": "«Tutto quello che avete fatto a uno solo di questi miei fratelli più piccoli, l'avete fatto a me.» — Matteo 25:40",
        "ar": "«ما فعلتموه لأحد إخوتي هؤلاء الصغار، فلي فعلتموه.» — متى 25:40",
        "lg": "«Kye mwakola eri omu ku ab'oluganda bange abalala aba nteege, kwankola eri nze.» — Matayo 25:40",
    },

    # ── Common actions ────────────────────────────────────────────────────────
    "search": {
        "en": "Search", "es": "Buscar", "pt": "Pesquisar", "fr": "Rechercher",
        "sw": "Tafuta", "tl": "Maghanap", "ig": "Chọọ", "hi": "खोजें",
        "pl": "Szukaj", "it": "Cerca", "ar": "بحث", "lg": "Noonya",
        "sv": "Sök",
    },
    "save": {
        "en": "Save", "es": "Guardar", "pt": "Salvar", "fr": "Enregistrer",
        "sw": "Hifadhi", "tl": "I-save", "ig": "Chekwaa", "hi": "सहेजें",
        "pl": "Zapisz", "it": "Salva", "ar": "حفظ", "lg": "Tereka",
        "sv": "Spara",
    },
    "close": {
        "en": "Close", "es": "Cerrar", "pt": "Fechar", "fr": "Fermer",
        "sw": "Funga", "tl": "Isara", "ig": "Mechie", "hi": "बंद करें",
        "pl": "Zamknij", "it": "Chiudi", "ar": "إغلاق", "lg": "Ggalawo",
    },
    "today": {
        "en": "Today", "es": "Hoy", "pt": "Hoje", "fr": "Aujourd'hui",
        "sw": "Leo", "tl": "Ngayon", "ig": "Taa", "hi": "आज",
        "pl": "Dziś", "it": "Oggi", "ar": "اليوم", "lg": "Leero",
        "sv": "Idag",
    },

    # ── USSD footer ───────────────────────────────────────────────────────────
    "ussd_label": {
        "en": "Basic phone access",
        "es": "Acceso desde teléfono básico",
        "pt": "Acesso por telefone básico",
        "fr": "Accès téléphone de base",
        "sw": "Simu ya kawaida",
        "tl": "Access sa basic na telepono",
        "ig": "Ọbụna n'ekwenti dị mfe",
        "hi": "बेसिक फोन पर उपलब्ध",
        "pl": "Dostęp z telefonu podstawowego",
        "it": "Accesso da telefono base",
        "ar": "وصول عبر الهاتف العادي",
        "lg": "Okukozesa simu enyangu",
        "sv": "Grundtelefonåtkomst",
    },
    "ussd_hint": {
        "en": "Available once your diocese registers with Africa's Talking. See More Tools → Set Up USSD",
        "es": "Disponible cuando su diócesis se registre con Africa's Talking.",
        "pt": "Disponível quando sua diocese se registrar na Africa's Talking.",
        "fr": "Disponible quand votre diocèse s'inscrit chez Africa's Talking.",
        "sw": "Inapatikana baada ya dayosisi yako kusajiliwa na Africa's Talking.",
        "tl": "Available kapag nagrehistro na ang inyong diyosesis sa Africa's Talking.",
        "ig": "Dị maka mgbe dayọsis gị debanyere aha na Africa's Talking.",
        "hi": "जब आपका डायोसीस Africa's Talking में पंजीकृत हो जाएगा।",
        "pl": "Dostępne gdy diecezja zarejestruje się w Africa's Talking.",
        "it": "Disponibile quando la diocesi si registra con Africa's Talking.",
        "ar": "متاح عند تسجيل أبرشيتك مع Africa's Talking.",
        "lg": "Ejja ng'edayosizi yo egyegamba ne Africa's Talking.",
        "sv": "Tillgänglig när din stift registrerar sig hos Africa's Talking.",
    },
}


# ── Public API ────────────────────────────────────────────────────────────────

def get_lang() -> str:
    """Return current language code from session state. Default: 'en'."""
    return st.session_state.get("ui_lang", "en")


def t(key: str) -> str:
    """Translate a string key to current UI language. Falls back to English."""
    lang = get_lang()
    strings = STRINGS.get(key, {})
    return strings.get(lang) or strings.get("en") or key


def lang_selector():
    """Render compact language selector. Call inside a st.sidebar context."""
    current = get_lang()

    st.markdown(
        "<div style='font-size:0.65rem;color:rgba(255,255,255,0.45);"
        "text-transform:uppercase;letter-spacing:0.08em;"
        "margin-bottom:0.2rem;margin-top:0.75rem;'>🌐 Language / Lugha</div>",
        unsafe_allow_html=True
    )
    lang_labels = list(LANGUAGES.values())
    lang_codes  = list(LANGUAGES.keys())
    selected_label = st.selectbox(
        "Language",
        lang_labels,
        index=lang_codes.index(current),
        label_visibility="collapsed",
        key="lang_selector_widget"
    )
    new_code = lang_codes[lang_labels.index(selected_label)]
    if new_code != current:
        st.session_state["ui_lang"] = new_code
        st.rerun()
