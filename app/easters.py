"""Bengali easters & Sharodiya soul for Pujo Atlas API responses.

Central catalogue so backend (FastAPI) and frontend (index.html)
share the same Bengali voice. All strings are additive / non-breaking:
they ride along as extra JSON fields + X- headers, never replacing
core data.
"""

from __future__ import annotations

import datetime
import random
from typing import Optional

SHARODIYA_SUBHECHHA = "শারদীয়া শুভেচ্ছা! পুজো ভালো কাটুক।"

PROVERBS = [
    "আসছে বছর আবার হবে!",
    "ঢাকের তালে কোমর দোলে!",
    "পুজো মানে পাড়া, পাড়া মানে আপন!",
    "ভোরের পুষ্পাঞ্জলি, সন্ধ্যার ধুনো!",
    "ভিড় হবে, মন ভরবে!",
    "মা আসছেন — পথ ছাড়ো!",
    "কাশফুল দুললেই মন পুজো-পুজো করে!",
]

# Search-triggered easters: key -> Bengali toast/message.
# Keep keys lowercase, stripped. Supports both English transliteration
# and Bengali script.
EASTER_MAP = {
    # Dhaak — the heartbeat
    "dhaak": "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে! 🥁",
    "dhak": "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে! 🥁",
    "dhaaker kathi": "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে! 🥁",
    "ঢাক": "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে! 🥁",
    # Adda / para life
    "adda": "পাড়ার মোড়ে আড্ডা — চা হাতে ঠাকুর দেখা! ☕",
    "আড্ডা": "পাড়ার মোড়ে আড্ডা — চা হাতে ঠাকুর দেখা! ☕",
    "para": "পাড়ার পুজোই আসল পুজো — ফাঁকায় ঠাকুর দেখুন! 🏘️",
    "পাড়া": "পাড়ার পুজোই আসল পুজো — ফাঁকায় ঠাকুর দেখুন! 🏘️",
    # Mishti
    "mishti": "মিষ্টি মুখ করুন! শুভ শারদীয়া। 🍬",
    "misti": "মিষ্টি মুখ করুন! শুভ শারদীয়া। 🍬",
    "মিষ্টি": "মিষ্টি মুখ করুন! শুভ শারদীয়া। 🍬",
    "roshogolla": "রসগোল্লা না খেলে পুজো অসম্পূর্ণ! শুভ শারদীয়া।",
    "রসগোল্লা": "রসগোল্লা না খেলে পুজো অসম্পূর্ণ! শুভ শারদীয়া।",
    "sandesh": "সন্দেশ হাতে বনেদি বাড়ির উঠোনে বসুন।",
    # Dugga / Maa
    "dugga": "বলো দুগ্গা মাঈ কী — জয়! 🙏",
    "durga": "বলো দুগ্গা মাঈ কী — জয়! 🙏",
    "দুর্গা": "বলো দুগ্গা মাঈ কী — জয়! 🙏",
    "দুগ্গা": "বলো দুগ্গা মাঈ কী — জয়! 🙏",
    "maa aschen": "মা আসছেন — আগমনীর সুরে কাশফুল দোলে! 🌾",
    "agomoni": "আগমনীর সুর বাজছে — মা আসছেন! 🌾",
    "আগমনী": "আগমনীর সুর বাজছে — মা আসছেন! 🌾",
    # Mahalaya / tithis
    "mahalaya": "মহালয়ার ভোরে বীরেন্দ্রকৃষ্ণ — পুজো আসছে! 📻",
    "মহালয়া": "মহালয়ার ভোরে বীরেন্দ্রকৃষ্ণ — পুজো আসছে! 📻",
    "panchami": "পঞ্চমীতেই উদ্বোধনের ভিড় — জুতো সেলাই থেকে চণ্ডীপাঠ!",
    "shashti": "ষষ্ঠীতে বোধন — মায়ের ঘুম ভাঙে আজ! 🔔",
    "ষষ্ঠী": "ষষ্ঠীতে বোধন — মায়ের ঘুম ভাঙে আজ! 🔔",
    "saptami": "শুভ সপ্তমী! সকালে অঞ্জলি, বিকেলে ঘোরা। 🌼",
    "সপ্তমী": "শুভ সপ্তমী! সকালে অঞ্জলি, বিকেলে ঘোরা। 🌼",
    "ashtami": "শুভ অষ্টমী! পুষ্পাঞ্জলি আর খিচুড়ি ভোগ। 🙏🍛",
    "অষ্টমী": "শুভ অষ্টমী! পুষ্পাঞ্জলি আর খিচুড়ি ভোগ। 🙏🍛",
    "sandhi pujo": "সন্ধিপুজোর ৪৮ মিনিট — প্রদীপের আলোয় মায়ের চক্ষুদান!",
    "navami": "শুভ নবমী! আজ রাত জেগে ঠাকুর দেখার রাত। 🌙",
    "নবমী": "শুভ নবমী! আজ রাত জেগে ঠাকুর দেখার রাত। 🌙",
    "dashami": "শুভ বিজয়া! আসছে বছর আবার হবে। ❤️",
    "দশমী": "শুভ বিজয়া! আসছে বছর আবার হবে। ❤️",
    "bijoya": "শুভ বিজয়া! মিষ্টিমুখ আর প্রণাম। 🙏",
    "বিজয়া": "শুভ বিজয়া! মিষ্টিমুখ আর প্রণাম। 🙏",
    "bhasan": "ভাসানের ঢাক — চোখে জল, মুখে হাসি। আসছে বছর আবার হবে!",
    # Rituals
    "sindoor khela": "সিঁদুর খেলায় রাঙা দশমী — বলো দুগ্গা মাঈ কী জয়! 🔴",
    "সিঁদুর খেলা": "সিঁদুর খেলায় রাঙা দশমী — বলো দুগ্গা মাঈ কী জয়! 🔴",
    "sindoor": "সিঁদুর খেলায় রাঙা দশমী — বলো দুগ্গা মাঈ কী জয়! 🔴",
    "dhunuchi": "ধুনুচি নাচের ধোঁয়ায় সন্ধ্যা নামে! 🔥",
    "ধুনুচি": "ধুনুচি নাচের ধোঁয়ায় সন্ধ্যা নামে! 🔥",
    "dhunuchi naach": "ধুনুচি নাচের ধোঁয়ায় সন্ধ্যা নামে! 🔥",
    "pushpanjali": "ভোরের পুষ্পাঞ্জলি — ফুল, বেলপাতা আর মন্ত্রে মন ভরে! 🌸",
    "anjali": "ভোরের পুষ্পাঞ্জলি — ফুল, বেলপাতা আর মন্ত্রে মন ভরে! 🌸",
    "অঞ্জলি": "ভোরের পুষ্পাঞ্জলি — ফুল, বেলপাতা আর মন্ত্রে মন ভরে! 🌸",
    "bhog": "খিচুড়ি ভোগ আর লাবড়া — পুজোর আসল স্বাদ! 🍛",
    "ভোগ": "খিচুড়ি ভোগ আর লাবড়া — পুজোর আসল স্বাদ! 🍛",
    "khichuri": "খিচুড়ি ভোগ আর লাবড়া — পুজোর আসল স্বাদ! 🍛",
    # Nature of Sharod
    "kashful": "কাশফুল দুলছে — মা আসছেন! 🌾",
    "kash phool": "কাশফুল দুলছে — মা আসছেন! 🌾",
    "কাশফুল": "কাশফুল দুলছে — মা আসছেন! 🌾",
    "shiuli": "শিউলি ফুলের গন্ধে ভোরের পুজো! 🤍",
    "শিউলি": "শিউলি ফুলের গন্ধে ভোরের পুজো! 🤍",
    "sharat": "শরতের নীল আকাশে সাদা মেঘ — পুজো এসে গেছে! ☁️",
    # Kolkata icons
    "tram": "ট্রামে চেপে উত্তর থেকে দক্ষিণ — ধীরে চলো, পুজো দেখো! 🚋",
    "addaa": "পাড়ার মোড়ে আড্ডা — চা হাতে ঠাকুর দেখা! ☕",
    "kumartuli": "কুমারটুলির মাটির গন্ধে মায়ের চক্ষুদান! 👁️",
    "কুমারটুলি": "কুমারটুলির মাটির গন্ধে মায়ের চক্ষুদান! 👁️",
    "chokkhu daan": "চক্ষুদান না হলে মা দেখেন না — মহালয়ার পর কুমারটুলি যান!",
    "alpona": "আলপনার সাদা দাগে উঠোন সাজে! 〰️",
    "alpana": "আলপনার সাদা দাগে উঠোন সাজে! 〰️",
    "আলপনা": "আলপনার সাদা দাগে উঠোন সাজে! 〰️",
    "shankha": "শঙ্খে ফুঁ পড়েছে — সন্ধ্যারতি শুরু! 🐚",
    "uloo": "উলুধ্বনিতে মুখর পাড়া — জয় মা দুর্গা! 🙌",
    "bonedi": "বনেদি বাড়ির ঠাকুরদালানে একবার বসুন — সকালেই প্রাণ! 🏛️",
    "বনেদি": "বনেদি বাড়ির ঠাকুরদালানে একবার বসুন — সকালেই প্রাণ! 🏛️",
    "thakur dalan": "ঠাকুরদালানের ঝাড়বাতির নিচে সন্ধ্যা নামে!",
    # Love
    "bhalobasa": "ভালোবাসা থেকে কলকাতা! ❤️",
    "ভালোবাসা": "ভালোবাসা থেকে কলকাতা! ❤️",
    "kolkata": "কলকাতা মানে পুজো, পুজো মানে কলকাতা! ❤️",
    "howrah bridge": "হাওড়া ব্রিজের আলোয় ভাসছে গঙ্গা — পুজো এসেছে!",
}

# Petal-shower worthy words (frontend confetti triggers, mirrored in API)
PETAL_WORDS = {"bhalobasa", "ভালোবাসা", "dugga", "দুর্গা", "durga", "bijoya", "বিজয়া", "agomoni"}


def normalize_search_term(raw: str | None) -> str:
    if not raw:
        return ""
    return raw.strip().lower()


def get_easter_for_search(search: str | None) -> Optional[str]:
    """Return Bengali easter message for a search term, if any."""
    key = normalize_search_term(search)
    if not key:
        return None
    # exact match first
    if key in EASTER_MAP:
        return EASTER_MAP[key]
    # substring match: e.g. "dhaak beats" should still hit
    for k, v in EASTER_MAP.items():
        if k and (k in key or key in k):
            return v
    return None


def is_petal_word(search: str | None) -> bool:
    return normalize_search_term(search) in PETAL_WORDS


def get_subhechha_now() -> str:
    """Season-aware Sharodiya greeting based on today's date."""
    now = datetime.datetime.now()
    m, d = now.month, now.day
    if m == 10 and 9 <= d <= 13:
        return "শুভ সপ্তমী-অষ্টমী-নবমী! বলো দুগ্গা মাঈ কী — জয়!"
    if m == 10:
        return "শারদীয়া শুভেচ্ছা! পুজো ভালো কাটুক।"
    if m == 9:
        return "মহালয়ার শুভেচ্ছা — মা আসছেন! কাশফুল দুলছে।"
    return SHARODIYA_SUBHECHHA


def get_random_proverb() -> str:
    return random.choice(PROVERBS)


def get_pujo_tip(popularity: str = "", category: str = "", bonedi: bool = False,
                 district: str = "") -> str:
    """Per-pandal Bengali tip based on its character."""
    if bonedi or (category or "") == "bonedi_bari":
        return "বনেদি টিপ: সকালে যান, শাড়ি-পাঞ্জাবিতে — ঠাকুরদালানেই প্রাণ।"
    if (popularity or "") == "popular":
        return "ভিড়ের টিপ: ভোরে যান — ভিড় কম, আলো সুন্দর। জল সঙ্গে রাখুন!"
    # para / quiet
    tips = [
        "পাড়ার টিপ: সন্ধ্যায় ধুনোর গন্ধে বসুন, পুষ্পাঞ্জলিতে যোগ দিন।",
        "ফাঁকায় ঠাকুর দেখুন, পাড়ার মিষ্টির দোকানটা জিজ্ঞেস করুন!",
        "ধুনোর গন্ধে জিরিয়ে নিন — আড্ডায় বসুন।",
    ]
    idx = (len(district or "") + len(category or "")) % len(tips)
    return tips[idx]


def get_district_greeting(district: str | None) -> Optional[str]:
    if not district:
        return None
    d = district.strip().lower()
    mapping = {
        "nadia": "কল্যাণীর আলোর থিম মিস করবেন না! ✨",
        "hoogly": "গুপ্তিপাড়ার বারোয়ারি — বাংলার প্রথম কমিউনিটি পুজো! 🙏",
        "kolkata": "উত্তর থেকে দক্ষিণ — ট্রামে চেপে ঘুরুন! 🚋",
        "darjeeling": "পাহাড়ে পুজো — ম্যালে সন্ধ্যারতি! ⛰️",
        "cooch behar": "বড় দেবীর রাজবাড়ি — ৫০০ বছরের ঐতিহ্য! 👑",
        "bankura": "বিষ্ণুপুরের মৃন্ময়ী — ৯৯৭ সালের মন্দির পুজো! 🛕",
        "birbhum": "শান্তিনিকেতনের সুরে পুজো — সুরুল রাজবাড়ি ঘুরুন!",
        "murshidabad": "হাজারদুয়ারির ছায়ায় রাজবাড়ির পুজো!",
    }
    for k, v in mapping.items():
        if k in d:
            return v
    return None


# ---- ASCII-safe HTTP headers (headers must be latin-1) ----
# JSON bodies carry full Bengali script; headers carry transliteration.
HEADER_SUBHECHHA = "Sharodiya Shubhechha! Pujo bhalo katuk."
HEADER_PROVERBS = [
    "Asche bochor abar hobe!",
    "Dhaker taale komor dole!",
    "Pujo mane para, para mane apon!",
    "Bhorer pushpanjali, sondhyar dhuno!",
    "Bhir hobe, mon bhorbe!",
    "Maa aschen - poth charo!",
    "Kashful dullei mon pujo-pujo kore!",
]


def get_header_subhechha() -> str:
    return HEADER_SUBHECHHA


def get_header_proverb() -> str:
    return random.choice(HEADER_PROVERBS)


def to_ascii_header(text: str | None, fallback: str = "Bolo Dugga Mai ki - Joy!") -> str:
    """Encode any Bengali easter into an ASCII-safe header value.

    Uses unicode-escape so the header stays latin-1 while remaining
    decodable; falls back to a transliterated greeting.
    """
    if not text:
        return fallback
    try:
        text.encode("latin-1")
        return text
    except UnicodeEncodeError:
        return text.encode("unicode_escape").decode("ascii")
