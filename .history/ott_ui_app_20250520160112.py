import streamlit as st
from country_filtering import select_country
from api_utils import search_movie_tmdb, get_providers, get_trailer_url, translate_to_korean, is_english

# OTT 로고 매핑 (작은 이미지 아이콘)
logo_map = {
    "Netflix": "images/netflix.png",
    "Watcha": "images/watcha.png",
    "Wavve": "images/wavve.png",
    "Disney": "images/disneyplus.png",
    "Apple": "images/apple.png",
    "Amazon": "images/amazon.png",
    "Hulu": "images/hulu.png",
    "Max": "images/max.png",
    "Stan": "images/stan.png",
    "Google Play Movies": "images/google_play_movies.png"
}

# OTT 출력 함수 (로고 포함)
def render_platform_list(name_list):
    for name in name_list:
        matched_logo = None
        name_lower = name.lower()
        for key in logo_map:
            if key.lower() in name_lower:
                matched_logo = logo_map[key]
                break

        cols = st.columns([1.2, 8.8])
        if matched_logo:
            cols[0].image(matched_logo, width=30)
        else:
            cols[0].write("🎬")
        cols[1].write(name)

# Streamlit UI
st.title("🎬 OTT 어디있니?")
st.write("영화 제목을 입력하고, 어떤 OTT에서 볼 수 있는지 확인해보세요!")

# 국가 선택
country_name = st.selectbox("국가 선택", ["한국", "미국", "영국", "캐나다", "호주"])
country_code_map = {
    "한국": "KR", "미국": "US", "영국": "GB", "캐나다": "CA", "호주": "AU"
}
country_code = country_code_map[country_name]

# 영화 제목 입력
movie_title = st.text_input("영화 제목 입력")

# 검색 버튼
if st.button("검색"):
    with st.spinner("검색 중..."):
        movie = search_movie_tmdb(movie_title, country_code)
        if movie is None or "id" not in movie:
            st.error("영화를 찾을 수 없습니다. 제목을 확인해주세요.")
        else:
            providers = get_providers(movie["id"], country_code)

            # 예고편 URL 불러오기
            trailer_url = movie.get("trailer_url")

            # 제목 출력 (한글 + 영어)
            st.success(f"'{movie['title_ko']}' ({movie['title_en']})는 {country_name}에서 다음 OTT에서 시청할 수 있어요:")

            # 포스터 출력
            if movie["poster_path"]:
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                st.image(poster_url, width=250)


            # 개봉일 + 평점 출력
            st.markdown(f"📅 **개봉일**: {movie['release_date']}")
            stars = "⭐" * int(round(movie['vote_average']))
            st.markdown(f"⭐ **평점**: {movie['vote_average']} {stars}")

            # 영화 소개(overview) 출력 및 자동 번역
            if movie.get("overview"):
                st.markdown("### 📘 Overview (영화 소개)")
                st.write(movie["overview"])  # 원문 출력

                # 영어인 경우만 번역
                if is_english(movie["overview"]):
                    translated = translate_to_korean(movie["overview"])
                    st.write(f"➡️ {translated}")
                else:
                    st.info("이 영화 소개는 이미 한국어입니다.")

            # 예고편 영상 출력
            if trailer_url:
                st.video(trailer_url)  # YouTube 예고편 영상
            else:
                st.info("예고편이 제공되지 않습니다.")  # 예고편 없을 때 메시지


            # OTT 구분 출력
            st.markdown("### 🎟️ OTT 플랫폼")
            if isinstance(providers, dict) and any(providers.values()):
                if providers["flatrate"]:
                    st.markdown("**✅ 구독 가능 플랫폼**")
                    render_platform_list(providers["flatrate"])

                if providers["rent"]:
                    st.markdown("**💰 대여 가능 플랫폼**")
                    render_platform_list(providers["rent"])

                if providers["buy"]:
                    st.markdown("**🛒 구매 가능 플랫폼**")
                    render_platform_list(providers["buy"])
            else:
                st.warning("해당 국가에서 시청 가능한 플랫폼이 없습니다.")
                # ✅ 영화 상세정보 출력이 끝났을 때 실행되는 선택 추가 기능

if "selected_movies" not in st.session_state:
    st.session_state["selected_movies"] = []

for movie in search_results:  # 또는 movies
    st.markdown(f"### 🎬 {movie.get('title_ko', '제목 없음')}")
    
    if "title_ko" in movie and st.checkbox(f"📌 '{movie['title_ko']}' 이(가) 가성비 계산기에 추가하기", key=movie["title_ko"]):
        selected_title = movie["title_ko"]
        if selected_title not in st.session_state["selected_movies"]:
            st.session_state["selected_movies"].append(selected_title)
            st.success(f"✅ '{selected_title}' 이(가) 가성비 추천기에 추가되었습니다.")
        else:
            st.info(f"이미 '{selected_title}' 은(는) 추가된 상태입니다.")


