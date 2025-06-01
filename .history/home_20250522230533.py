import streamlit as st
from country_filtering import (
    get_available_countries,
    get_language_code,
    is_english,
    translate_text
)
from contents_search import (
    search_movie_tmdb,
    get_providers,
    get_ott_price_info,
    logo_map
)

# ✅ 페이지 설정
st.set_page_config(page_title="🌍 OTT 콘텐츠 검색기", layout="wide")
st.title("🎬 국가별 OTT 콘텐츠 검색기 (요금 + 번역 지원)")

# 🌍 국가 선택
country_dict = get_available_countries()
selected_country = st.selectbox("🌎 국가를 선택하세요", list(country_dict.keys()))
selected_code = country_dict[selected_country]
target_lang = get_language_code(selected_code)

# 🔍 콘텐츠 검색
title = st.text_input("🔍 콘텐츠 제목을 입력하세요", "")

if title:
    with st.spinner("🔍 검색 중입니다..."):
        content = search_movie_tmdb(title)

    if content:
        st.subheader(f"📌 {content['title_ko']} ({content['release_date'][:4]})")

        cols = st.columns([1.2, 2])
        with cols[0]:
            if content["poster_path"]:
                st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_column_width=True)
        with cols[1]:
            st.markdown(f"**영문 제목:** {content['title_en']}")
            st.markdown(f"**평점:** ⭐ {content['vote_average']}")

            overview = content["overview"]
            if is_english(overview):
                overview = translate_text(overview, target_lang)
            st.markdown(f"**설명:** {overview}")

            if content["trailer_url"]:
                st.markdown(f"[▶️ 예고편 보기]({content['trailer_url']})")

        # 📺 제공 OTT 플랫폼 정보
        st.subheader(f"📺 {selected_country}에서 시청 가능한 OTT 플랫폼")
        providers = get_providers(content['title_ko'])

        if providers:
            for monetization, platforms in providers.items():
                if not platforms:
                    continue
                st.markdown(f"#### 💰 {monetization.capitalize()}")

                for platform in platforms:
                    rows = get_ott_price_info(selected_country, platform)

                    with st.container():
                        cols = st.columns([1, 5])
                        with cols[0]:
                            if platform in logo_map:
                                st.image(logo_map[platform], width=50)
                            else:
                                st.markdown(f"**{platform}**")
                        with cols[1]:
                            if rows:
                                for plan, local, krw, user_cnt, has_ads in rows:
                                    ads = " (광고 포함)" if has_ads else ""
                                    st.markdown(
                                        f"- {plan}: {int(local)}원 / ₩{int(krw)} / 최대 {user_cnt}인 사용 가능{ads}"
                                    )
                            else:
                                st.markdown("- 요금 정보 없음")
        else:
            st.warning("❌ 선택한 국가에서 제공 중인 OTT 플랫폼이 없습니다.")
    else:
        st.error("❌ 콘텐츠를 찾을 수 없습니다.")
