import sqlite3
import re
from googletrans import Translator

# ✅ 전역 번역기 객체
translator = Translator()

# ✅ 사용 가능한 국가 리스트 (DB에서 추출)
def get_available_countries():
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT country_code, country_name FROM ott_prices")
        rows = cursor.fetchall()
        conn.close()
        return {name: code for code, name in sorted(rows, key=lambda x: x[1])}
    except Exception as e:
        print(f"[DB Error] {e}")
        return {}

# ✅ 영어 비율 기준 텍스트 판단
def is_english(text):
    if not text:
        return False
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ 국가 코드 → 언어 코드 매핑 (TMDB 및 번역에 사용)
def get_language_code(country_code):
    mapping = {
        "KR": "ko", "US": "en", "GB": "en", "JP": "ja",
        "FR": "fr", "DE": "de", "BR": "pt", "IN": "hi",
        "AU": "en", "CA": "en"
    }
    return mapping.get(country_code.upper(), "en")

# ✅ 텍스트 번역 (Google Translate API)
def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        result = translator.translate(text, src="en", dest=target_lang)
        return result.text if hasattr(result, "text") else str(result)
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
