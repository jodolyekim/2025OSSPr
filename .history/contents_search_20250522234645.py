import os
import sqlite3
import requests
from dotenv import load_dotenv
from justwatch import JustWatch

# ✅ TMDB API 설정
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ OTT 로고 매핑
logo_map = {
    "Netflix": "images/netflix.png",
    "Watcha": "images/watcha.png",
    "Wavve": "images/wavve.png",
    "Tving": "images/tving.png",
    "Disney+": "images/disneyplus.png",
    "Apple TV+": "images/apple.png",
    "Amazon Prime Video": "images/amazon.png",
    "Google Play Movies": "images/google_play_movies.png",
    "Hulu": "images/hulu.png",
    "Max": "images/max.png",
    "Stan": "images/stan.png"
}

# ✅ TMDB 콘텐츠 통합 검색 (언어 지정 가능)
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

# ✅ JustWatch OTT 제공 플랫폼 조회
def get_providers(title, country_code='KR'):
    supported = ["US", "KR", "JP", "FR", "DE", "GB", "AU", "BR", "CA", "IN"]
    if country_code not in supported:
        print(f"[JustWatch Warning] 국가 코드 {country_code}는 JustWatch에서 지원되지 않음")
        return {}

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
            monetization_type = offer.get("monetization_type")
            provider_info = justwatch.get_provider(provider_id)

            if provider_info and monetization_type in provider_dict:
                provider_name = provider_info.get("clear_name")
                if provider_name and provider_name not in provider_dict[monetization_type]:
                    provider_dict[monetization_type].append(provider_name)

        return provider_dict
    except Exception as e:
        print(f"[JustWatch Error] 해당 국가에서 OTT 정보를 찾을 수 없습니다: {e}")
        return {}


# ✅ OTT 가격 정보 조회 (DB: ott_prices.db 기준)
def get_ott_price_info(country, platform):
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        query = """
            SELECT plan, price_local, price_krw, user_count, has_ads
            FROM ott_prices
            WHERE country = ? AND platform = ?
        """
        cursor.execute(query, (country, platform))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB Error] {e}")
        return []
