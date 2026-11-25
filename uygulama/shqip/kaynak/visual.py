# Visual layer: unit icons/colours, extra pictures for words, story covers and character avatars.
# Picture codes: emoji | "#hex" colour | "n:12" number | "cal:Pzt" calendar page | "sym:?" big symbol tile
UNIT_LOOK = {  # id: (icon, hue)
 "selam": ("👋", 350), "hal": ("🤝", 20), "zamir": ("🙋", 200), "aile": ("👨‍👩‍👧", 330), "sayi": ("🔢", 210),
 "renk": ("🎨", 280), "meyve": ("🍎", 5), "hayvan": ("🦅", 30), "gun": ("📅", 190), "zaman": ("⏰", 220),
 "mevsim": ("🌦️", 170), "ev": ("🏠", 25), "okul": ("🏫", 45), "icecek": ("☕", 30), "ulke": ("🌍", 160),
 "fiil": ("🏃", 260), "sifat": ("✨", 300), "cumle": ("💬", 345), "faleminderit": ("🙏", 40), "festa": ("🎉", 320),
 "ndjenja": ("💞", 340), "trupi": ("🧍", 15), "doktor": ("🩺", 180), "pazar": ("🛒", 140), "plazh": ("🏖️", 195),
 "pyetje": ("❓", 230), "lidhezat": ("🔗", 250), "koha-shkuar": ("⏪", 270), "shquar": ("📘", 215), "mbiemra": ("⚖️", 290),
 "karakteri": ("🦉", 35), "te-afermit": ("👪", 325), "proverba": ("📜", 40), "telefoni": ("📱", 205),
 "rutina": ("⏰", 30), "veshje": ("👕", 285), "ushqim": ("🍲", 15), "qyteti": ("🏙️", 210), "transport": ("🚌", 45),
 "puna": ("💼", 240), "hobi": ("⚽", 120), "shendeti": ("💊", 175), "blerje": ("🛍️", 330), "udhetim": ("🧳", 195),
 "koha2": ("⏳", 260), "kundersi": ("☯️", 300), "fiilet2": ("🤲", 20), "teknologji": ("📱", 220), "natyra": ("🌲", 130),
 "festat": ("🎊", 350), "kosova": ("🇽🇰", 215),
}
EXTRA_PICS = {
 "Ju lutem": "🥺", "S'ka përse": "😊", "Më falni": "😅", "Shihemi nesër": "📅", "Si je?": "🙂", "Jo keq": "👌", "Po ti?": "🫵",
 "Si quhesh?": "🏷️", "Unë quhem Ana": "🙋‍♀️", "Nga je?": "🗺️", "Sa vjeç je?": "🎂", "ju": "👥", "ata": "👨‍👨‍👦", "unë jam": "🙋",
 "ti je": "👉", "ai është": "👨", "ne jemi": "👥", "ata janë": "👨‍👩‍👦", "xhaxha": "👨‍🦳", "teze": "👩‍🦱",
 "e hënë": "cal:Pzt", "e martë": "cal:Sal", "e mërkurë": "cal:Çar", "e enjte": "cal:Per", "e premte": "cal:Cum", "e shtunë": "cal:Cmt",
 "e diel": "cal:Paz", "vit": "🗓️", "sot": "cal:Bugün", "dje": "cal:Dün", "nesër": "cal:Yarın", "tavolinë": "🪵", "jastëk": "🛌", "çati": "🏘️",
 "klasë": "🧑‍🏫", "fjalë": "🔤", "shqip": "🇦🇱", "turqisht": "🇹🇷", "anglisht": "🇬🇧", "vij": "🚶", "i ri": "🐣", "i vjetër": "👴",
 "Ç'po bën?": "🤔", "Ku po shkon?": "🧭", "Do të vij nesër": "📆", "Ju falënderoj": "🙏", "Urdhëroni": "🤲", "Faleminderit për ndihmën": "🤝",
 "qafë": "🦒", "bark": "🫃", "shpinë": "🧍", "Ku ju dhemb?": "🤕", "Më dhemb barku": "🤢", "Keni…?": "🛍️", "lekë": "🪙", "madhësi": "📏",
 "Ku është arka?": "🧾", "rërë": "🏝️", "peshqir": "🧺", "çadër": "⛱️", "Kush?": "sym:?", "Çfarë?": "sym:?", "Si?": "sym:?", "Sa?": "sym:#",
 "Nga?": "🧭", "Cili?": "👈", "Kur vjen?": "⏰", "Çfarë do?": "🤲", "dhe": "sym:+", "ose": "sym:/", "por": "sym:↔", "sepse": "sym:∵",
 "nëse": "sym:?→", "që": "sym:…", "kur": "⏱️", "edhe": "sym:+1", "prandaj": "sym:⇒", "pastaj": "sym:→", "Jam i lodhur, por i lumtur": "😮‍💨",
 "Nuk vij sepse jam i sëmurë": "🤒", "shkova": "🚶", "erdha": "🏃", "piva": "🥤", "bëra": "🛠️", "fola": "🗣️", "punova": "💼",
 "Dje shkova në punë": "🏢", "Ai erdhi vonë": "⌛", "djalë i mirë": "👦", "vajzë e mirë": "👧", "i gjatë": "🦒", "e gjatë": "🦒",
 "i shkurtër": "🐁", "i varfër": "🪫", "i vështirë": "🧗", "i ndyrë": "🧹", "i sjellshëm": "🎩", "i ndershëm": "🤞", "i durueshëm": "🧘",
 "koprrac": "🔒", "krenar": "🦚", "kunat": "🧔", "kunatë": "👩", "vjehërr": "👴", "vjehrrë": "👵", "nipi": "👦", "mbesa": "👧",
 "stërgjysh": "🧓", "Sa vëllezër ke?": "👬", "Cili është numri yt?": "☎️", "Numri im është…": "🔢", "Alo, kush flet?": "📞", "Do të të telefonoj": "📲",
}
STORY_LOOK = {  # story id: cover scene
 "klasa": "🏫✏️📚", "familja": "👨‍👩‍👧‍👦🏠", "kafe": "☕🍦🧾", "qindarka": "🍨🪙👦", "lypsari": "🧓🤝🚶",
 "talesi": "🏛️🦉📜", "dyqani": "🍎🍇⚖️", "plazhi": "🏖️🌊🍦", "mjeku": "🩺💊🤒", "ataturku": "🇹🇷📜🕊️",
}
AVATARS = {  # speaker name -> avatar emoji
 "Mësuesja": "👩‍🏫", "Nxënësit": "🧒", "Arbeni": "👦", "Arturi": "🧑", "Dritani": "👦🏻", "Kamerieri": "🧑‍🍳", "Kamerierja": "👩‍🍳",
 "Ana": "👩", "Artani": "👨", "Recepsionisti": "🧑‍💼", "Shoferi": "🧔", "Pula": "🐔", "Shqiponja": "🦅", "Djali": "👦", "Unë": "🙂", "Lypësi": "🧓", "Talesi": "🧙", "Shitësi": "🧔", "Mjeku": "👨‍⚕️", "Pacienti": "🤒",
}

FEMALE = {"Mësuesja", "Kamerierja", "Ana", "Pula", "Shqiponja"}   # story speakers voiced by the female voice
