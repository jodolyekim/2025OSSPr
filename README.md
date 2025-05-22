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
├── home.py                    # 메인 콘텐츠 검색 페이지
├── pages/
│   ├── 1_calc_page.py         # 가성비 계산기
│   ├── 2_mbti_page.py         # MBTI 추천기
├── contents_search.py        # TMDB 관련 함수 모듈
├── country_filtering.py      # 국가 및 언어 관련 모듈
├── ott_prices.db             # OTT 요금 DB
├── .env                      # API 키 저장
└── README.md
```

---

## ✅ 향후 추가 가능 기능
- 사용자 계정 시스템
- 찜 목록 저장 및 공유
- TMDB 평점 기반 필터링