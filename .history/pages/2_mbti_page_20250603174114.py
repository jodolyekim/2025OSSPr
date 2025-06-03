import streamlit as st
from collections import Counter
import requests
import os
from dotenv import load_dotenv
from contents_search import get_details, get_trailer_url, get_multilang_overview

# ✅ API 키 로드
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
EMOJI_API_KEY = os.getenv("EMOJI_API_KEY")

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

# ✅ 이모지 해석 함수
@st.cache_data
def get_genres_from_emoji(emoji):
    url = f"https://api.api-ninjas.com/v1/emoji?name={emoji}"
    headers = {"X-Api-Key": EMOJI_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            result = res.json()
            if result:
                category = result[0].get("category", "")
                emoji_category_to_genres = {
                    "smileys-emotion": ["Comedy", "Family"],
                    "people-body": ["Drama", "Romance"],
                    "symbols": ["Thriller", "Mystery"],
                    "activities": ["Action", "Adventure"],
                    "animals-nature": ["Fantasy", "Animation"],
                }
                return emoji_category_to_genres.get(category, [])
    except Exception as e:
        print(f"[이모지 API 실패] {e}")
    return []

# ✅ 페이지 설정
st.set_page_config(page_title="MBTI + 감정 기반 추천기", layout="wide")
st.title("🧠 MBTI + 감정 기반 콘텐츠 추천기")

# ✅ 사용자 입력
mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_genres_map.keys()))
selected_emoji = st.text_input("오늘의 기분을 이모지로 표현해 주세요 (예: 😊, 😢, 😱)", "😊")

# ✅ 장르 추천
mbti_genres = mbti_genres_map[mbti]
emotion_genres = get_genres_from_emoji(selected_emoji)

if not emotion_genres:
    st.warning("이모지를 해석하지 못했어요. 기본 장르를 사용합니다.")
    emotion_genres = ["Drama"]

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
