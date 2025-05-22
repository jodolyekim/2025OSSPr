import os
import sqlite3
import requests
from dotenv import load_dotenv
import yt_dlp

# ✅ TMDB API 설정
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# ✅ OTT 로고 매핑
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

# ✅ 콘텐츠 검색 (multi)
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

# ✅ 예고편 YouTube 링크 추출
def get_trailer_url(content_id, media_type):
    url = f"{BASE_URL}/{media_type}/{content_id}/videos"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])

    for video in results:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# ✅ yt-dlp로 유튜브 영상 임베드 URL 추출
def get_trailer_embed_url_ytdlp(youtube_url):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best",
            "extract_flat": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return f"https://www.youtube.com/embed/{info['id']}"
    except Exception as e:
        print(f"[yt-dlp Error] {e}")
        return None

# ✅ OTT 플랫폼 조회
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
                price = item.get("retail_price")
                if name:
                    provider_dict[method].append({
                        "name": name,
                        "price": price
                    })

        return provider_dict
    except Exception as e:
        print(f"[TMDB Provider Error] {e}")
        return {}

# ✅ 가격 정보 (DB)
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

# ✅ 제작사 및 출연진 정보 가져오기
def get_details(content_id, media_type, lang="ko"):
    try:
        base_url = f"{BASE_URL}/{media_type}/{content_id}"
        params = {"api_key": TMDB_API_KEY, "language": lang}

        details = requests.get(base_url, params=params).json()
        credits = requests.get(f"{base_url}/credits", params=params).json()

        # 장르, 언어, 제작사 등
        genres = [g["name"] for g in details.get("genres", [])]
        companies = details.get("production_companies", [])
        languages = [l["name"] for l in details.get("spoken_languages", [])]
        homepage = details.get("homepage")
        status = details.get("status")
        tagline = details.get("tagline")
        popularity = details.get("popularity")
        original_language = details.get("original_language")

        # 러닝타임 처리
        if media_type == "movie":
            runtime = details.get("runtime")
            num_seasons = None
            num_episodes = None
        else:
            runtimes = details.get("episode_run_time", [])
            runtime = runtimes[0] if runtimes else None
            num_seasons = details.get("number_of_seasons")
            num_episodes = details.get("number_of_episodes")

        # 출연진 상위 10명
        cast = credits.get("cast", [])[:10]

        return {
            "genres": genres,
            "production_companies": companies,
            "languages": languages,
            "homepage": homepage,
            "status": status,
            "tagline": tagline,
            "popularity": popularity,
            "original_language": original_language,
            "runtime": runtime,
            "number_of_seasons": num_seasons,
            "number_of_episodes": num_episodes,
            "cast": cast
        }

    except Exception as e:
        print(f"[TMDB Details Error] {e}")
        return {}


# ✅ 설명 다국어 병기 (현지언어)
def get_multilang_overview(content_id, media_type, lang_code="en"):
    try:
        url = f"{BASE_URL}/{media_type}/{content_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": lang_code
        }
        response = requests.get(url, params=params)
        return response.json().get("overview", "")
    except Exception as e:
        print(f"[Overview Multilang Error] {e}")
        return ""
