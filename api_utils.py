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
        "release_date": movie.get("release_date", "알 수 없음"),
        "vote_average": movie.get("vote_average", 0.0),
        "overview": movie.get("overview", ""),
        "trailer_url": get_trailer_url(movie_id)
    }


# OTT 플랫폼 조회 함수
def get_providers(movie_id, country_code):
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json().get("results", {}).get(country_code, {})

    return {
        "flatrate": [p["provider_name"] for p in data.get("flatrate", [])],
        "rent": [p["provider_name"] for p in data.get("rent", [])],
        "buy": [p["provider_name"] for p in data.get("buy", [])]
    }


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

# 각 국가별 스트리밍, 대여, 구매 정보 반환환
def get_detailed_providers_all(movie_id, country_codes):
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    results = response.json().get("results", {})

    result_by_country = {}
    for code in country_codes:
        info = results.get(code, {})
        result_by_country[code] = {
            "flatrate": [p["provider_name"] for p in info.get("flatrate", [])],
            "rent":     [p["provider_name"] for p in info.get("rent", [])],
            "buy":      [p["provider_name"] for p in info.get("buy", [])]
        }
    return result_by_country

# TMDB API의 추천 영화 찾기
def get_recommendations(movie_id):
    """
    TMDB의 /movie/{movie_id}/recommendations 엔드포인트를 호출하여,
    해당 영화와 유사한 추천 영화 목록(최대 20개 정도)을 반환합니다.
    """
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {
        "api_key": API_KEY,
        "language": "ko-KR"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", [])