import sqlite3
import re
from googletrans import Translator

# ✅ 국가 → 언어코드 매핑
country_lang_map = {
    "Korea": "ko",
    "United States": "en",
    "Japan": "ja",
    "France": "fr",
    "Germany": "de",
    "United Kingdom": "en",
    "Brazil": "pt",
    "India": "hi",
    "Australia": "en",
    "Canada": "en"
}

# ✅ DB에서 사용 가능한 국가 목록 불러오기
def get_available_countries():
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT country FROM ott_prices")
        countries = sorted([row[0] for row in cursor.fetchall()])
        conn.close()
        return countries
    except Exception as e:
        print(f"[DB Error] {e}")
        return []

# ✅ 영어 여부 판단
def is_english(text):
    if not text:
        return False
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ 국가에 맞는 언어코드 추출
def get_language_code(country):
    return country_lang_map.get(country, "en")  # 기본값 영어

# ✅ 번역 함수 (영어 → 해당 국가 언어)
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
