import streamlit as st
from contents_search import (
    search_movie_tmdb,
    get_providers,
    get_ott_price_info,
    logo_map,
    get_trailer_url,
    get_details,
    get_multilang_overview,
    get_trailer_embed_url_ytdlp
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
        contents = search_movie_tmdb(title)

    if contents:
        # ✅ 콘텐츠를 영화/TV로 구분
        movies = [c for c in contents if c["media_type"] == "movie"]
        tv_shows = [c for c in contents if c["media_type"] == "tv"]

        if movies:
            st.subheader("🎬 영화")
            for idx, movie in enumerate(movies):
                st.markdown(f"{idx+1}. {movie['title_ko']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'})")

        if tv_shows:
            st.subheader("📺 드라마/예능")
            for idx, show in enumerate(tv_shows):
                st.markdown(f"{idx+1}. {show['title_ko']} ({show['release_date'][:4] if show['release_date'] else 'N/A'})")

        # ✅ 사용자에게 선택 옵션 제공
        options = [f"{c['title_ko']} ({c['release_date'][:4] if c['release_date'] else 'N/A'})" for c in contents]
        selected_idx = st.selectbox("🎯 정확한 콘텐츠를 선택하세요", options, index=0)
        content = contents[options.index(selected_idx)]

        # ✅ 국가 선택
        country_dict = get_available_countries()
        default_idx = list(country_dict.keys()).index("한국") if "한국" in country_dict else 0
        selected_country = st.selectbox("🌍 국가를 선택하세요", list(country_dict.keys()), index=default_idx)
        selected_code = country_dict[selected_country]
        target_lang = get_language_code(selected_code)

        # ✅ 예고편 링크 및 상세 정보 호출
        content['trailer_url'] = get_trailer_url(content['id'], content['media_type'])
        content['trailer_embed'] = get_trailer_embed_url_ytdlp(content['trailer_url']) if content['trailer_url'] else None
        details = get_details(content['id'], content['media_type'])

        st.markdown("---")
        st.subheader(f"📌 {content['title_ko']} ({content['release_date'][:4] if content['release_date'] else 'N/A'})")

        # ✅ 콘텐츠 요약 출력
        cols = st.columns([1.2, 2])
        with cols[0]:
            if content["poster_path"]:
                st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_container_width=True)
        with cols[1]:
            st.markdown(f"**영문 제목:** {content['title_en']}")
            st.markdown(f"**평점:** ⭐ {content['vote_average']}")
            if details["production_companies"]:
                st.markdown("**제작사:** " + ", ".join([c["name"] for c in details["production_companies"]]))

        # ✅ 출연진 표시
        if details["cast"]:
            st.markdown("**출연진:**")
            cast_cols = st.columns(5)
            for i, actor in enumerate(details["cast"]):
                with cast_cols[i % 5]:
                    if actor.get("profile_path"):
                        st.image(f"https://image.tmdb.org/t/p/w185{actor['profile_path']}", width=90)
                    st.caption(actor["name"])

        # ✅ 설명: 한국어 + 선택 국가 언어 병기
        st.markdown("**설명:**")
        st.info(f"🇰🇷 {content['overview']}")
        overview_local = get_multilang_overview(content['id'], content['media_type'], lang_code=target_lang)
        if overview_local and overview_local != content["overview"]:
            st.info(f"🌐 {overview_local}")

        # ✅ 예고편 영상 임베드
        if content["trailer_embed"]:
            st.markdown("**🎞️ 예고편:**")
            st.video(content["trailer_embed"])

        # ✅ OTT 플랫폼 및 가격 정보
        st.subheader(f"📺 {selected_country}에서 시청 가능한 OTT 플랫폼")
        providers = get_providers(content['id'], content['media_type'], country_code=selected_code)

        if providers:
            for monetization, platforms in providers.items():
                label = {
                    "flatrate": "📦 구독형",
                    "rent": "🎟️ 대여",
                    "buy": "🛒 구매"
                }.get(monetization, monetization)

                if not platforms:
                    st.warning(f"❌ {selected_country}에서 {label} 서비스로는 제공되지 않습니다.")
                    continue

                st.markdown(f"#### {label}")
                for platform in platforms:
                    platform_name = platform["name"].lower()
                    if "netflix" in platform_name and "with ads" in platform_name:
                        continue

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
                                if platform.get("price"):
                                    st.markdown(f"- {platform_name.title()}: {int(platform['price']):,}원")
                                else:
                                    st.markdown(f"- {platform_name.title()}")
        else:
            st.warning("❌ 선택한 국가에서 제공 중인 OTT 플랫폼이 없습니다.")
    else:
        st.error("❌ 콘텐츠를 찾을 수 없습니다.")

