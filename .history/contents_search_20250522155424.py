import os
import re
import asyncio
import requests
from dotenv import load_dotenv
from googletrans import Translator
from justwatch import JustWatch

# 📦 초기 설정
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
translator = Translator()

# ✅ 영화/TV 통합 검색 (UI용 이름: search_movie_tmdb)
def search_movie_tmdb(title, country='KR'):
    search_url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US",
        "include_adult": False
    }
    response = requests.get(search_url, params=params)
    results = response.json().get("results", [])

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

        return {
            "id": content_id,
            "media_type": media_type,
            "title_ko": title_ko,
            "title_en": title_en,
            "poster_path": poster_path,
            "release_date": release_date,
            "vote_average": vote,
            "overview": overview,
            "trailer_url": trailer
        }

    return None

# ✅ 예고편 링크 추출 (movie / tv 공용)
def get_trailer_url(content_id, media_type):
    url = f"{BASE_URL}/{media_type}/{content_id}/videos"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# ✅ 영어 → 한글 번역
def translate_to_korean(text):
    if not text:
        return ""
    try:
        result = asyncio.run(translator.translate(text, dest="ko"))
        return result.text
    except Exception as e:
        print(f"[번역 오류] {e}")
        return text

# ✅ 영어 비율 판단
def is_english(text):
    if not text:
        return False
    letters = re.findall(r'[a-zA-Z]', text)
    return len(letters) / max(len(text), 1) > 0.6

# ✅ OTT 제공 플랫폼 조회 (UI에서 get_providers로 사용)
def get_providers(title, country_code='KR'):
    try:
        justwatch = JustWatch(country=country_code)
        search_results = justwatch.search_for_item(query=title)

        if not search_results.get('items'):
            return {}

        item = search_results['items'][0]
        offers = item.get('offers', [])
        provider_dict = {"flatrate": [], "rent": [], "buy": []}

        for offer in offers:
            provider_id = offer.get("provider_id")
            monetization_type = offer.get("monetization_type")  # flatrate, rent, buy
            provider_info = justwatch.get_provider(provider_id)

            if provider_info and monetization_type in provider_dict:
                provider_name = provider_info.get("clear_name")
                if provider_name and provider_name not in provider_dict[monetization_type]:
                    provider_dict[monetization_type].append(provider_name)

        return provider_dict
    except Exception as e:
        print(f"[JustWatch Error] {e}")
        return {}
