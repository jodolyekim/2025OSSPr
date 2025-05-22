import streamlit as st
import pandas as pd
import plotly.express as px
from contents_search import get_providers, get_ott_price_info, search_movie_tmdb

st.set_page_config(page_title="OTT 가성비 계산기", layout="wide")
st.title("💸 OTT 가성비 계산기 (구독형 기반 분석)")

# ✅ 찜한 콘텐츠 목록 불러오기
selected_titles = st.session_state.get("selected_contents", [])

if not selected_titles:
    st.warning("🚫 현재 찜한 콘텐츠가 없습니다. 가성비 계산을 위해 최소 1개의 콘텐츠를 찜해주세요.")
    st.stop()

st.success(f"📅 선택한 콘텐츠 {len(selected_titles)}개")
st.markdown("\n".join([f"- {title}" for title in selected_titles]))

# ✅ 사용자 수 입력
user_count = st.slider("👥 함께 이용할 사용자 수를 선택하세요", min_value=1, max_value=4, value=1)

# ✅ 국가 설정 (기본 한국)
country = st.selectbox("🌍 OTT 가격을 확인할 국가", ["한국", "미국"])
country_code = {"한국": "KR", "미국": "US"}[country]

# ✅ OTT 콘텐츠 포함 여부 계산
otts_content = {}  # {"netflix": ["콘텐츠1", "콘텐츠2"], ...}
for title in selected_titles:
    results = search_movie_tmdb(title, lang="ko")
    if not results:
        continue
    result = results[0]  # 가장 첫 번째 결과 선택
    providers = get_providers(result['id'], result['media_type'], country_code=country_code)
    flatrate = providers.get("flatrate", [])
    for item in flatrate:
        ott = item["name"].lower()
        if ott not in otts_content:
            otts_content[ott] = []
        if title not in otts_content[ott]:
            otts_content[ott].append(title)

if not otts_content:
    st.warning("해당 콘텐츠들을 제공하는 구독형 OTT가 없습니다.")
    st.stop()

# ✅ OTT별 가격 정보 + 가성비 계산
data = []
for ott, contents in otts_content.items():
    plans = get_ott_price_info(country, ott)
    if not plans:
        continue
    for plan, local_price, krw_price, max_users, has_ads in plans:
        try:
            content_count = len(contents)
            cost_per_user_per_content = krw_price / (user_count * content_count)
            data.append({
                "OTT": ott.title(),
                "요금제": plan,
                "제공 콘텐츠 수": content_count,
                "1인당 콘텐츠당 가격": round(cost_per_user_per_content, 2),
                "총 요금(₩)": krw_price,
                "광고": "O" if has_ads else "X",
                "사용자 수": user_count
            })
        except Exception as e:
            print(f"[오류] {ott} - {plan}: {e}")

if not data:
    st.warning("모든 OTT 요금 정보를 불러오지 못했습니다.")
    st.stop()

# ✅ 정렬 및 시각화
sorted_df = pd.DataFrame(data).sort_values("1인당 콘텐츠당 가격")
st.subheader("🏆 가장 저렴한 OTT 순위")
st.dataframe(sorted_df.reset_index(drop=True))

fig = px.bar(
    sorted_df,
    x="OTT",
    y="1인당 콘텐츠당 가격",
    color="OTT",
    hover_data=["요금제", "총 요금(₩)", "제공 콘텐츠 수", "광고"],
    title="OTT별 1인당 콘텐츠당 가격 비교"
)
st.plotly_chart(fig, use_container_width=True)

st.caption("※ 가격은 사용자 수 및 제공 콘텐츠 수에 따라 자동 계산됩니다.")
