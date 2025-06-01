import streamlit as st
import pandas as pd
import plotly.express as px
from api_utils import search_movie_tmdb, get_providers

st.set_page_config(page_title="OTT 가성비 계산기", layout="wide")
st.title("📊 OTT 가성비 계산기")

selected_titles = st.session_state.get("selected_movies", [])
if not selected_titles:
    st.warning("❌ 선택한 영화가 없습니다. 먼저 영화를 검색하고 추가해주세요.")
    st.stop()

if len(selected_titles) > 10:
    st.warning("⚠️ 최대 10개까지만 계산에 사용됩니다.")
    selected_titles = selected_titles[:10]

st.markdown("### 🎬 선택된 영화 목록")
st.write(selected_titles)

ott_prices = {
    "Netflix": 15000,
    "Disney+": 9900,
    "Watcha": 7900,
    "Coupang Play": 4990,
    "Wavve": 7900,
    "Tving": 10900,
}

country_code = "KR"
ott_data = []

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
    st.error("❌ OTT 정보를 불러올 수 없습니다.")
    st.stop()

df = pd.DataFrame(ott_data)
ott_columns = [col for col in df.columns if col != "movie"]
ott_counts = df[ott_columns].sum()

cost_per_movie = {}
for ott in ott_counts.index:
    count = ott_counts[ott]
    if count > 0:
        cost_per_movie[ott] = ott_prices[ott] / count

result_df = pd.DataFrame({
    "OTT": ott_counts.index,
    "제공 편수": ott_counts.values,
    "월 요금": [ott_prices[ott] for ott in ott_counts.index],
    "편당 가격": [round(cost_per_movie[ott]) if ott in cost_per_movie else None for ott in ott_counts.index]
}).dropna().sort_values("편당 가격")

if result_df.empty:
    st.warning("📭 선택한 영화들을 제공하는 OTT가 없습니다.")
else:
    best = result_df.iloc[0]
    st.success(f"🎉 가장 가성비 좋은 OTT는 **{best['OTT']}**입니다! "
               f"{int(best['제공 편수'])}편을 편당 **{int(best['편당 가격'])}원**에 볼 수 있어요.")

    st.markdown("### 📊 OTT별 분석 결과")
    st.dataframe(result_df.reset_index(drop=True))

    fig = px.bar(result_df, x="OTT", y="편당 가격", color="OTT",
                 title="OTT별 편당 가격 비교", text="제공 편수")
    st.plotly_chart(fig)
