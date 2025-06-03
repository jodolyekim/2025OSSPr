import streamlit as st
import sqlite3
import pandas as pd
from contents_search import get_movie_summary
import os

# award_winners.db에 수상년도, 영화명, 영화의 tmdb상 id 저장
DB_PATH = "award_winners.db"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w342"

st.set_page_config(page_title="🏆 3대 영화제 수상작", layout="wide")
st.title("🏆 세계 3대 영화제 연도별 수상작")

# 영화제 로고 매핑
LOGO_FILES = {
    "칸 영화제 (Palme d'Or)": "cannes.png",
    "베를린 영화제 (Golden Bear)": "berlin.png",
    "베니스 영화제 (Golden Lion)": "venice.png",
}

# images 폴더에 각 영화제 로고 저장되어있음
BASE_DIR = os.getcwd()
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# 영화제 <-> (테이블명, 공개연도 오프셋)
festival_map = {
    "칸 영화제 (Palme d'Or)": ("cannes_winners",  0),
    "베를린 영화제 (Golden Bear)": ("berlin_winners", -1),
    "베니스 영화제 (Golden Lion)": ("venice_winners", -1),
}

# award_winners.db의 데이터 긁어오기
# sqlite3 이용: 각 영화제 테이블로부터 년도, 영화명, id 긁어오기
def load_table(table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT year, title_ko, tmdb_id FROM {table_name} ORDER BY year DESC",
        conn
    )
    conn.close()
    return df

# 사이드바에 수상 년도 선택할 수 있도록 함
all_years = set()
for tbl, _ in festival_map.values():
    all_years |= set(load_table(tbl)["year"])
year = st.sidebar.selectbox("🔢 연도 선택", sorted(all_years, reverse=True))

# 3열 레이아웃 - 칸, 베를린, 베니스 순서
cols = st.columns(3, gap="small")
for (label, (table, offset)), col in zip(festival_map.items(), cols):
    with col:
        # 로고 + 서브헤더
        logo_file = LOGO_FILES.get(label)
        if logo_file:
            img_path = os.path.join(IMAGES_DIR, logo_file)
            # 파일명만 붙였을 때 정상 경로를 가리키는지 확인
            try:
                with open(img_path, "rb") as f:
                    col.image(f.read(), width=200)        # 로고 표시
            except FileNotFoundError:
                st.warning(f"로고 파일을 찾을 수 없습니다: {img_path}")
        col.markdown(f"**{label}**")                   # 굵은 제목

        df = load_table(table)
        entry = df[df["year"] == year]
        if entry.empty:
            st.info("해당 연도 수상작이 없습니다.")
            continue

        row = entry.iloc[0]
        title_ko = row["title_ko"]
        tmdb_id = row["tmdb_id"]
        display_yr = year + offset

        # id 기반으로 포스터, 평점, 줄거리, 제목, 개봉년도 반환
        summary = get_movie_summary(tmdb_id, "movie", lang="ko-KR")

        # 포스터
        poster = summary["poster_path"]
        if poster:
            st.image(f"{TMDB_IMAGE_BASE}{poster}", use_container_width=True)
        else:
            st.write("포스터 정보 없음")

        # 제목 + 공개연도
        title_en = summary["title"] or title_ko
        st.markdown(f"**{title_en}** ({display_yr})")

        # 평점
        vote = summary["vote_average"]
        if vote is not None:
            st.markdown(f"⭐ 평점: {vote:.1f}")
        else:
            st.markdown("⭐ 평점 정보 없음")

        # 줄거리
        overview = summary["overview"]
        if overview:
            st.write(overview)

        # mbti 페이지처럼, 바로 검색할 수 있도록 버튼 생성
        btn_key = f"search_{table}_{tmdb_id}"
        if st.button("🔍 메인에서 검색하기", key=btn_key):
            st.session_state["selected_movie_data"] = {
                "id": tmdb_id,
                "media_type": "movie",
                "title_ko": title_ko,
                "title_en": title_en,
                "poster_path": summary["poster_path"],
                "overview": overview,
                "vote_average": vote or 0.0,
                "release_date": summary["release_date"]
            }
            st.switch_page("home.py")
