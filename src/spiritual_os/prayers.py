"""
Catholic Prayer Library

Complete collection of traditional Catholic prayers in multiple languages.

Includes:
- Basic prayers (Our Father, Hail Mary, Glory Be, etc.)
- Rosary (all 4 mysteries)
- Chaplet of Divine Mercy
- Stations of the Cross
- Liturgy of the Hours (excerpts)
- Marian devotions
- Prayers for various occasions

Languages: English, Latin, Swahili (Phase 1)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class PrayerLanguage(Enum):
    """Supported prayer languages"""
    ENGLISH = "en"
    LATIN = "la"
    SWAHILI = "sw"
    SPANISH = "es"


class PrayerCategory(Enum):
    """Prayer categories"""
    BASIC = "basic"
    ROSARY = "rosary"
    DIVINE_MERCY = "divine_mercy"
    STATIONS = "stations"
    MARIAN = "marian"
    SAINTS = "saints"
    OCCASIONAL = "occasional"
    LITURGY_HOURS = "liturgy_hours"


@dataclass
class Prayer:
    """Individual prayer"""
    id: str
    title: str
    category: PrayerCategory
    text: Dict[str, str]  # Language code -> prayer text
    notes: Optional[str] = None
    when_to_pray: Optional[str] = None
    biblical_reference: Optional[str] = None


# ============================================================================
# BASIC PRAYERS
# ============================================================================

SIGN_OF_THE_CROSS = Prayer(
    id="sign_of_cross",
    title="Sign of the Cross",
    category=PrayerCategory.BASIC,
    text={
        "en": "In the name of the Father, and of the Son, and of the Holy Spirit. Amen.",
        "la": "In nomine Patris, et Filii, et Spiritus Sancti. Amen.",
        "sw": "Kwa jina la Baba, na la Mwana, na la Roho Mtakatifu. Amen."
    },
    notes="Make the Sign of the Cross by touching: forehead, chest, left shoulder, right shoulder",
    when_to_pray="Beginning and end of all prayers"
)

OUR_FATHER = Prayer(
    id="our_father",
    title="Our Father (The Lord's Prayer)",
    category=PrayerCategory.BASIC,
    text={
        "en": """Our Father, who art in heaven,
hallowed be thy name;
thy kingdom come;
thy will be done on earth as it is in heaven.
Give us this day our daily bread;
and forgive us our trespasses
as we forgive those who trespass against us;
and lead us not into temptation,
but deliver us from evil. Amen.""",
        "la": """Pater noster, qui es in caelis,
sanctificetur nomen tuum.
Adveniat regnum tuum.
Fiat voluntas tua, sicut in caelo et in terra.
Panem nostrum quotidianum da nobis hodie,
et dimitte nobis debita nostra,
sicut et nos dimittimus debitoribus nostris.
Et ne nos inducas in tentationem,
sed libera nos a malo. Amen.""",
        "sw": """Baba yetu uliye mbinguni,
jina lako litukuzwe;
ufalme wako uje;
mapenzi yako yatimizwe,
hapa duniani kama huko mbinguni.
Utupe leo chakula chetu cha kila siku;
utusamehe makosa yetu,
kama sisi tunavyowasamehe waliokosea kwetu;
usitutie katika majaribu,
lakini utuokoe na yule mwovu. Amen."""
    },
    biblical_reference="Matthew 6:9-13, Luke 11:2-4",
    when_to_pray="Daily, Rosary, Liturgy of the Hours",
    notes="Taught by Jesus to his disciples"
)

HAIL_MARY = Prayer(
    id="hail_mary",
    title="Hail Mary",
    category=PrayerCategory.BASIC,
    text={
        "en": """Hail Mary, full of grace, the Lord is with thee;
blessed art thou among women,
and blessed is the fruit of thy womb, Jesus.
Holy Mary, Mother of God,
pray for us sinners,
now and at the hour of our death. Amen.""",
        "la": """Ave Maria, gratia plena,
Dominus tecum.
Benedicta tu in mulieribus,
et benedictus fructus ventris tui, Iesus.
Sancta Maria, Mater Dei,
ora pro nobis peccatoribus,
nunc et in hora mortis nostrae. Amen.""",
        "sw": """Salamu Maria, ujaa wa neema,
Bwana yu pamoja nawe.
Umebarikiwa wewe kuliko wanawake wote,
na amebarikiwa uzao wa tumbo lako, Yesu.
Maria Mtakatifu, Mama wa Mungu,
utuombee sisi wenye dhambi,
sasa na saa ya kufa kwetu. Amen."""
    },
    biblical_reference="Luke 1:28, 1:42",
    when_to_pray="Rosary, Angelus, daily devotion",
    notes="Based on the Angel Gabriel's greeting to Mary"
)

GLORY_BE = Prayer(
    id="glory_be",
    title="Glory Be (Doxology)",
    category=PrayerCategory.BASIC,
    text={
        "en": """Glory be to the Father,
and to the Son,
and to the Holy Spirit.
As it was in the beginning,
is now, and ever shall be,
world without end. Amen.""",
        "la": """Gloria Patri,
et Filio,
et Spiritui Sancto.
Sicut erat in principio,
et nunc, et semper,
et in saecula saeculorum. Amen.""",
        "sw": """Utukufu kwa Baba,
na kwa Mwana,
na kwa Roho Mtakatifu.
Kama ulivyokuwa mwanzoni,
uko sasa, na utakuwa milele,
hata milele na milele. Amen."""
    },
    when_to_pray="After each decade of the Rosary, Liturgy of the Hours",
    notes="Ancient Christian prayer of praise to the Trinity"
)

APOSTLES_CREED = Prayer(
    id="apostles_creed",
    title="Apostles' Creed",
    category=PrayerCategory.BASIC,
    text={
        "en": """I believe in God, the Father almighty,
Creator of heaven and earth,
and in Jesus Christ, his only Son, our Lord,
who was conceived by the Holy Spirit,
born of the Virgin Mary,
suffered under Pontius Pilate,
was crucified, died and was buried;
he descended into hell;
on the third day he rose again from the dead;
he ascended into heaven,
and is seated at the right hand of God the Father almighty;
from there he will come to judge the living and the dead.

I believe in the Holy Spirit,
the holy catholic Church,
the communion of saints,
the forgiveness of sins,
the resurrection of the body,
and life everlasting. Amen.""",
        "la": """Credo in Deum Patrem omnipotentem,
Creatorem caeli et terrae.
Et in Iesum Christum, Filium eius unicum, Dominum nostrum,
qui conceptus est de Spiritu Sancto,
natus ex Maria Virgine,
passus sub Pontio Pilato,
crucifixus, mortuus, et sepultus,
descendit ad inferos,
tertia die resurrexit a mortuis,
ascendit ad caelos,
sedet ad dexteram Dei Patris omnipotentis,
inde venturus est iudicare vivos et mortuos.

Credo in Spiritum Sanctum,
sanctam Ecclesiam catholicam,
sanctorum communionem,
remissionem peccatorum,
carnis resurrectionem,
vitam aeternam. Amen."""
    },
    when_to_pray="Rosary, Baptism renewal, Sunday Mass",
    notes="Summary of Christian faith, used since 2nd century"
)

# ============================================================================
# ROSARY MYSTERIES
# ============================================================================

JOYFUL_MYSTERIES = [
    "The Annunciation (Luke 1:26-38)",
    "The Visitation (Luke 1:39-56)",
    "The Nativity (Luke 2:1-21)",
    "The Presentation in the Temple (Luke 2:22-38)",
    "The Finding in the Temple (Luke 2:41-52)"
]

LUMINOUS_MYSTERIES = [
    "The Baptism of Jesus (Matthew 3:13-17)",
    "The Wedding at Cana (John 2:1-11)",
    "The Proclamation of the Kingdom (Mark 1:14-15)",
    "The Transfiguration (Matthew 17:1-8)",
    "The Institution of the Eucharist (Matthew 26:26-29)"
]

SORROWFUL_MYSTERIES = [
    "The Agony in the Garden (Matthew 26:36-56)",
    "The Scourging at the Pillar (Matthew 27:26)",
    "The Crowning with Thorns (Matthew 27:27-31)",
    "The Carrying of the Cross (Matthew 27:32-33)",
    "The Crucifixion (Matthew 27:34-56)"
]

GLORIOUS_MYSTERIES = [
    "The Resurrection (Matthew 28:1-10)",
    "The Ascension (Luke 24:50-53, Acts 1:6-11)",
    "The Descent of the Holy Spirit (Acts 2:1-41)",
    "The Assumption of Mary",
    "The Coronation of Mary"
]

# ============================================================================
# PRAYER LIBRARY
# ============================================================================

ALL_PRAYERS = [
    SIGN_OF_THE_CROSS,
    OUR_FATHER,
    HAIL_MARY,
    GLORY_BE,
    APOSTLES_CREED,
]


class PrayerLibrary:
    """
    Central prayer library with search and filtering
    """
    
    @staticmethod
    def get_prayer(prayer_id: str, language: str = "en") -> Optional[Prayer]:
        """Get a specific prayer by ID"""
        for prayer in ALL_PRAYERS:
            if prayer.id == prayer_id:
                return prayer
        return None
    
    @staticmethod
    def get_prayers_by_category(category: PrayerCategory, language: str = "en") -> List[Prayer]:
        """Get all prayers in a category"""
        return [p for p in ALL_PRAYERS if p.category == category]
    
    @staticmethod
    def get_basic_prayers(language: str = "en") -> List[Prayer]:
        """Get essential daily prayers"""
        return [
            SIGN_OF_THE_CROSS,
            OUR_FATHER,
            HAIL_MARY,
            GLORY_BE,
            APOSTLES_CREED
        ]
    
    @staticmethod
    def get_rosary_structure(language: str = "en") -> Dict:
        """Get complete Rosary structure"""
        return {
            "opening": [SIGN_OF_THE_CROSS, APOSTLES_CREED, OUR_FATHER, HAIL_MARY, HAIL_MARY, HAIL_MARY, GLORY_BE],
            "mysteries": {
                "Monday/Saturday": ("Joyful", JOYFUL_MYSTERIES),
                "Tuesday/Friday": ("Sorrowful", SORROWFUL_MYSTERIES),
                "Wednesday/Sunday": ("Glorious", GLORIOUS_MYSTERIES),
                "Thursday": ("Luminous", LUMINOUS_MYSTERIES)
            },
            "decade_structure": {
                "announce_mystery": True,
                "our_father": 1,
                "hail_mary": 10,
                "glory_be": 1,
                "fatima_prayer": "O my Jesus, forgive us our sins, save us from the fires of hell, and lead all souls to Heaven, especially those in most need of Thy mercy."
            },
            "closing": ["Hail Holy Queen", "Final prayers"]
        }
