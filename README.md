# OTT 콘텐츠 검색기
이 프로젝트는 TMDB API를 기반으로 한 OTT 콘텐츠 검색기입니다.
사용자는 영화 및 예능/드라마 정보를 검색하고, 국가별 시청 가능한 OTT 플랫폼과 요금 정보를 확인할 수 있습니다.
또한 MBTI 및 감정 기반 추천 기능, 유사한 영화 추천 기능도 포함되어 있습니다.

---

## 주요 기능

- **OTT 콘텐츠 검색**  
  - TMDB API를 사용해 영화/TV/예능 제목으로 검색  
  - 국가별 스트리밍 제공처(넷플릭스, 왓챠 등) 및 요금 정보 확인  
  - 포스터, 개봉일, 출연진, 러닝타임, 줄거리 등 상세 정보 제공  
- **가성비 계산기**  
  - 사용자가 찜한 콘텐츠 목록을 기반으로  
  - 선택한 국가의 월 구독료, 제공 콘텐츠 수, 사용자 수를 고려해 1인당 콘텐츠당 비용 계산  
  - 테이블과 간단한 막대 그래프로 결과 시각화  
- **MBTI + 감정 기반 추천**  
  - MBTI 유형과 오늘의 기분(이모지)을 선택하여  
  - 사전 정의된 가중치에 따라 장르별 인기 콘텐츠 추천  
  - “자세히 보기” 버튼 클릭 시 해당 콘텐츠 상세 정보로 바로 이동
- **다국어 번역**  
  - `googletrans`를 이용해 제목·줄거리 등 영어 데이터를 한국어, 일본어, 프랑스어 등으로 번역  
- **예고편 미리보기**  
  - TMDB에서 가져온 YouTube 예고편 URL을 `yt-dlp`로 임베드 가능한 형태로 변환  
  - Streamlit 내에서 간단한 플레이어처럼 재생 가능  

---

## 기술 스택

- **프로그래밍 언어**: Python 3.8 이상  
- **웹 프레임워크**: Streamlit  
- **API**: TMDb API (콘텐츠 검색, 예고편, 제공처 조회)  
- **데이터베이스**: SQLite (`ott_prices.db`, `award_winners.db`)  
- **번역 라이브러리**: googletrans  
- **유사 영화 추천 알고리즘**: rapidfuzz  
- **데이터 처리**: pandas  
- **비디오 임베드 변환**: yt-dlp  
- **환경변수 관리**: python-dotenv  

---

## 실행 방법

1. **프로젝트 클론 및 이동**
   ```bash
   git clone <레포지토리_URL>
   cd <프로젝트_폴더>
   ```

2. **가상환경 설정 (선택)**(굳이 필요 X)
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .venv\Scripts\activate.bat       # Windows
   ```

3. **환경변수 설정 (`.env` 파일 생성)**
   ```
   TMDB_API_KEY=<발급받은_API_Key>
   ```
   - `.env` 파일은 프로젝트 루트에 위치해야 합니다.

4. **패키지 설치**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **앱 실행**
   ```bash
   streamlit run home.py
   ```
   - 브라우저가 열리며, 사이드바에서 계산기, MBTI 추천, OTT 검색 페이지로 이동할 수 있습니다.

---

## 디렉토리 구조

```
프로젝트 루트/
├── home.py
├── contents_search.py
├── country_filtering.py
├── recommend_engine.py
├── ott_prices.db
├── static_event_contents.json
├── images/
│   ├── netflix.png
│   ├── watcha.png
│   ├── wavve.png
│   ├── tving.png
│   ├── disneyplus.png
│   ├── apple.png
│   ├── amazon.png
│   ├── google_play_movies.png
│   ├── hulu.png
│   ├── max.png
│   ├── stan.png
│   ├── cannes.png
│   ├── berlin.png
│   └── venice.png
├── .env
├── README.md
├── requirements.txt
└── pages/
    ├── 1_calc_page.py
    └── 2_mbti_page.py

```

- **home.py**: 메인 페이지
- **contents_search.py**: TMDB API 연동 및 데이터 조회 유틸 함수  
- **country_filtering.py**: 국가 목록, 언어 코드 매핑
- **recommend_engine.py**: RapidFuzz 기반 유사 영화 추천
- **ott_prices.db**: 국가별·플랫폼별 요금 정보 SQLite DB
- **images/**: OTT 및 영화제 로고들을 저장해놓은 이미지 폴더  
- **.env**: TMDB API 키 환경변수 파일  
- **requirements.txt**: 프로젝트 의존성 목록  
- **pages/1_calc_page.py**: OTT 가성비 계산기 페이지  
- **pages/2_mbti_page.py**: MBTI + 감정 기반 콘텐츠 추천 페이지  
- **pages/3_mbti_page.py**: 세계 3대 영화제(칸, 베니스, 베를린) 수상작 리스트 페이지 
---
