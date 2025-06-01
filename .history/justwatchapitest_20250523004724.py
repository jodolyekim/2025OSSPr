from justwatch import JustWatch

justwatch = JustWatch(country='US')
results = justwatch.search_for_item(query='Interstellar')
print(results['items'][0]['offers'])
