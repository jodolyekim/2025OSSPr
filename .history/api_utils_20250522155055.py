import os
import re
import asyncio
import requests
import streamlit as st
from dotenv import load_dotenv
from googletrans import Translator
from justwatch import JustWatch

# 📦 초기 설정
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
translator = Translator()

# 🔍 영화/TV 통합 검색 (TMDB)
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

    # movie, tv만 필터링
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

# 🎞️ 예고편 링크 추출 (movie / tv 공용)
def get_trailer_url(content_id, media_type):
    url = f"{BASE_URL}/{media_type}/{content_id}/videos"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# 🌐 영어 → 한글 번역
def translate_to_korean(text):
    if not text:
        return ""
    try:
        result = asyncio.run(translator.translate(text, dest="ko"))
        return result.text
    except Exception as e:
        print(f"[번역 오류] {e}")
        return text

# 🇺🇸 영어 비율 판단
def is_english(text):
    if not text:
        return False
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) / max(len(text), 1) > 0.6

# 📺 OTT 제공 플랫폼 정보 (JustWatch 사용)
def get_providers_justwatch(title, country_code='KR'):
    justwatch = JustWatch(country=country_code)
    search_results = justwatch.search_for_item(query=title)

    if not search_results.get('items'):
        return []

    item = search_results['items'][0]
    offers = item.get('offers', [])
    provider_set = set()

    for offer in offers:
        provider_id = offer.get("provider_id")
        monetization_type = offer.get("monetization_type")  # flatrate, rent, buy
        provider_info = justwatch.get_provider(provider_id)
        if provider_info:
            name = provider_info.get("clear_name")
            if name:
                provider_set.add((name, monetization_type))

    return list(provider_set)
