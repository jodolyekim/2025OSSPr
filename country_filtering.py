import streamlit as st

# 국가 선택
def select_country():
    country_name = st.selectbox("국가 선택", ["한국", "미국", "영국", "캐나다", "호주"])
    country_code_map = {
        "한국": "KR", "미국": "US", "영국": "GB", "캐나다": "CA", "호주": "AU"
    }
    country_code = country_code_map[country_name]
    return country_code
