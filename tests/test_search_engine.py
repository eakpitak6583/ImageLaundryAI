from search.search_engine import (
    search_parts,
    search_manual,
    search_repair,
)

print("="*60)
print("PARTS")
print("="*60)

for row in search_parts("DI225", "Steam"):
    print(row)

print()

print("="*60)
print("MANUAL")
print("="*60)

for row in search_manual("DI225", "Steam"):
    print(row)

print()

print("="*60)
print("REPAIR")
print("="*60)

for row in search_repair("DI225", "Steam"):
    print(row)