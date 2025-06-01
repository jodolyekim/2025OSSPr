import sqlite3

db_path = "ott_prices.db"  # 또는 ott_prices (6).db
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 현재 존재하는 테이블 목록 확인
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("✅ 현재 존재하는 테이블들:")
for t in tables:
    print("-", t[0])
