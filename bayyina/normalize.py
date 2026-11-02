import re

def normalize_ar(text: str) -> str:
    """
    Normalizes Arabic/English text per spec rules:
    - Removes U+064B–U+0652 (tashkeel) and U+0670 (dagger alif)
    - Removes tatweel U+0640
    - Maps electro-arabic/persian digits: ٠-٩ and ۰-۹ -> 0-9
    - Maps hamzas: أ, إ, آ -> ا
    - Maps ة -> ه and ى -> ي
    - Lowercases text
    - Collapses runs of whitespace to a single space and strips ends
    - Preserves ؤ and ئ
    """
    if not text:
        return ""

    # Remove tashkeel (U+064B-U+0652) and dagger alif (U+0670)
    text = re.sub(r'[\u064B-\u0652\u0670]', '', text)
    
    # Remove tatweel (U+0640)
    text = re.sub(r'\u0640', '', text)

    # Map Eastern Arabic & Persian digits to ASCII 0-9
    digit_map = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
    text = text.translate(digit_map)

    # Map hamzas: أ, إ, آ -> ا
    text = re.sub(r'[\u0622\u0623\u0625]', '\u0627', text)

    # Map ة -> ه and ى -> ي
    text = text.replace('\u0629', '\u0647').replace('\u0649', '\u064A')

    # Lowercase
    text = text.lower()

    # Collapse runs of whitespace and strip
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def tokenize(text: str) -> list[str]:
    """
    Normalizes text first, then extracts all Unicode word matches (\\w+).
    Franco tokens like 'sha7en' stay intact.
    """
    normalized = normalize_ar(text)
    return re.findall(r'\w+', normalized)