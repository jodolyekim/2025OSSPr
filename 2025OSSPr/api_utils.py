import os
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()
API_KEY = os.getenv("TDMB_API_KEY")

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