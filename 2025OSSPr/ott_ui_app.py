import streamlit as st
from api_utils import search_movie_tmdb, get_providers
from country_filtering import select_country

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
        movie = search_movie_tmdb(movie_title)
        if not movie:
            st.error("영화를 찾을 수 없습니다. 제목을 확인해주세요.")
        else:
            providers = get_providers(movie["id"], country_code)

            # 제목 출력 (한글 + 영어)
            st.success(f"'{movie['title_ko']}' ({movie['title_en']})는 {country_name}에서 다음 OTT에서 시청할 수 있어요:")

            # 포스터 출력
            if movie["poster_path"]:
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                st.image(poster_url, width=250)

            # OTT 출력 (로고 + 이름)
            if providers:
                for p in providers:
                    matched_logo = None
                    p_lower = p.lower()
                    for key in logo_map:
                        if key.lower() in p_lower:
                            matched_logo = logo_map[key]
                            break

                    cols = st.columns([1.2, 8.8])
                    if matched_logo:
                        cols[0].image(matched_logo, width=30)
                    else:
                        cols[0].write("🎬")
                    cols[1].write(p)
            else:
                st.warning("해당 국가에서 시청 가능한 OTT 플랫폼이 없습니다.")
