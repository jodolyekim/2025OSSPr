import streamlit as st
from country_filtering import select_country
from api_utils import (
    search_movie_tmdb,
    get_providers,
    get_trailer_url,
    translate_to_korean,
    is_english,
    get_detailed_providers_all,
    get_recommendations,
)

# ── OTT 로고 매핑 (작은 이미지 아이콘) ──
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
    "Google Play Movies": "images/google_play_movies.png",
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

# 화면에 표시할 국가명 <-> 코드 매핑 (select_country() 반환값이 코드이므로, 보여줄 때 사용)
COUNTRY_NAME_MAP = {
    "KR": "한국",
    "US": "미국",
    "GB": "영국",
    "CA": "캐나다",
    "AU": "호주",
}

st.title("🎬 OTT 어디있니?")
st.write("영화 제목을 입력하고, 어떤 OTT에서 볼 수 있는지 확인해보세요!")

# ── country_filtering.py 의 select_country() 를 사용하여 country_code를 가져옴 ──
country_code = select_country()
country_name = COUNTRY_NAME_MAP.get(country_code, country_code)

# ── 영화 제목 입력 ──
movie_title = st.text_input("영화 제목 입력")

# ── 검색 버튼 ──
if st.button("검색"):
    with st.spinner("검색 중..."):
        movie = search_movie_tmdb(movie_title, country_code)
        if movie is None or "id" not in movie:
            st.error("영화를 찾을 수 없습니다. 제목을 확인해주세요.")
        else:
            # OTT 플랫폼 정보 (streaming/flatrate, rent, buy)
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
            stars = "⭐" * int(round(movie["vote_average"]))
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
                st.info("예고편이 제공되지 않습니다.")

            # ── OTT 플랫폼 구분 출력 ──
            st.markdown("### 🎟️ OTT 플랫폼")
            if isinstance(providers, dict) and any(providers.values()):
                if providers.get("flatrate"):
                    st.markdown("**✅ 구독 가능 플랫폼**")
                    render_platform_list(providers["flatrate"])

                if providers.get("rent"):
                    st.markdown("**💰 대여 가능 플랫폼**")
                    render_platform_list(providers["rent"])

                if providers.get("buy"):
                    st.markdown("**🛒 구매 가능 플랫폼**")
                    render_platform_list(providers["buy"])
            else:
                st.warning("해당 국가에서 시청 가능한 플랫폼이 없습니다.")

            # ── 국가별 스트리밍 정보 (다른 국가: US, GB, JP, AU) ──
            other_countries = ["US", "GB", "JP", "AU"]
            others = get_detailed_providers_all(movie["id"], other_countries)
            st.markdown("## 🌍 다른 국가에서 시청 가능한 OTT")
            has_other = False
            for code, info in others.items():
                flatrate_list = info.get("flatrate", [])
                if flatrate_list:
                    has_other = True
                    country_label = COUNTRY_NAME_MAP.get(code, code)
                    st.markdown(f"**{country_label}**:")
                    render_platform_list(flatrate_list)
            if not has_other:
                st.info("다른 국가에서 시청 가능한 스트리밍 정보가 없습니다.")

            # ── 추천 영화 (최대 5개) ──
            st.markdown("## 🔍 추천 영화")
            recommendations = get_recommendations(movie["id"])
            if recommendations and isinstance(recommendations, list):
                for rec in recommendations[:5]:
                    cols = st.columns([1.2, 8.8])
                    poster_path = rec.get("poster_path")
                    title = rec.get("title", "")
                    overview = rec.get("overview", "")
                    vote = rec.get("vote_average", "N/A")

                    if poster_path:
                        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                        cols[0].image(poster_url, width=80)
                    else:
                        cols[0].write("🎬")

                    cols[1].write(f"**{title}**")
                    cols[1].write(overview)
                    cols[1].write(f"⭐ 평점: {vote}")
            else:
                st.info("추천 영화 정보를 찾을 수 없습니다.")
