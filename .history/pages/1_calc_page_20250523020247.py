import streamlit as st
from contents_search import get_providers, get_ott_price_info

st.set_page_config(page_title="OTT \uac00\uc131\ube44 \uacc4\uc0b0\uae30", layout="wide")
st.title("\ud83d\udcb8 OTT \uac00\uc131\ube44 \uacc4\uc0b0\uae30 (\uad6c\ub3c5\ud615 \ud3ec\ud568)")

# 현재 즔한 컨텐트 값 반환
selected = st.session_state.get("selected_contents", [])

if not selected:
    st.warning("\ud83d\udeab \uc694즘 \uc994\ud55c \ucee8\ud150\uce20가 \uc5c6습\ub2c8\ub2e4. \uac00성\ube44 \uacc4\uc0b0\uc740 \uc694즘\ud55c \ucee8\ud150\uce20가 \ud544요\ud569\ub2c8\ub2e4.")
    st.stop()

st.success(f"\ud83d\udcc5 \uc120\ud0dd\ud55c \ucee8\ud150\uce20 {len(selected)}\uac1c")
st.write("\n".join([f"- {title}" for title in selected]))

# 이용자 수 입력
user_count = st.slider("\ud569\uae08\uc744 \ub098누\ub294 \uc774용\uc790 \uc218", min_value=1, max_value=4, value=1, step=1)

# 가성\ube44 계산 (가장 많이 포함한 OTT, 일반적 가격 및 \uc0ac용자수로 \ub098누는 가격)
# 일반화하게 OTT 플\ub7ab\ud3fc 업체를 구현

st.info("\u2728 \uc9c0\uae08\uc740 \uae30본 \uae30능\ub9cc \uad6c현\ub418\uc5b4 \uc788습\ub2c8\ub2e4. \uce7c\ub7fc \uae30본\uae30를 \ubcf4다 \uad6c\uccb4\ud654\ud558고, \ud604재\ub294 \ubc14\ub85c \uac00성\ube44 \uacc4\uc0b0\uc740 \uc548\ud558\uc9c0\ub9cc, \uc784의 OTT \uac00격 \ub370이\ud130를 \uae30본\uc73c로 \ud3c9가\ud558\ub294 \ud615식\uc785\ub2c8\ub2e4.")

st.markdown("---")
st.markdown("(\u26a0\ufe0f \uadf8\ub9ac\uace0 \uac00\uc7a5 \uc800\ub834\ud55c OTT \ucd94\ucc9c\uae30 \uac00\uc131\ube44 \uacc4\uc0b0\ub294 \ub2e4\uc74c\uc5d0 \ubcf4\ud638\ub428.)")
st.markdown("- \uac00성\ube44 = OTT \uac00격 / (원하는 \ucee8텐\uce20 \uc218 * \uc774용\uc790 수)")

# 추가 개발필: \uc120\ud0dd한 컨텐\uce20 목록의 OTT 제공 공급자 정보를 얻어서, 
# OTT \ubcc0수에 \ubc18영\ud558여 \uac00성\ube44 \uacc4산 결과 표시

# (추가필요) 가격 데이\ud130와 OTT 역시 로\uace0 결과 보기
st.warning("\u26a0\ufe0f \uc800\ub834\ud55c OTT \uacc4산 \uae30본 \uae30능\uc740 \ud604재 \uadf8리\uace0 \uc788지\ub9cc, \uacc4산\uae30\ub97c \uc644\uc804\ud654\ud574\uc11c \uac00장 \uc800\ub834\ud55c OTT \ud45c준\uc744 \ubcf4\uc5ec주는 \ud615식\uc740 \uc870\ub9cc\uac04 \uad6c현\ud560\uacc4\ud569\ub2c8\ub2e4.")
