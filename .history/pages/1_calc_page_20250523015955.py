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

st.set_page_config(page_title="\ud83c\udf0d OTT \ucee8\ud150\uce20 \uac80\uc0c9\uae30", layout="wide")
st.title("\ud83c\udfac \ud1b5\ud569 OTT \ucee8\ud150\uce20 \uac80\uc0c9\uae30 (\uc694\uae08 + \uc124\uba85 \ubc88\uc5ed \uc9c0\uc6d0)")

if 'selected_contents' not in st.session_state:
    st.session_state['selected_contents'] = []

if st.session_state['selected_contents']:
    st.success("\ud83d\udccc \ud604\uc7ac \uc994\ud55c \ucee8\ud150\uce20: " + " | ".join(st.session_state['selected_contents']))
else:
    st.info("\ud83d\udccc \uc994\ud55c \ucee8\ud150\uce20\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.")

title = st.text_input("\ud83d\udd0d \ucee8\ud150\uce20 \uc81c\ubaa9\uc744 \uc785\ub825\ud558\uc138\uc694", "")

if title:
    with st.spinner("\ud83d\udd0d \ucee8\ud150\uce20\ub97c \uac80\uc0c9 \uc911\uc785\ub2c8\ub2e4..."):
        contents = search_movie_tmdb(title)

    if contents:
        tabs = st.tabs(["\ud83c\udfac \uc601\ud654", "\ud83d\udcfa \ub4dc\ub77c\ub9c8/\uc608\ub839"])

        for tab, media_type in zip(tabs, ["movie", "tv"]):
            with tab:
                filtered = [c for c in contents if c["media_type"] == media_type]
                if not filtered:
                    st.info("\uac80\uc0c9\ub41c \ucee8\ud150\uce20\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.")
                    continue

                selected = st.radio(
                    "\uc6d0\ud558\ub294 \ucee8\ud150\uce20\ub97c \uc120\ud0dd\ud558\uc138\uc694",
                    options=[f"{c['title_ko']} ({c['release_date'][:4] if c['release_date'] else 'N/A'})" for c in filtered],
                    key=media_type
                )
                content = next(c for c in filtered if f"{c['title_ko']} ({c['release_date'][:4] if c['release_date'] else 'N/A'})" == selected)

                country_dict = get_available_countries()
                default_idx = list(country_dict.keys()).index("\ud55c\uad6d") if "\ud55c\uad6d" in country_dict else 0
                selected_country = st.selectbox("\ud83c\udf0d \uad6d\uac00\ub97c \uc120\ud0dd\ud558\uc138\uc694", list(country_dict.keys()), index=default_idx, key=f"country_{media_type}")
                selected_code = country_dict[selected_country]
                target_lang = get_language_code(selected_code)

                content['trailer_url'] = get_trailer_url(content['id'], content['media_type'])
                content['trailer_embed'] = get_trailer_embed_url_ytdlp(content['trailer_url']) if content['trailer_url'] else None
                details = get_details(content['id'], content['media_type'])
                overview_local = get_multilang_overview(content['id'], content['media_type'], lang_code=target_lang)

                st.markdown("---")
                st.subheader(f"\ud83d\udccc {content['title_ko']} ({content['release_date'][:4] if content['release_date'] else 'N/A'})")

                cols = st.columns([1.5, 3])
                with cols[0]:
                    if content["poster_path"]:
                        st.image(f"https://image.tmdb.org/t/p/w500{content['poster_path']}", use_container_width=True)
                with cols[1]:
                    st.markdown(f"**\uc601\ubb38 \uc81c\ubaa9:** {content['title_en']}")
                    st.markdown(f"**\ud3c9\uc810:** ⭐ {content['vote_average']}")
                    if details.get("genres"):
                        st.markdown("**\uc7a5\ub974:** " + ", ".join(details["genres"]))
                    if details.get("runtime"):
                        st.markdown(f"**\ub7ec\ub2dd\ud0c0\uc784:** {details['runtime']}\ubd84")
                    if details.get("languages"):
                        st.markdown("**\uc0ac\uc6a9 \uc5b8\uc5b4:** " + ", ".join(details["languages"]))
                    if details.get("homepage"):
                        st.markdown(f"[\uacf5\uc2dd \ud648\ud398\uc774\uc9c0 \ubc14\ub85c\uac00\uae30]({details['homepage']})")
                    if details["production_companies"]:
                        st.markdown("**\uc81c\uc791\uc0ac:** " + ", ".join([c["name"] for c in details["production_companies"]]))
                    if details.get("status"):
                        st.markdown(f"**\uc0c1\ud669:** {details['status']}")
                    if details.get("tagline"):
                        st.markdown(f"**\ud0dc\uadf8\ub77c\uc778:** _{details['tagline']}_")
                    if details.get("popularity"):
                        st.markdown(f"**TMDB \uc778\uae30\uc9c0\uc218:** {round(details['popularity'], 2)}")
                    if details.get("number_of_seasons") and details.get("number_of_episodes"):
                        st.markdown(f"**\uc2dc\uc98c/\uc5d0\ud53c\uc18c\ub4dc:** {details['number_of_seasons']}\uc2dc\uc98c / {details['number_of_episodes']}\ud3b8")

                if details["cast"]:
                    st.markdown("**\ucd9c\uc5f0\uc9c4:**")
                    cast_cols = st.columns(5)
                    for i, actor in enumerate(details["cast"][:10]):
                        with cast_cols[i % 5]:
                            if actor.get("profile_path"):
                                st.image(f"https://image.tmdb.org/t/p/w185{actor['profile_path']}", width=90)
                            st.caption(actor["name"])

                st.markdown("**\uc124\uba85:**")
                st.info(f"\ud55c\uad6d\uc5b4 {content['overview']}")
                if overview_local and overview_local != content["overview"]:
                    st.info(f"{target_lang.upper()} {overview_local}")

                if content["trailer_embed"]:
                    st.markdown("**\ud83c\udfae \uc608\uace0\ud3b8:**")
                    st.video(content["trailer_embed"])

                if len(st.session_state['selected_contents']) >= 10:
                    st.warning("\u2757 \ucee8\ud150\uce20\ub294 \ucd5c\ub300 10\uac1c\uae4c\uc9c0 \uc994\ud55c \uac00\ub2a5\ud569\ub2c8\ub2e4.")
                elif st.button("\ud83d\udccc \uc774 \ucee8\ud150\uce20 \uc994\ud55c\uae30", key=f"bookmark_{media_type}_{content['id']}"):
                    title_to_add = content['title_ko']
                    if title_to_add not in st.session_state['selected_contents']:
                        st.session_state['selected_contents'].append(title_to_add)
                        st.success(f"✅ '{title_to_add}' \ub97c \uc994\ud588\uc2b5\ub2c8\ub2e4.")
                    else:
                        st.info(f"이미 '{title_to_add}' \ub294 \uc774\ubbf8 \uc994\ud55c \ucee8\ud150\uce20\uc5d0 \uc788\uc5b4\uc694.")

                st.subheader(f"\ud83d\udcfa {selected_country}\uc5d0\uc11c \uc2dc\uccad \uac00\ub2a5\ud55c OTT \ud50c\ub7ab\ud3fc")
                providers = get_providers(content['id'], content['media_type'], country_code=selected_code)

                if providers:
                    for monetization, platforms in providers.items():
                        label = {
                            "flatrate": "\ud83d\udce6 \uad6c\ub3c5\ud615",
                            "rent": "\ud83c\udfab \ub300\uc5ec",
                            "buy": "\ud83d\uded2 \uad6c\ub9e4"
                        }.get(monetization, monetization)

                        if not platforms:
                            st.warning(f"\u274c {selected_country}\uc5d0\uc11c {label} \uc11c\ube44\uc2a4\ub85c\ub294 \uc81c\uacf5\ub418\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.")
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
                                        st.markdown(f"**\ud83c\udfac {platform_name.title()}**")
                                with cols[1]:
                                    if monetization == "flatrate":
                                        rows = get_ott_price_info(selected_country, platform_name)
                                        if rows:
                                            for plan, local, krw, user_cnt, has_ads in rows:
                                                ad_str = " | **\ud83c\udfae \uad11\uace0 \ud3ec\ud568**" if has_ads else ""
                                                st.markdown(
                                                    f"- **{plan}**: {int(local):,}\uc6d0 (\uc57d \u20a9{int(krw):,}) / \ucd5c\ub300 {user_cnt}\uba85 \uc0ac\uc6a9 \uac00\ub2a5{ad_str}"
                                                )
                                        else:
                                            st.markdown("- \uc694\uae08 \uc815\ubcf4 \uc5c6\uc74c")
                                    else:
                                        if platform.get("price"):
                                            st.markdown(f"- {platform_name.title()}: {int(platform['price']):,}\uc6d0")
                                        else:
                                            st.markdown(f"- {platform_name.title()}")
                else:
                    st.warning("\u274c \uc120\ud0dd\ud55c \uad6d\uac00\uc5d0\uc11c \uc81c\uacf5 \uc911\uc778 OTT \ud50c\ub7ab\ud3fc\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.")
    else:
        st.error("\u274c \ucee8\ud150\uce20\ub97c \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.")
