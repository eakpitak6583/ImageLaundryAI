from pathlib import Path
import sqlite3
import fitz
from tqdm import tqdm

# -----------------------------
# Path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

PDF_FOLDER = BASE_DIR / "manuals" / "pdf"
DB_FILE = BASE_DIR / "database" / "laundry.db"

# -----------------------------
# Database
# -----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# -----------------------------
# อ่านทุก PDF
# -----------------------------
pdf_files = list(PDF_FOLDER.glob("*.pdf"))

print("=" * 60)
print(f"พบ Manual ทั้งหมด {len(pdf_files)} ไฟล์")
print("=" * 60)

for pdf in tqdm(pdf_files):

    print(f"\nกำลังอ่าน : {pdf.name}")

    doc = fitz.open(pdf)

    model = pdf.stem

    # เพิ่ม Machine ถ้ายังไม่มี
    cursor.execute("""
        INSERT OR IGNORE INTO machines(
            brand,
            model,
            machine_type,
            manual_file
        )
        VALUES(
            ?,?,?,?
        )
    """, (
        "IMAGE",
        model,
        "",
        pdf.name
    ))

    # อ่านทุกหน้า
    for page_number in range(len(doc)):

        page = doc.load_page(page_number)

        text = page.get_text()

        cursor.execute("""
            INSERT INTO manual_pages(
                model,
                page,
                content
            )
            VALUES(
                ?,?,?
            )
        """, (
            model,
            page_number + 1,
            text
        ))

    doc.close()

conn.commit()
conn.close()

print("\n")
print("=" * 60)
print("Manual Import Complete")
print("=" * 60)