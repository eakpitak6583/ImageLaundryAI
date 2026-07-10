from ai.knowledge import load_parts
from ai.knowledge import load_repairs

print("="*60)
print("PARTS")
print("="*60)

for p in load_parts("DI475")[:5]:
    print(p)

print()

print("="*60)
print("REPAIR")
print("="*60)

for r in load_repairs("DI225")[:5]:
    print(r)