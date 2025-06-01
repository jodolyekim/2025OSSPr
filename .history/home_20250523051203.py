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

def extract_title(c):
    return c.get("title_ko") or c.get("title") or "제목없음"

def extract_year(c, media_type):
    # TMDB가 first_air_date를 안 줄 수도 있으니 release_date도 같이 고려
    date = c.get("release_date") or c.get("first_air_date")
    if date and len(date) >= 4:
        return date[:4]

    # fallback: 상세정보에서 가져오기
    try:
        details = get_details(c["id"], media_type)
        date = details.get("first_air_date") or details.get("release_date")
        if date and len(date) >= 4:
            return date[:4]
    except:
        pass

    return "방영일 미정"




st.set_page_config(page_title="🌍 OTT 콘텐츠 검색기", layout="wide")
st.title("🎬 통합 OTT 콘텐츠 검색기 (요금 + 설명 번역 지원)")

if 'selected_movie_data' in st.session_state:
    content = st.session_state.pop('selected_movie_data')
    contents = [content]
    title = content.get("title_ko", "")
else:
    title = st.text_input("🔍 콘텐츠 제목을 입력하세요", "")
    contents = search_movie_tmdb(title) if title else []

if 'selected_contents' not in st.session_state:
    st.session_state['selected_contents'] = []

if st.session_state['selected_contents']:
    st.success("📌 현재 찜한 콘텐츠: " + " | ".join(st.session_state['selected_contents']))
else:
    st.info("📌 찜한 콘텐츠가 없습니다.")

if st.button("📊 가성비 계산기로 이동하기"):
    st.switch_page("pages/1_calc_page.py")

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
                this_title = extract_title(c)
                year = extract_year(c, media_type)
                options.append(f"{this_title} ({year})")

            selected = st.radio("원하는 콘텐츠를 선택하세요", options=options, key=media_type)

            content = next(
                (c for c in filtered if f"{extract_title(c)} ({extract_year(c, media_type)})" == selected),
                None
            )
            if content is None:
                st.error("⚠️ 선택한 콘텐츠를 찾을 수 없습니다.")
                st.stop()

            country_dict = get_available_countries()
            default_idx = list(country_dict.keys()).index("한국") if "한국" in country_dict else 0
            selected_country = st.selectbox(
                "🌍 국가를 선택하세요",
                list(country_dict.keys()),
                index=default_idx,
                key=f"country_{media_type}"
            )
            selected_code = country_dict[selected_country]
            target_lang = get_language_code(selected_code)

            with st.container():
                cols = st.columns([2, 1])
                with cols[0]:
                    if len(st.session_state['selected_contents']) >= 10:
                        st.warning("❗ 콘텐츠는 최대 10개까지 찜할 수 있습니다.")
                    elif st.button("📌 이 콘텐츠 찜하기", key=f"bookmark_{media_type}_{content['id']}"):
                        title_to_add = extract_title(content)
                        if title_to_add not in st.session_state['selected_contents']:
                            st.session_state['selected_contents'].append(title_to_add)
                            st.success(f"✅ '{title_to_add}' 를 찜했습니다.")
                        else:
                            st.info(f"이미 '{title_to_add}' 는 찜한 콘텐츠에 있어요.")
                with cols[1]:
                    st.page_link("pages/1_calc_page.py", label="📊 계산기로 이동", icon="📈")

            content['trailer_url'] = get_trailer_url(content['id'], content['media_type'])
            content['trailer_embed'] = get_trailer_embed_url_ytdlp(content['trailer_url']) if content['trailer_url'] else None
            details = get_details(content['id'], content['media_type'])
            overview_local = get_multilang_overview(content['id'], content['media_type'], lang_code=target_lang)

            st.markdown("---")
            st.subheader(f"📌 {extract_title(content)} ({extract_year(content, media_type)})")

            cols = st.columns([1.5, 3])
            with cols[0]:
                if content["poster_path"]:
                    st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_container_width=True)
            with cols[1]:
                st.markdown(f"**영문 제목:** {content.get('title_en', '-')}")
                st.markdown(f"**평점:** ⭐ {content.get('vote_average', '-')}")
                if details.get("genres"):
                    st.markdown("**장르:** " + ", ".join(details["genres"]))
                if details.get("runtime"):
                    st.markdown(f"**러닝타임:** {details['runtime']}분")
                if details.get("languages"):
                    st.markdown("**사용 언어:** " + ", ".join(details["languages"]))
                if details.get("homepage"):
                    st.markdown(f"[공식 홈페이지 바로가기]({details['homepage']})")
                if details.get("production_companies"):
                    st.markdown("**제작사:** " + ", ".join([c["name"] for c in details["production_companies"]]))
                if details.get("status"):
                    st.markdown(f"**상태:** {details['status']}")
                if details.get("tagline"):
                    st.markdown(f"**태그라인:** _{details['tagline']}_")
                if details.get("popularity"):
                    st.markdown(f"**TMDB 인기지수:** {round(details['popularity'], 2)}")
                if details.get("number_of_seasons") and details.get("number_of_episodes"):
                    st.markdown(f"**시즌/에피소드:** {details['number_of_seasons']}시즌 / {details['number_of_episodes']}편")

            if details.get("cast"):
                st.markdown("**출연진:**")
                cast_cols = st.columns(5)
                for i, actor in enumerate(details["cast"][:10]):
                    with cast_cols[i % 5]:
                        if actor.get("profile_path"):
                            st.image(f"https://image.tmdb.org/t/p/w185{actor['profile_path']}", width=90)
                        st.caption(actor["name"])

            st.markdown("**설명:**")
            st.info(f"🇰🇷 {content.get('overview', '-')}")
            if overview_local and overview_local != content.get("overview"):
                st.info(f"🌐 {overview_local}")

            if content["trailer_embed"]:
                st.markdown("**🎞️ 예고편:**")
                st.video(content["trailer_embed"])

            # OTT 정보
            st.subheader(f"📺 {selected_country}에서 시청 가능한 OTT 플랫폼")

            # ✅ media_type이 없을 경우 대비
            media_type_value = content.get("media_type", media_type)
            providers = get_providers(content['id'], media_type_value, country_code=selected_code)
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
                st.warning("❌ 현재 선택한 콘텐츠는 해당 국가의 OTT에서 제공되지 않거나 정보가 없습니다.")

else:
    st.info("🔍 콘텐츠를 검색하거나, MBTI 추천기로 이동해 콘텐츠를 찾아보세요.")
