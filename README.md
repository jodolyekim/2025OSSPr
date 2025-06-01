구현된 기능

1. 검색
2. 영화 -> 컨텐츠 확장
3. db로 각 ott별 가격 정리
4. mbti별 추천 기능 추가 + 이모지(오픈소스) 기능을 추가하여 그 날 기분에 따라 추천에 차등을 둠.
5. 번역기능 추가 -> 일어, 불어 등 다양한 언어로 번역 (한국어랑 동시에 보임)
6. 계산기 추가 (pandas 이용, 그래프는 오픈소스 안쓰고 직접 코딩 -> panadas 기능 확장) 그 외에도 광고 유무, 사용자 수에 따른 계산 등 여러 기능 추가
7. 국가 필터링으로 각 국가별로 볼 수 있는 ott랑 가격 추가(가격은 현지 통화로 구성, 한화로 환전 기능도 넣음)
8. 영화 정보 (출연진, 러닝타임 등등) 추가
9. 유튜브 미리보기 추가
10. 기념일 추천 컨텐츠 🆕




# 🎬 OTT 콘텐츠 검색기 (요금 + 설명 번역 지원)

이 프로젝트는 TMDB API를 기반으로 한 OTT 콘텐츠 검색기입니다. 사용자는 영화 및 예능/드라마 정보를 검색하고, 국가별 시청 가능 OTT 플랫폼과 요금 정보를 확인할 수 있습니다. 또한 MBTI 및 감정 기반 추천 기능도 탑재되어 있습니다.

---

## 📌 주요 기능

### 🔍 콘텐츠 검색
- 영화 및 드라마/예능을 검색하여 결과를 보여줍니다.
- 국가별 OTT 제공 플랫폼, 가격 정보 제공 (정가 및 광고 여부 포함).
- 유튜브 예고편 임베딩 지원.

### 🧠 MBTI 기반 추천기
- 사용자 MBTI 및 감정 이모지 입력을 바탕으로 관련 장르 추천.
- 각 장르별 인기 콘텐츠를 TMDB에서 불러와 추천.
- 추천된 영화 상세정보 보기 기능.

### 📊 가성비 계산기
- 최대 10개의 콘텐츠를 찜하여 어떤 OTT가 가장 가성비 좋은지 시각적으로 비교합니다.

### 📅 기념일 콘텐츠 추천 (🆕)
- 사용자가 날짜를 선택하면, 해당 날짜가 삼일절·현충일·크리스마스 등 국가 기념일일 경우 추천 콘텐츠 자동 출력
- 추천 콘텐츠는 JSON 파일에 정적으로 저장되어 있어 빠르게 로딩되며, 영화·드라마 등 다양한 포맷 지원
- 관련 파일: `event_contents.py`, `static_event_contents.json`


---

## 🛠️ 기술 스택

- Python 3.9+
- Streamlit
- Requests
- dotenv
- TMDB API (The Movie Database)
- Google Translate (선택적)
- SQLite (OTT 요금 DB)

---

## 🚀 실행 방법

1. 가상환경 설정 (선택사항)
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows는 .venv\Scripts\activate
    ```

2. 패키지 설치
    ```bash
    pip install -r requirements.txt
    ```

3. `.env` 파일 생성 및 API 키 저장
    ```env
    TMDB_API_KEY=your_tmdb_key
    ```

4. 앱 실행
    ```bash
    streamlit run home.py
    ```

---

## 📁 디렉토리 구조

```
📦 2025OSSPr-feature-frontend-ui
├── home.py # 메인 콘텐츠 검색 페이지
├── pages/
│ ├── 1_calc_page.py # 가성비 계산기
│ ├── 2_mbti_page.py # MBTI 추천기
├── contents_search.py # TMDB 관련 함수 모듈
├── country_filtering.py # 국가 및 언어 관련 모듈
├── event_contents.py # 기념일 추천 콘텐츠 처리 모듈 🆕
├── static_event_contents.json # 기념일별 추천 콘텐츠 데이터 🆕
├── ott_prices.db # OTT 요금 DB
├── .env # API 키 저장
└── README.md
```

---

## ✅ 향후 추가 가능 기능
- 사용자 계정 시스템
- 찜 목록 저장 및 공유
- TMDB 평점 기반 필터링
