from justwatch import JustWatch

justwatch = JustWatch(country='KR')
results = justwatch.search_for_item(query='타짜')

print(results.get("items"))  # 이게 리스트로 나오면 정상 작동
