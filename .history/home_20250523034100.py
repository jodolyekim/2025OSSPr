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
    get_language_code
)

# ✅ 페이지 설정
st.set_page_config(page_title="🌍 OTT 콘텐츠 검색기", layout="wide")
st.title("🎬 통합 OTT 콘텐츠 검색기 (요금 + 설명 번역 지원)")

# ✅ MBTI 추천 결과에서 들어온 경우 처리
if 'selected_movie_id' in st.session_state:
    movie_id = st.session_state.pop('selected_movie_id')
    detail = get_details(movie_id, media_type="movie")
    title = detail.get("title", "")
    contents = [{
        "id": movie_id,
        "title_ko": detail.get("title", ""),
        "title_en": detail.get("title", ""),
        "release_date": detail.get("release_date", ""),
        "overview": detail.get("overview", ""),
        "poster_path": detail.get("poster_path", ""),
        "vote_average": detail.get("vote_average", 0),
        "media_type": "movie"
    }]
else:
    # ✅ 콘텐츠 검색 입력
    title = st.text_input("🔍 콘텐츠 제목을 입력하세요", "")
    contents = search_movie_tmdb(title) if title else []


# ✅ 찜한 콘텐츠 상태 초기화
if 'selected_contents' not in st.session_state:
    st.session_state['selected_contents'] = []

# ✅ 현재 찜 목록 표시
if st.session_state['selected_contents']:
    st.success("📌 현재 찜한 콘텐츠: " + " | ".join(st.session_state['selected_contents']))
else:
    st.info("📌 찜한 콘텐츠가 없습니다.")

# ✅ 계산기 이동 버튼
if st.button("📊 가성비 계산기로 이동하기"):
    st.switch_page("pages/1_calc_page.py")

# ✅ MBTI 추천기 이동 버튼
if st.button("🧠 MBTI 추천기로 이동하기"):
    st.switch_page("pages/2_mbti_page.py")

if contents:
    tabs = st.tabs(["🎬 영화", "📺 드라마/예능"])

    for tab, media_type in zip(tabs, ["movie", "tv"]):
        with tab:
            filtered = [c for c in contents if c["media_type"] == media_type]
            if not filtered:
                st.info("검색된 콘텐츠가 없습니다.")
                continue

            options = []
            for c in filtered:
                title = c.get('title_ko', '제목없음')
                raw_date = c.get('release_date') or c.get('first_air_date') or ''
                year = raw_date[:4] if raw_date else 'N/A'
                options.append(f"{title} ({year})")


        selected = st.radio(
            "원하는 콘텐츠를 선택하세요",
            options=options,
            key=media_type
        )

        content = next(
            c for c in filtered
            if f"{c.get('title_ko', '제목없음')} ({(c.get('release_date') or c.get('first_air_date') or '')[:4] or 'N/A'})" == selected
        )


            # 국가 및 언어 설정
            country_dict = get_available_countries()
            default_idx = list(country_dict.keys()).index("한국") if "한국" in country_dict else 0
            selected_country = st.selectbox(
                "🌍 국가를 선택하세요", list(country_dict.keys()),
                index=default_idx, key=f"country_{media_type}"
            )
            selected_code = country_dict[selected_country]
            target_lang = get_language_code(selected_code)

            # ✅ 찜하기 기능 + 계산기 이동
            with st.container():
                cols = st.columns([2, 1])
                with cols[0]:
                    if len(st.session_state['selected_contents']) >= 10:
                        st.warning("❗ 콘텐츠는 최대 10개까지 찜할 수 있습니다.")
                    elif st.button("📌 이 콘텐츠 찜하기", key=f"bookmark_{media_type}_{content['id']}"):
                        title_to_add = content['title_ko']
                        if title_to_add not in st.session_state['selected_contents']:
                            st.session_state['selected_contents'].append(title_to_add)
                            st.success(f"✅ '{title_to_add}' 를 찜했습니다.")
                        else:
                            st.info(f"이미 '{title_to_add}' 는 찜한 콘텐츠에 있어요.")
                with cols[1]:
                    st.page_link("pages/1_calc_page.py", label="📊 계산기로 이동", icon="📈")

            # 상세 정보 및 예고편
            content['trailer_url'] = get_trailer_url(content['id'], content['media_type'])
            content['trailer_embed'] = get_trailer_embed_url_ytdlp(content['trailer_url']) if content['trailer_url'] else None
            details = get_details(content['id'], content['media_type'])
            overview_local = get_multilang_overview(content['id'], content['media_type'], lang_code=target_lang)


            st.markdown("---")
            st.subheader(f"📌 {content['title_ko']} ({content['release_date'][:4] if content['release_date'] else 'N/A'})")

            cols = st.columns([1.5, 3])
            with cols[0]:
                if content["poster_path"]:
                    st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_container_width=True)
            with cols[1]:
                st.markdown(f"**영문 제목:** {content['title_en']}")
                st.markdown(f"**평점:** ⭐ {content['vote_average']}")
                if details.get("genres"):
                    st.markdown("**장르:** " + ", ".join(details["genres"]))
                if details.get("runtime"):
                    st.markdown(f"**러닝타임:** {details['runtime']}분")
                if details.get("languages"):
                    st.markdown("**사용 언어:** " + ", ".join(details["languages"]))
                if details.get("homepage"):
                    st.markdown(f"[공식 홈페이지 바로가기]({details['homepage']})")
                if details["production_companies"]:
                    st.markdown("**제작사:** " + ", ".join([c["name"] for c in details["production_companies"]]))
                if details.get("status"):
                    st.markdown(f"**상태:** {details['status']}")
                if details.get("tagline"):
                    st.markdown(f"**태그라인:** _{details['tagline']}_")
                if details.get("popularity"):
                    st.markdown(f"**TMDB 인기지수:** {round(details['popularity'], 2)}")
                if details.get("number_of_seasons") and details.get("number_of_episodes"):
                    st.markdown(f"**시즌/에피소드:** {details['number_of_seasons']}시즌 / {details['number_of_episodes']}편")

            if details["cast"]:
                st.markdown("**출연진:**")
                cast_cols = st.columns(5)
                for i, actor in enumerate(details["cast"][:10]):
                    with cast_cols[i % 5]:
                        if actor.get("profile_path"):
                            st.image(f"https://image.tmdb.org/t/p/w185{actor['profile_path']}", width=90)
                        st.caption(actor["name"])

            st.markdown("**설명:**")
            st.info(f"🇰🇷 {content['overview']}")
            if overview_local and overview_local != content["overview"]:
                st.info(f"🌐 {overview_local}")

            if content["trailer_embed"]:
                st.markdown("**🎞️ 예고편:**")
                st.video(content["trailer_embed"])

            # ✅ OTT 정보
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
    st.info("🔍 콘텐츠를 검색하거나, MBTI 추천기로 이동해 콘텐츠를 찾아보세요.")


    