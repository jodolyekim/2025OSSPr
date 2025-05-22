import streamlit as st
import pandas as pd
import plotly.express as px
from api_utils import search_movie_tmdb, get_providers

st.set_page_config(page_title="OTT 가성비 추천기", layout="wide")

st.title("🎯 OTT 가성비 추천기")
st.markdown("📝 다른 화면에서 ‘가성비 계산기에 추가’한 영화들의 OTT 가성비를 비교합니다.")

# ✅ 세션 상태 초기화
if "selected_movies" not in st.session_state:
    st.session_state["selected_movies"] = []
if "run_analysis" not in st.session_state:
    st.session_state["run_analysis"] = False

# ✅ 선택된 영화 리스트 출력
selected_titles = st.session_state["selected_movies"]
if not selected_titles:
    st.warning("가성비 계산기에 추가된 영화가 없습니다. 먼저 영화를 검색하고 추가해주세요.")
    st.stop()

st.markdown("### 🎬 선택한 영화 목록")
st.write(selected_titles)

# ✅ 계산 버튼
if st.button("📊 가성비 계산 시작"):
    st.session_state["run_analysis"] = True

# ✅ 조건부 실행: 버튼 눌렀을 때만 아래 분석 실행
if st.session_state["run_analysis"]:

    st.markdown("---")
    st.subheader("📈 OTT 가성비 분석 결과")

    # ✅ OTT 월 구독 요금 (원화 기준)
    ott_prices = {
        "Netflix": 15000,
        "Disney+": 9900,
        "Watcha": 7900,
        "Coupang Play": 4990,
        "Wavve": 7900,
        "Tving": 10900,
    }

    # ✅ 최대 10개까지 처리
    if len(selected_titles) > 10:
        st.warning("선택된 영화가 10개를 초과했습니다. 처음 10개만 분석에 사용됩니다.")
        selected_titles = selected_titles[:10]

    country_code = "KR"
    ott_data = []

    # ✅ 영화별 OTT 제공 정보 수집
    for title in selected_titles:
        movie = search_movie_tmdb(title, country_code)
        if not movie:
            continue

        providers = get_providers(movie["id"], country_code)
        flatrate_list = providers.get("flatrate", [])

        row = {"movie": title}
        for ott in ott_prices:
            row[ott] = 1 if ott in flatrate_list else 0
        ott_data.append(row)

    if not ott_data:
        st.error("선택한 영화들 중 OTT 정보를 불러올 수 없습니다.")
        st.stop()

    df = pd.DataFrame(ott_data)

    # ✅ OTT별 제공 편수 계산
    ott_columns = [col for col in df.columns if col != "movie"]
    ott_counts = df[ott_columns].sum()

    # ✅ 편당 가격 계산
    cost_per_movie = {}
    for ott in ott_counts.index:
        count = ott_counts[ott]
        if count > 0:
            cost_per_movie[ott] = ott_prices[ott] / count

    # ✅ 결과 정리
    result_df = pd.DataFrame({
        "OTT": ott_counts.index,
        "제공 편수": ott_counts.values,
        "월 요금": [ott_prices[ott] for ott in ott_counts.index],
        "편당 가격": [round(cost_per_movie[ott]) if ott in cost_per_movie else None for ott in ott_counts.index]
    }).dropna().sort_values("편당 가격")

    if result_df.empty:
        st.error("선택한 영화들을 제공하는 OTT 플랫폼이 없습니다.")
    else:
        best = result_df.iloc[0]
        st.success(f"🎉 가장 가성비 좋은 OTT는 **{best['OTT']}**입니다! "
                   f"{int(best['제공 편수'])}편을 편당 약 **{int(best['편당 가격'])}원**에 볼 수 있어요.")

        # ✅ 테이블 출력
        st.markdown("### 📊 OTT별 비교 결과")
        st.dataframe(result_df.reset_index(drop=True))

        # ✅ 시각화
        fig = px.bar(result_df, x="OTT", y="편당 가격", color="OTT",
                     title="OTT별 편당 가격 비교", text="제공 편수")
        st.plotly_chart(fig)
