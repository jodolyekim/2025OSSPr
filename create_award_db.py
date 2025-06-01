import sqlite3

def main():
    conn = sqlite3.connect("award_winners.db")
    cur  = conn.cursor()

    for tbl in ("cannes_winners","berlin_winners","venice_winners"):
        cur.execute(f"DROP TABLE IF EXISTS {tbl};")

    cur.execute("""
    CREATE TABLE cannes_winners (
        year     INTEGER NOT NULL,
        title_ko TEXT    NOT NULL    -- 한글 제목만
    );
    """)
    cur.execute("""
    CREATE TABLE berlin_winners (
        year     INTEGER NOT NULL,
        title_ko TEXT    NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE venice_winners (
        year     INTEGER NOT NULL,
        title_ko TEXT    NOT NULL
    );
    """)
    conn.commit()
    conn.close()
    print("✅ 한글 제목만 쓰는 festival tables 생성 완료")

if __name__ == "__main__":
    main()
