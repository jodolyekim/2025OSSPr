import sqlite3
import re
from googletrans import Translator

# ✅ DB에서 사용 가능한 국가 이름과 코드 가져오기
def get_available_countries():
    try:
        conn = sqlite3.connect("ott_prices (6).db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT country_code, country_name FROM ott_prices")
        rows = cursor.fetchall()
        conn.close()
        # 딕셔너리: {"Korea": "KR", "United States": "US", ...}
        return {name: code for code, name in sorted(rows, key=lambda x: x[1])}
    except Exception as e:
        print(f"[DB Error] {e}")
        return {}

# ✅ 영어 설명 여부 판별
def is_english(text):
    if not text:
        return False
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ 국가코드 → 언어코드 매핑 (필요시 추가 가능)
def get_language_code(country_code):
    mapping = {
        "KR": "ko",
        "US": "en",
        "GB": "en",
        "JP": "ja",
        "FR": "fr",
        "DE": "de",
        "BR": "pt",
        "IN": "hi",
        "AU": "en",
        "CA": "en"
    }
    return mapping.get(country_code.upper(), "en")  # 기본은 영어

# ✅ 번역 함수 (영어 → 대상 언어)
def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        translator = Translator()
        result = translator.translate(text, src="en", dest=target_lang)
        return result.text
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
