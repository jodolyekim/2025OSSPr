import streamlit as st
import sqlite3
from api_utils import search_movie_tmdb, get_providers

# 🎨 OTT 로고 매핑 (images 폴더 내 파일명 기준)
logo_map = {
    "Netflix": "images/netflix.png",
    "Watcha": "images/watcha.png",
    "Wavve": "images/wavve.png",
    "Tving": "images/tving.png",
    "Disney+": "images/disneyplus.png",
    "Apple TV+": "images/apple.png",
    "Amazon Prime Video": "images/amazon.png",
    "Google Play Movies": "images/google_play_movies.png",
    "Hulu": "images/hulu.png",
    "Max": "images/max.png",
    "Stan": "images/stan.png"
}

# 📦 OTT 가격 정보 조회 함수 (국가=Korea 고정)
def get_ott_price_info(country, platform):
    try:
        conn = sqlite3.connect("ott_prices.db")
        cursor = conn.cursor()
        query = """
            SELECT plan, price_local, price_krw, user_count, has_ads
            FROM ott_prices
            WHERE country = ? AND platform = ?
        """
        cursor.execute(query, (country, platform))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB Error] {e}")
        return []

# 🧠 메인 화면
st.set_page_config(page_title="OTT 콘텐츠 검색", layout="wide")
st.title("🎬 OTT 콘텐츠 검색기")

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
            st.markdown(f"**설명:** {content['overview']}")
            if content["trailer_url"]:
                st.markdown(f"[▶️ 예고편 보기]({content['trailer_url']})")

        # 🎥 JustWatch 기반 플랫폼 표시
        st.subheader("📺 시청 가능한 OTT 플랫폼")
        providers = get_providers(content['title_ko'])

        if providers:
            for monetization, platforms in providers.items():
                if not platforms:
                    continue
                st.markdown(f"#### 💰 {monetization.capitalize()}")

                for platform in platforms:
                    rows = get_ott_price_info("Korea", platform)

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
                                        f"- {plan}: {int(local)}원 / {int(krw)}원 (₩ 기준), 최대 {user_cnt}인 사용 가능{ads}"
                                    )
                            else:
                                st.markdown("- 요금 정보 없음")
        else:
            st.warning("해당 콘텐츠는 현재 제공 중인 OTT 플랫폼이 없습니다.")
    else:
        st.error("❌ 검색 결과를 찾을 수 없습니다.")
