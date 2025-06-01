import os
import sqlite3
import requests
from dotenv import load_dotenv

# ✅ TMDB API 설정
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ OTT 로고 매핑 (images 디렉토리 기준, 모두 소문자 키)
logo_map = {
    "netflix": "images/netflix.png",
    "watcha": "images/watcha.png",
    "wavve": "images/wavve.png",
    "tving": "images/tving.png",
    "disney+": "images/disneyplus.png",
    "apple tv+": "images/apple.png",
    "amazon prime video": "images/amazon.png",
    "google play movies": "images/google_play_movies.png",
    "hulu": "images/hulu.png",
    "max": "images/max.png",
    "stan": "images/stan.png"
}

# ✅ 콘텐츠 검색 (영화, 드라마, 예능 등 통합, 여러 개 반환)
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

    contents = []
    for item in results:
        media_type = item.get("media_type")
        if media_type not in ["movie", "tv"]:
            continue

        title_ko = item.get("title") if media_type == "movie" else item.get("name")
        title_en = item.get("original_title") if media_type == "movie" else item.get("original_name")
        release_date = item.get("release_date") if media_type == "movie" else item.get("first_air_date")

        contents.append({
            "id": item.get("id"),
            "media_type": media_type,
            "title_ko": title_ko,
            "title_en": title_en,
            "poster_path": item.get("poster_path"),
            "release_date": release_date,
            "overview": item.get("overview", ""),
            "vote_average": item.get("vote_average", 0.0)
        })

    return contents

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

# ✅ TMDB 기반 OTT 제공 플랫폼 조회 (소문자 기준 + 대여/구매 가격 포함)
def get_providers(content_id, media_type="movie", country_code='KR'):
    try:
        url = f"{BASE_URL}/{media_type}/{content_id}/watch/providers"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)
        results = response.json().get("results", {})

        country_data = results.get(country_code)
        if not country_data:
            return {}

        provider_dict = {
            "flatrate": [],
            "rent": [],
            "buy": []
        }

        for method in provider_dict:
            for item in country_data.get(method, []):
                name = item.get("provider_name", "").strip().lower()
                price = item.get("retail_price")  # 실질적으로 없음, 미래 확장용
                if name:
                    provider_dict[method].append({
                        "name": name,
                        "price": price
                    })

        return provider_dict
    except Exception as e:
        print(f"[TMDB Provider Error] {e}")
        return {}

# ✅ 구독형 OTT 가격 정보 조회 (DB: ott_prices.db 기준)
def get_ott_price_info(country_name, platform):
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        query = """
            SELECT plan, local_price, price_krw, user_count, has_ads
            FROM ott_prices
            WHERE country_name = ? AND LOWER(platform) = ?
        """
        cursor.execute(query, (country_name, platform.lower()))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB Error] {e}")
        return []
