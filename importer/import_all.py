"""
LaundryBot V6

Import All PDF
"""

from pathlib import Path

from importer.pdf_reader import read_pdf
from importer.debug_export import save_debug
from importer.detect_document import detect_document

from importer.service_report_parser import parse
from importer.summary_report_parser import parse_summary

from services.import_service import save_service_report


def import_all(folder):

    folder = Path(folder)

    if not folder.exists():

        print(f"Folder not found : {folder}")

        return

    pdfs = sorted(folder.glob("*.pdf"))

    print("=" * 70)
    print("LaundryBot PDF Import")
    print("=" * 70)

    print(f"พบไฟล์ {len(pdfs)} ไฟล์\n")

    success = 0
    duplicate = 0
    error = 0

    required = [
        "job_no",
        "customer",
    ]

    for pdf in pdfs:

        print("-" * 70)
        print(f"FILE : {pdf.name}")

        try:

            # =====================================================
            # Read PDF
            # =====================================================

            text = read_pdf(pdf)

            save_debug(pdf, text)

            # =====================================================
            # Detect Document Type
            # =====================================================

            doc_type = detect_document(text)

            print("=" * 60)
            print("DEBUG DETECT")
            print("=" * 60)
            print(text[:400])
            print("=" * 60)
            print("TYPE =", doc_type)
            print("=" * 60)
            # =====================================================
            # SERVICE REPORT
            # =====================================================

            if doc_type == "service_report":

                data = parse(text)

                missing = [
                    field
                    for field in required
                    if not data.get(field)
                ]

                if missing:

                    print(f"⚠ Missing : {', '.join(missing)}")

                print("=" * 60)

                for k, v in data.items():

                    if v:

                        print(f"{k:15} : {v}")

                print("=" * 60)

                saved = save_service_report(data)

                if saved:

                    print("✅ Saved")

                    success += 1

                else:

                    print("⚠ Already Exists")

                    duplicate += 1

            # =====================================================
            # SUMMARY REPORT
            # =====================================================

            elif doc_type == "summary_report":

                jobs = parse_summary(text)

                print(f"พบ {len(jobs)} งาน")

                for job in jobs:

                    print("-" * 50)

                    print(job.get("job_no", ""))

                    saved = save_service_report(job)

                    if saved:

                        success += 1

                        print("✅ Saved")

                    else:

                        duplicate += 1

                        print("⚠ Already Exists")

            # =====================================================
            # PARTS MANUAL
            # =====================================================

            elif doc_type == "parts_manual":

                print("📘 Parts Manual")

            # =====================================================
            # UNKNOWN
            # =====================================================

            else:

                print("⚠ Unknown Document")

        except Exception as e:

            print(f"❌ ERROR : {pdf.name}")

            print(e)

            error += 1

        print()

    print("=" * 70)
    print("IMPORT SUMMARY")
    print("=" * 70)
    print(f"Total Files     : {len(pdfs)}")
    print(f"Saved           : {success}")
    print(f"Already Exists  : {duplicate}")
    print(f"Errors          : {error}")
    print("=" * 70)