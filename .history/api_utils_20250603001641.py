import os
from dotenv import load_dotenv
from googletrans import Translator
import streamlit as st
import requests
import re

# ✅ 전역 번역기 객체
translator = Translator()

# ✅ API 키 설정
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ 영화 검색 함수
def search_movie_tmdb(title, country):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US"
    }
    response = requests.get(search_url, params=params)
    results = response.json().get("results", [])
    if not results:
        return None

    movie = results[0]
    movie_id = movie["id"]
    title_ko = movie.get("title", "제목 없음")
    title_en = movie.get("original_title", "영문 제목 없음")
    poster_path = movie.get("poster_path")
    trailer_url = get_trailer_url(movie_id)

    return {
        "id": movie_id,
        "title_ko": title_ko,
        "title_en": title_en,
        "poster_path": poster_path,
        "overview": movie.get("overview", ""),
        "trailer_url": trailer_url
    }

# ✅ OTT 플랫폼 조회 함수
def get_providers(movie_id, country_code):
    if not country_code:
        return "전체 OTT 확인 불가"

    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json().get("results", {})
    country_data = data.get(country_code, {})

    providers = country_data.get("flatrate", [])
    provider_names = [p["provider_name"] for p in providers]

    return provider_names if provider_names else "해당 국가에서는 제공되지 않음"

# ✅ 예고편 조회 함수
def get_trailer_url(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            youtube_key = video["key"]
            return f"https://www.youtube.com/watch?v={youtube_key}"
    return None

# ✅ 영어 비율이 높은지 판단 (필요 시 유지)
def is_english(text):
    if not text:
        return False
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ 국가 코드 → 언어 코드 매핑 함수
def get_language_code(country_code):
    mapping = {
        "KR": "ko", "US": "en", "GB": "en", "JP": "ja",
        "FR": "fr", "DE": "de", "BR": "pt", "IN": "hi",
        "AU": "en", "CA": "en", "IT": "it", "CN": "zh-CN",
        "ES": "es", "RU": "ru", "MX": "es", "AR": "es"
    }
    return mapping.get(country_code.upper(), "en")

# ✅ 다국어 자동 번역 함수
def translate_text(text, target_lang):
    if not text:
        return ""
    try:
        result = translator.translate(text, src="auto", dest=target_lang)
        return result.text
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text
