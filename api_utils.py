import os
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# 영화 검색 함수
def search_movie_tmdb(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "ko-KR"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
        if "results" in data and data["results"]:
            first = data["results"][0]
            return {
                "id": first.get("id"),
                "title_ko": first.get("title", ""),
                "title_en": first.get("original_title", ""),
                "poster_path": first.get("poster_path", "")
            }
    except Exception as e:
        st.error(f"API 응답 처리 중 오류 발생: {e}")

    return None

# OTT 플랫폼 조회 함수
def get_providers(movie_id, country_code):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    country_data = data.get("results", {}).get(country_code, {})
    return [p["provider_name"] for p in country_data.get("flatrate", [])]

# 대여, 구매 가능한 곳도 같이 출력
def get_detailed_providers(movie_id, country_code):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    country_data = data.get("results", {}).get(country_code, {})

    return {
        "stream": [p["provider_name"] for p in country_data.get("flatrate", [])],
        "rent": [p["provider_name"] for p in country_data.get("rent", [])],
        "buy": [p["provider_name"] for p in country_data.get("buy", [])]
    }

# 추천 영화
def get_recommendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {
        "api_key": API_KEY,
        "language": "ko-KR"
    }
    
    response = requests.get(url, params = params)
    data = response.json()
    
    return data.get("results", [])

# 다른 국가 OTT에서 시청 가능한 경우
def get_detailed_providers_all(movie_id, country_codes):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("results", {})
    result_by_country = {}

    for code in country_codes:
        info = results.get(code, {})
        if info:
            result_by_country[code] = {
                "link": info.get("link"),
                "flatrate": [p["provider_name"] for p in info.get("flatrate", [])],
                "rent": [p["provider_name"] for p in info.get("rent", [])],
                "buy": [p["provider_name"] for p in info.get("buy", [])]
            }

    return result_by_country