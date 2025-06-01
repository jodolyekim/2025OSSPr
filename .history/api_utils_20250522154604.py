import os
from dotenv import load_dotenv
from googletrans import Translator
import streamlit as st
import requests
import re
import asyncio

# 번역기 초기화
translator = Translator()

# 환경 변수 로드 (.env 파일)
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# 🔍 콘텐츠 통합 검색 함수 (영화 + TV)
def search_content_tmdb(title):
    search_url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US",
        "include_adult": False
    }
    response = requests.get(search_url, params=params)
    results = response.json().get("results", [])

    # 영화 또는 TV만 필터링
    filtered = []
    for item in results:
        media_type = item.get("media_type")
        if media_type not in ["movie", "tv"]:
            continue

        title_ko = item.get("title") if media_type == "movie" else item.get("name")
        title_en = item.get("original_title") if media_type == "movie" else item.get("original_name")
        release_date = item.get("release_date") if media_type == "movie" else item.get("first_air_date")
        poster_path = item.get("poster_path")
        content_id = item.get("id")
        overview = item.get("overview", "")
        vote = item.get("vote_average", 0.0)
        trailer = get_trailer_url(content_id, media_type)

        filtered.append({
            "id": content_id,
            "media_type": media_type,
            "title_ko": title_ko,
            "title_en": title_en,
            "poster_path": poster_path,
            "release_date": release_date,
            "vote_average": vote,
            "overview": overview,
            "trailer_url": trailer
        })

    return filtered

# 🎥 예고편 조회 함수 (영화/TV 모두 가능)
def get_trailer_url(content_id, media_type):
    url = f"{BASE_URL}/{media_type}/{content_id}/videos"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            youtube_key = video["key"]
            return f"https://www.youtube.com/watch?v={youtube_key}"
    return None

# 📺 OTT 플랫폼 조회 함수 (영화만 가능 — TV는 지원 안함)
def get_providers(content_id, country_code, media_type):
    if media_type != "movie":
        return {"flatrate": [], "rent": [], "buy": []}  # TV는 제공 안됨

    url = f"{BASE_URL}/movie/{content_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json().get("results", {}).get(country_code, {})

    return {
        "flatrate": [p["provider_name"] for p in data.get("flatrate", [])],
        "rent": [p["provider_name"] for p in data.get("rent", [])],
        "buy": [p["provider_name"] for p in data.get("buy", [])]
    }

# 🌐 영어 → 한글 번역 함수
def translate_to_korean(text):
    if not text:
        return ""
    try:
        result = asyncio.run(translator.translate(text, dest="ko"))
        return result.text
    except Exception as e:
        print(f"[번역 오류] {e}")
        return text

# 🇺🇸 영어 여부 판단 함수
def is_english(text):
    """영문 비율이 60% 이상이면 영어로 간주"""
    if not text:
        return False
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) / max(len(text), 1) > 0.6
