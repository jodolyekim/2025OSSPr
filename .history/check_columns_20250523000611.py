import sqlite3

# ott_prices.db 파일 열기
conn = sqlite3.connect("ott_prices.db")
cursor = conn.cursor()

# 테이블 구조 확인
cursor.execute("PRAGMA table_info(ott_prices)")
columns = cursor.fetchall()

conn.close()

# 결과 출력
print("테이블 ott_prices의 컬럼 목록:")
for col in columns:
    print(f"- {col[1]} ({col[2]})")
