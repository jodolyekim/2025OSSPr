import os
import sqlite3
import requests
from dotenv import load_dotenv

# ✅ TMDB API 설정
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ OTT 로고 매핑 (images 디렉토리 기준)
logo_map = {
    "Netflix": "images/netflix.png",
    "Watcha": "images/watcha.png",
    "Wavve": "images/wavve.png",
    "Tving": "images/tving.png",
    "Disney Plus": "images/disneyplus.png",
    "Apple TV Plus": "images/apple.png",
    "Amazon Prime Video": "images/amazon.png",
    "Google Play Movies": "images/google_play_movies.png",
    "Hulu": "images/hulu.png",
    "Max": "images/max.png",
    "Stan": "images/stan.png"
}

# ✅ 콘텐츠 검색 (영화, 드라마, 예능 등 통합)
def search_movie_tmdb(title, lang="ko"):
    search_url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": lang,
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

# ✅ 예고편 YouTube 링크 추출 (movie / tv 공용)
def get_trailer_url(content_id, media_type):
    url = f"{BASE_URL}/{media_type}/{content_id}/videos"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# ✅ TMDB 기반 OTT 제공 플랫폼 조회 (구독, 대여, 구매 구분)
def get_providers(content_id, media_type="movie", country_code='KR'):
    try:
        url = f"{BASE_URL}/{media_type}/{content_id}/watch/providers"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)
        results = response.json().get("results", {})

        country_data = results.get(country_code)
        if not country_data:
            return {}

        provider_dict = {"flatrate": [], "rent": [], "buy": []}
        for key in provider_dict:
            for provider in country_data.get(key, []):
                name = provider.get("provider_name")
                if name and name not in provider_dict[key]:
                    provider_dict[key].append(name)
        return provider_dict
    except Exception as e:
        print(f"[TMDB Provider Error] {e}")
        return {}

# ✅ OTT 가격 정보 조회 (오직 구독형만 DB에서 조회)
def get_ott_price_info(country_name, platform):
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        query = """
            SELECT plan, local_price, price_krw, user_count, has_ads
            FROM ott_prices
            WHERE country_name = ? AND platform = ?
        """
        cursor.execute(query, (country_name, platform))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB Error] {e}")
        return []
