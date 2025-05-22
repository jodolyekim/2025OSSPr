import requests
import os
from dotenv import load_dotenv

# ✅ TMDB API 키 불러오기
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

# ✅ 확인할 콘텐츠 정보
movie_id = 157336  # Interstellar
media_type = "movie"

# ✅ 확인할 10개국 코드
countries = {
    "KR": "한국",
    "US": "미국",
    "JP": "일본",
    "FR": "프랑스",
    "DE": "독일",
    "GB": "영국",
    "CA": "캐나다",
    "AU": "호주",
    "BR": "브라질",
    "IN": "인도"
}

# ✅ TMDB API 요청 URL
url = f"https://api.themoviedb.org/3/{media_type}/{movie_id}/watch/providers"
params = {"api_key": api_key}
response = requests.get(url, params=params)
data = response.json()

# ✅ 결과 출력
for code, name in countries.items():
    print(f"\n📺 [{name}] {code} 국가에서 제공되는 OTT 플랫폼:")
    country_data = data.get("results", {}).get(code)

    if country_data:
        found_any = False
        for method in ["flatrate", "rent", "buy"]:
            platforms = country_data.get(method, [])
            if platforms:
                found_any = True
                label = {
                    "flatrate": "구독형",
                    "rent": "대여",
                    "buy": "구매"
                }[method]
                print(f"\n🔹 {label}")
                for p in platforms:
                    print(f"  - {p.get('provider_name')}")
        if not found_any:
            print("  ❌ 제공 플랫폼 없음")
    else:
        print("  ❌ TMDB 제공 정보 없음")
