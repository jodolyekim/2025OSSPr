# 2025OSSPr
2025OSSPr
# 🎬 OTT 어디있니?

> “OTT 어디있니?”는 TMDB(The Movie Database) API를 활용해 사용자가 입력한 영화 제목을 기반으로, 해당 영화가 어느 OTT(구독·스트리밍) 플랫폼에서 제공되는지 알려주는 Streamlit  기반의 웹 애플리케이션입니다.  
> 또한 대여(Rent), 구매(Buy) 가능한 플랫폼 정보와 다른 국가(US, GB, JP, AU)에서의 스트리밍 정보, 그리고 추천 영화(Recommendations) 목록까지 함께 제공합니다.

---

## 프로젝트 개요

“OTT 어디있니?”는 사용자가 검색창에 영화 제목을 입력하면,  
1. 해당 영화의 TMDB 메타정보(제목, 포스터, 개요, 평점 등)  
2. 선택한 국가에서 **구독+스트리밍(Flatrate)** 가능한 플랫폼  
3. 선택한 국가에서 **대여(Rent)** 및 **구매(Buy)** 가능한 플랫폼  
4. 미국(US), 영국(GB), 일본(JP), 호주(AU) 등 **다른 국가별 스트리밍** 플랫폼  
5. 해당 영화와 유사한 **추천 영화** 목록 (최대 5개)  

를 한 화면에서 한눈에 확인할 수 있도록 도와줍니다.  
한국어/영어 제목, 포스터 이미지, 평점, 예고편(YouTube) 삽입 기능도 포함되어 있습니다.

---

## 주요 기능

- **영화 검색**  
  - TMDB API를 통해 사용자가 입력한 영화 제목을 검색  
  - 한국어/영어 제목, 포스터, 개요(Overview), 개봉일, 평점 등 메타정보 출력  
  - 개요가 영어로 제공되는 경우 자동 한글 번역(구글 번역 API 연동)  

- **국가별 OTT 정보**  
  - 사용자가 선택한 국가(한국, 미국, 영국, 캐나다, 호주)에서 구독(Flatrate), 대여(Rent), 구매(Buy) 가능한 플랫폼 목록 출력  
  - 각 플랫폼별 로고(Netflix, Watcha, Wavve, Disney+, Apple, Amazon, Hulu, Max, Stan, Google Play Movies 등) 함께 표시  

- **다른 국가 스트리밍 정보**  
  - 미국(US), 영국(GB), 일본(JP), 호주(AU)에서 **구독(Flatrate)** 가능한 플랫폼 목록 출력  

- **추천 영화(Recommendations)**  
  - TMDB의 Recommendations API를 통해, 검색된 영화와 유사한 영화 목록(최대 5개) 출력  
  - 각 추천 영화의 포스터, 제목, 개요, 평점 표시  

---

## 폴더 구조

```text
.
├── .env                 # TMDB API Key 등 환경 변수를 저장하는 파일
├── .gitignore
├── README.md            # (이 파일)
├── api_utils.py         # TMDB API 호출 함수 모음
├── country_filtering.py # Streamlit용 국가 선택 UI 함수
├── ott_ui_app.py        # 메인 Streamlit 앱
├── api_infos.txt        # (참고용) API 엔드포인트 및 정보 정리 텍스트
├── logo_images/         # OTT 플랫폼 로고 아이콘 이미지 디렉터리
└──── netflix.png
   ├── watcha.png
   ├── wavve.png
   ├── disneyplus.png
   ├── apple.png
   ├── amazon.png
   ├── hulu.png
   ├── max.png
   ├── stan.png
   └── google_play_movies.png

