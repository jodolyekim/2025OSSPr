import streamlit as st
from contents_search import (
    search_movie_tmdb,
    get_providers,
    get_ott_price_info,
    logo_map
)
from country_filtering import (
    get_available_countries,
    get_language_code,
    is_english,
    translate_text
)

# ✅ 페이지 설정
st.set_page_config(page_title="🌍 OTT 콘텐츠 검색기", layout="wide")
st.title("🎬 통합 OTT 콘텐츠 검색기 (요금 + 설명 번역 지원)")

# ✅ 콘텐츠 검색 입력
title = st.text_input("🔍 콘텐츠 제목을 입력하세요", "")

if title:
    with st.spinner("🔍 콘텐츠를 검색 중입니다..."):
        content = search_movie_tmdb(title)

    if content:
        st.subheader(f"📌 {content['title_ko']} ({content['release_date'][:4]})")

        # ✅ 콘텐츠 요약 출력
        cols = st.columns([1.2, 2])
        with cols[0]:
            if content["poster_path"]:
                st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_container_width=True)
        with cols[1]:
            st.markdown(f"**영문 제목:** {content['title_en']}")
            st.markdown(f"**평점:** ⭐ {content['vote_average']}")

        # ✅ 국가 선택
        country_dict = get_available_countries()
        default_idx = list(country_dict.keys()).index("한국") if "한국" in country_dict else 0
        selected_country = st.selectbox("🌍 국가를 선택하세요", list(country_dict.keys()), index=default_idx)
        selected_code = country_dict[selected_country]
        target_lang = get_language_code(selected_code)

        # ✅ 설명 번역
        overview = content["overview"]
        if is_english(overview):
            overview = translate_text(overview, target_lang)
        st.markdown(f"**설명:** {overview}")

        # ✅ 예고편 링크
        if content["trailer_url"]:
            st.markdown(f"[▶️ 예고편 보기]({content['trailer_url']})")

        # ✅ OTT 플랫폼 및 가격 정보
        st.subheader(f"📺 {selected_country}에서 시청 가능한 OTT 플랫폼")

        providers = get_providers(content['id'], content['media_type'], country_code=selected_code)

        if providers:
            for monetization, platforms in providers.items():
                if not platforms:
                    continue

                label = {
                    "flatrate": "📦 구독형",
                    "rent": "🎟️ 대여",
                    "buy": "🛒 구매"
                }.get(monetization, monetization)
                st.markdown(f"#### {label}")

                for platform in platforms:
                    platform_name = platform["name"].lower()

                    # ❌ 넷플릭스 with ads 제거
                    if "netflix" in platform_name and "with ads" in platform_name:
                        continue

                    # ✅ 로고 출력
                    with st.container():
                        cols = st.columns([1, 5])
                        with cols[0]:
                            logo = logo_map.get(platform_name)
                            if logo:
                                st.image(logo, width=50)
                            else:
                                st.markdown(f"**🎬 {platform_name.title()}**")

                        with cols[1]:
                            if monetization == "flatrate":
                                rows = get_ott_price_info(selected_country, platform_name)
                                if rows:
                                    for plan, local, krw, user_cnt, has_ads in rows:
                                        ad_str = " | **🎞️ 광고 포함**" if has_ads else ""
                                        st.markdown(
                                            f"- **{plan}**: {int(local):,}원 (약 ₩{int(krw):,}) / 최대 {user_cnt}명 사용 가능{ad_str}"
                                        )
                                else:
                                    st.markdown("- 요금 정보 없음")
                            else:
                                # ✅ 대여/구매 가격이 있으면 표시
                                if platform.get("price"):
                                    st.markdown(f"- {platform_name.title()}: {int(platform['price']):,}원")
                                else:
                                    st.markdown(f"- {platform_name.title()}")
        else:
            st.warning("❌ 선택한 국가에서 제공 중인 OTT 플랫폼이 없습니다.")
    else:
        st.error("❌ 콘텐츠를 찾을 수 없습니다.")
