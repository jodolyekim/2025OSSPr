import sqlite3
import re
from deep_translator import GoogleTranslator  # ✅ 변경된 부분

# ✅ OTT 가격 DB에서 사용 가능한 국가 목록 추출
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

# ✅ 영어 비율이 높은지 판단 (TMDB 원제 필터링 등에서 사용 가능)
def is_english(text):
    if not text:
        return False
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ 국가 코드 → 언어 코드 매핑 (Google Translate용)
def get_language_code(country_code):
    mapping = {
        "KR": "ko", "US": "en", "GB": "en", "JP": "ja",
        "FR": "fr", "DE": "de", "BR": "pt", "IN": "hi",
        "AU": "en", "CA": "en", "IT": "it", "CN": "zh-CN",
        "ES": "es", "RU": "ru", "MX": "es", "AR": "es"
    }
    return mapping.get(country_code.upper(), "en")

# ✅ 텍스트를 타겟 언어로 번역 (동기 방식)
def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
