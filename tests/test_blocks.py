from pathlib import Path
import fitz

PDF = Path("manuals/pdf").glob("*.pdf")

pdf_file = next(PDF)

print("=" * 60)
print(pdf_file.name)
print("=" * 60)

doc = fitz.open(pdf_file)

page = doc.load_page(2)      # หน้า 3

blocks = page.get_text("blocks")

for b in blocks:

    print("-" * 60)

    print(b[4])

doc.close()