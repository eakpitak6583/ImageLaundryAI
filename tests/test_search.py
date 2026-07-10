from search.part_search import search_part

keyword = input("Search : ")

rows = search_part(keyword)

print()
print("=" * 60)
print("Result :", len(rows))
print("=" * 60)

for part in rows:

    print(f"""
Model       : {part['model']}
Part No     : {part['part_no']}
Description : {part['description']}
Page        : {part['page']}
------------------------------------------------------------
""")