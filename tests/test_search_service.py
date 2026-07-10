from search.search_service import search_everything

result = search_everything(
    "DI225",
    "steam"
)

print(result["parts"])

print(result["manual"])

print(result["repair"])