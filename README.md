안녕하세요 . 현재까지

1. 검색
2. 영화 -> 컨텐츠 확장
3. db로 각 ott별 가격 정리
4. mbti별 추천 기능 추가 + 이모지(오픈소스) 기능을 추가하여 그 날 기분에 따라 추천에 차등을 둠.
5. 번역기능 추가 -> 일어, 불어 등 다양한 언어로 번역 (한국어랑 동시에 보임)
6. 계산기 추가 (pandas 이용, 그래프는 오픈소스 안쓰고 직접 코딩 -> panadas 기능 확장) 그 외에도 광고 유무, 사용자 수에 따른 계산 등 여러 기능 추가
7. 국가 필터링으로 각 국가별로 볼 수 있는 ott랑 가격 추가(가격은 현지 통화로 구성, 한화로 환전 기능도 넣음)
8. 영화 정보 (출연진, 러닝타임 등등) 추가
9. 유튜브 미리보기 추가

이렇게 구성을 해서 깃 브랜치 checkpoint-0523에 올려놓았습니다. 이 파일 다운 받으셔서 작업 부탁드립니다!
어쩌다보니 하다보니 욕심이 생겨서 이것저것 건드렸습니다..! 부디 괜찮길 바라봅니다!
다음주 수요일까지 본인 할 일 하시고 업로드 부탁드려요~




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
