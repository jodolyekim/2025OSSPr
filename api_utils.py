import os
from dotenv import load_dotenv
from googletrans import Translator
import streamlit as st
import requests
import re

translator = Translator()

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# 영화 검색 함수
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
        "trailer_url": get_trailer_url(movie_id)
    }


# OTT 플랫폼 조회 함수
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

# 예고편 조회 함수
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

# 영화 소개 번역 함수
def translate_to_korean(text):
    if not text:
        return ""
    result = translator.translate(text, dest="ko")
    return result.text

def is_english(text):
    """영문 비율이 60% 이상이면 영어로 간주"""
    if not text:
        return False
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) / max(len(text), 1) > 0.6