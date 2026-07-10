from analytics.failure import (
    top_failures,
    top_parts,
    top_problems,
)

print("="*60)
print("FAILURES")
print("="*60)

print(top_failures("DI225"))

print()

print("="*60)
print("TOP COMPLAINT")
print("="*60)

print(top_problems("DI225"))

print()

print("="*60)
print("TOP PARTS")
print("="*60)

print(top_parts("DI475"))