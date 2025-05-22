import requests
import os
from dotenv import load_dotenv

# ✅ TMDB API 키 불러오기
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

# ✅ 확인할 콘텐츠 ID (예: 인터스텔라 = 157336)
movie_id = 157336
media_type = "movie"  # 또는 "tv"

# ✅ 확인할 국가 코드
country_code = "US"  # KR, JP, CA 등으로 변경 가능

# ✅ TMDB API 요청
url = f"https://api.themoviedb.org/3/{media_type}/{movie_id}/watch/providers"
params = {"api_key": api_key}
response = requests.get(url, params=params)
data = response.json()

# ✅ 결과 출력
print(f"\n📺 [TMDB 기준] {country_code}에서 제공되는 OTT 플랫폼:")
country_data = data.get("results", {}).get(country_code)

if country_data:
    for method in ["flatrate", "rent", "buy"]:
        platforms = country_data.get(method, [])
        if platforms:
            print(f"\n🔹 {method.upper()}")
            for p in platforms:
                print(f"  - {p.get('provider_name')}")
else:
    print("❌ 해당 국가에서는 제공 정보가 없습니다.")
