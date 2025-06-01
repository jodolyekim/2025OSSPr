# pages/1_mbti_page.py

import streamlit as st
from collections import Counter
import requests
import os
from dotenv import load_dotenv
from contents_search import get_details, get_trailer_url, get_multilang_overview

# ✅ TMDB API 키 로드
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ✅ 장르 이름 ↔ 장르 ID
genre_name_to_id = {
    "Action": 28, "Adventure": 12, "Animation": 16,
    "Comedy": 35, "Drama": 18, "Fantasy": 14,
    "Mystery": 9648, "Romance": 10749, "Thriller": 53,
    "Documentary": 99, "Family": 10751, "History": 36,
}

# ✅ MBTI별 추천 장르
mbti_genres_map = {
    "INFP": ["Fantasy", "Drama", "Romance"],
    "ENFP": ["Comedy", "Adventure", "Romance"],
    "INFJ": ["Drama", "Mystery", "Fantasy"],
    "ENFJ": ["Drama", "Documentary", "Romance"],
    "INTP": ["Documentary", "Mystery", "Drama"],
    "ENTP": ["Comedy", "Adventure", "Action"],
    "INTJ": ["Thriller", "Mystery", "Drama"],
    "ENTJ": ["Action", "Thriller", "Documentary"],
    "ISFP": ["Fantasy", "Animation", "Romance"],
    "ESFP": ["Comedy", "Romance", "Adventure"],
    "ISTP": ["Action", "Thriller", "Mystery"],
    "ESTP": ["Action", "Comedy", "Adventure"],
    "ISFJ": ["Family", "Drama", "Romance"],
    "ESFJ": ["Comedy", "Family", "Drama"],
    "ISTJ": ["Drama", "History", "Documentary"],
    "ESTJ": ["Action", "Drama", "History"],
}

# ✅ 감정 이모지 → 장르 추천
emoji_genre_map = {
    "😊": ["Comedy", "Family"],
    "😢": ["Drama", "Romance"],
    "😱": ["Thriller", "Mystery"],
    "🤔": ["Documentary", "History"],
    "😍": ["Romance", "Fantasy"],
    "💪": ["Action", "Adventure"]
}

# ✅ 페이지 설정
st.set_page_config(page_title="MBTI + 감정 기반 추천기", layout="wide")
st.title("🧠 MBTI + 감정 기반 콘텐츠 추천기")

# ✅ 사용자 입력
mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_genres_map.keys()))
selected_emoji = st.selectbox("오늘의 기분은 어떤가요?", list(emoji_genre_map.keys()))

# ✅ 장르 추천
mbti_genres = mbti_genres_map[mbti]
emotion_genres = emoji_genre_map[selected_emoji]
total_genres = mbti_genres + emotion_genres
genre_scores = Counter(total_genres)

st.markdown("### 🎯 추천 장르")
for genre, score in genre_scores.most_common():
    st.markdown(f"- **{genre}** (점수: {score})")

# ✅ 탭별 영화 추천
tabs = st.tabs([f"📺 {genre}" for genre, _ in genre_scores.most_common()])

for idx, (genre, _) in enumerate(genre_scores.most_common()):
    with tabs[idx]:
        genre_id = genre_name_to_id[genre]
        state_key = f"page_{genre}"
        if state_key not in st.session_state:
            st.session_state[state_key] = 1
        page = st.session_state[state_key]

        url = f"https://api.themoviedb.org/3/discover/movie?with_genres={genre_id}&language=ko-KR&sort_by=popularity.desc&page={page}"
        url = f"https://api.themoviedb.org/3/discover/movie?with_genres={genre_id}&language=ko-KR&sort_by=popularity.desc&page={page}&api_key={TMDB_API_KEY}"
        res = requests.get(url)

        

        if res.status_code == 200:
            movies = res.json().get("results", [])
            for movie in movies:
                st.markdown(f"**🎞️ {movie.get('title', '제목없음')}** ({movie.get('release_date', '')[:4]})")
                st.caption(movie.get("overview", "줄거리 없음"))

                if st.button(f"자세히 보기 - {movie['id']}", key=f"go_detail_{genre}_{movie['id']}"):
                    st.session_state['selected_movie_data'] = {
                        "id": movie["id"],
                        "title_ko": movie.get("title", ""),
                        "title_en": movie.get("original_title", ""),
                        "release_date": movie.get("release_date", ""),
                        "overview": movie.get("overview", ""),
                        "poster_path": movie.get("poster_path", ""),
                        "vote_average": movie.get("vote_average", 0),
                        "media_type": "movie"
                    }
                    st.switch_page("home.py")

            if st.button("📦 더 보기", key=f"load_more_{genre}"):
                st.session_state[state_key] += 1
        else:
            st.warning(f"❌ 영화 로딩 실패: {res.status_code} - {res.text}")
