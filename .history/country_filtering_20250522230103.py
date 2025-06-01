import sqlite3
import re
from googletrans import Translator

translator = Translator()  # 전역에서 단 1회만 생성

def get_available_countries():
    try:
        conn = sqlite3.connect("ott_prices (6).db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT country_code, country_name FROM ott_prices")
        rows = cursor.fetchall()
        conn.close()
        return {name: code for code, name in sorted(rows, key=lambda x: x[1])}
    except Exception as e:
        print(f"[DB Error] {e}")
        return {}

def is_english(text):
    if not text:
        return False
    letters = re.findall(r"[a-zA-Z]", text)
    return len(letters) / max(len(text), 1) > 0.6

def get_language_code(country_code):
    mapping = {
        "KR": "ko", "US": "en", "GB": "en", "JP": "ja", "FR": "fr",
        "DE": "de", "BR": "pt", "IN": "hi", "AU": "en", "CA": "en"
    }
    return mapping.get(country_code.upper(), "en")

def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        result = translator.translate(text, src="en", dest=target_lang)
        return result.text
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
