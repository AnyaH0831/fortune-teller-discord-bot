from datetime import date

ZODIAC_SIGNS = [
    ("Capricorn",  (12, 22), (1,  19)),
    ("Aquarius",   (1,  20), (2,  18)),
    ("Pisces",     (2,  19), (3,  20)),
    ("Aries",      (3,  21), (4,  19)),
    ("Taurus",     (4,  20), (5,  20)),
    ("Gemini",     (5,  21), (6,  20)),
    ("Cancer",     (6,  21), (7,  22)),
    ("Leo",        (7,  23), (8,  22)),
    ("Virgo",      (8,  23), (9,  22)),
    ("Libra",      (9,  23), (10, 22)),
    ("Scorpio",    (10, 23), (11, 21)),
    ("Sagittarius",(11, 22), (12, 21)),
    ("Capricorn",  (12, 22), (12, 31)),
]

SIGN_EMOJIS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

def get_zodiac_sign(month: int, day: int) -> str:
    """Returns the zodiac sign for a given month and day."""
    for sign, (start_m, start_d), (end_m, end_d) in ZODIAC_SIGNS:
        if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
            return sign
    return "Unknown"

def get_sign_emoji(sign: str) -> str:
    return SIGN_EMOJIS.get(sign.capitalize(), "⭐")