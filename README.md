## 유명 영화제의 수상 영화 표시
![[berlin.png]]![[cannes.png]]![[venice.png]]
### 3_awards_page.py - 메뉴에 새 페이지 연결
- contents_search.py에 함수 추가
```
# 영화의 포스터, 평점, 줄거리, 제목, 개봉년도 반환
# 어워드 페이지에서 사용
def get_movie_summary(tmdb_id: int, media_type: str = "movie", lang: str = "ko-KR") -> dict:
    url = f"{BASE_URL}/{media_type}/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "language": lang}
    data = requests.get(url, params=params, timeout=5).json()

    return {
        "poster_path": data.get("poster_path"),
        "vote_average": data.get("vote_average"),
        "overview": data.get("overview", ""),
        "title": data.get("title") or data.get("original_title"),
        "release_date": data.get("release_date", "")
    }
```
- award_winners.db를 직접 작성
>2000 ~ 2025년 칸, 베니스, 베를린 영화제 수상작의 수상년도, 영화명, tmdb id를 관리

1. 로고 이미지를 매핑
2. awards_winners.db에서 필요한 데이터 긁어오기
3. 사이드바에서 년도 선택 가능
>디폴트: 2025년
4. 영화제 로고, 해당 년도의 수상작들의 포스터, 별점, 줄거리 + 바로 main page에서 검색 가능한 버튼 표시
