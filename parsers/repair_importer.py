from pathlib import Path
import json
import pdfplumber

from database.db import connect
from parsers.repair_parser import split_jobs
from parsers.ai_repair_parser import parse_job

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "repair_reports"
CACHE_DIR = BASE_DIR / "cache"

CACHE_DIR.mkdir(exist_ok=True)

conn = connect()
cursor = conn.cursor()

pdf_files = sorted(PDF_DIR.glob("*.pdf"))

print("=" * 60)
print("Repair Import")
print("=" * 60)

for pdf in pdf_files:

    print(f"\nกำลังอ่าน : {pdf.name}")

    text = ""

    with pdfplumber.open(pdf) as doc:

        for page in doc.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    jobs = split_jobs(text)

    print(f"พบ {len(jobs)} JOB")

    for i, job_text in enumerate(jobs, start=1):

        try:

            data = parse_job(job_text)

            # -------------------------
            # Cache
            # -------------------------
            cache_file = CACHE_DIR / f"{data['job_no']}.json"

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # -------------------------
            # Database
            # -------------------------
            cursor.execute(
                """
                INSERT OR IGNORE INTO repair_history(
                    job_no,
                    machine_model,
                    complaint,
                    detail,
                    repair_action,
                    result,
                    sap_no,
                    serial_no,
                    report_file
                )
                VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    data["job_no"],
                    data["machine_model"],
                    data["complaint"],
                    data["detail"],
                    data["repair_action"],
                    data["result"],
                    data["sap_no"],
                    data["serial_no"],
                    pdf.name,
                ),
            )

            print(f"[{i:03}/{len(jobs)}] ✓ {data['job_no']}")

        except Exception as e:

            print(f"[{i:03}/{len(jobs)}] ✗ ERROR : {e}")

conn.commit()
conn.close()

print()
print("=" * 60)
print("Repair Import Complete")
print("=" * 60)