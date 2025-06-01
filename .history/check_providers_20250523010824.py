import requests
import os
from dotenv import load_dotenv
from collections import defaultdict
import pandas as pd

# API 키 불러오기
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

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

headers = {"Authorization": f"Bearer {api_key}"}
base_url = "https://api.themoviedb.org/3"
popular_ids = []

# 인기 영화 2페이지(40개) 추출
for page in range(1, 3):
    res = requests.get(f"{base_url}/movie/popular", params={"api_key": api_key, "page": page})
    popular_ids += [m["id"] for m in res.json().get("results", [])]

# 국가별 플랫폼 수집
results = defaultdict(set)

for movie_id in popular_ids:
    url = f"{base_url}/movie/{movie_id}/watch/providers"
    res = requests.get(url, params={"api_key": api_key})
    if res.status_code != 200:
        continue
    data = res.json().get("results", {})
    for code in countries.keys():
        for method in ["flatrate", "rent", "buy"]:
            for p in data.get(code, {}).get(method, []):
                results[code].add(p["provider_name"])

# 데이터프레임 변환
rows = [{"국가코드": code, "국가명": countries[code], "플랫폼": name} for code, ps in results.items() for name in ps]
df = pd.DataFrame(rows).sort_values(by=["국가코드", "플랫폼"])
print(df)
