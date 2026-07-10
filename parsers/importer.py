from pathlib import Path
import shutil

from parsers.manual_pdf_importer import import_manual_pdf
from parsers.service_pdf_importer import import_service_pdf
from parsers.summary_pdf_importer import import_summary_pdf
from parsers.pdf_detector import detect_pdf_type

from services.import_log_service import save_import_log


# =====================================================
# Folder
# =====================================================

KNOWLEDGE = Path("knowledge")

MANUALS = KNOWLEDGE / "manuals"
REPORTS = KNOWLEDGE / "service_reports"
IMPORTED = KNOWLEDGE / "imported"

SUPPORTED_EXTENSIONS = {".pdf"}


# =====================================================
# Scan Folder
# =====================================================

def scan_files(folder: Path):

    if not folder.exists():
        return []

    return sorted(
        file
        for file in folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )


# =====================================================
# Import All
# =====================================================

def import_all():

    IMPORTED.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = []

    results.extend(import_folder(MANUALS, "manual"))
    results.extend(import_folder(REPORTS, "service_report"))

    return results


# =====================================================
# Import Folder
# =====================================================

def import_folder(folder: Path, document_type: str):

    results = []

    for file in scan_files(folder):

        results.append(
            process_file(
                file=file,
                document_type=document_type,
            )
        )

    return results


# =====================================================
# Process File
# =====================================================

def process_file(file: Path, document_type: str):

    destination = IMPORTED / file.name

    # -----------------------------
    # Duplicate
    # -----------------------------

    if destination.exists():

        return finish(
            filename=file.name,
            document_type=document_type,
            status="SKIP",
            records=0,
        )

    try:

        # -----------------------------
        # Manual PDF
        # -----------------------------

        if document_type == "manual":

            records = import_manual_pdf(file)

        # -----------------------------
        # Service Report PDF
        # -----------------------------

        elif document_type == "service_report":

            pdf_type = detect_pdf_type(file)

            if pdf_type == "service":

                records = import_service_pdf(file)

            elif pdf_type == "summary":

                records = import_summary_pdf(file)

            else:

                raise Exception(
                    f"Unknown Service Report Format : {file.name}"
                )

        # -----------------------------
        # Unsupported
        # -----------------------------

        else:

            return finish(
                filename=file.name,
                document_type=document_type,
                status="UNSUPPORTED",
                records=0,
            )

        # -----------------------------
        # Move File
        # -----------------------------

        shutil.move(
            str(file),
            str(destination),
        )

        return finish(
            filename=file.name,
            document_type=document_type,
            status="SUCCESS",
            records=records,
        )

    except Exception as e:

        return finish(
            filename=file.name,
            document_type=document_type,
            status="ERROR",
            records=0,
            error=str(e),
        )


# =====================================================
# Finish
# =====================================================

def finish(
    filename,
    document_type,
    status,
    records,
    error=None,
):

    save_import_log(
        filename=filename,
        document_type=document_type,
        status=status,
        records=records,
    )

    result = {
        "filename": filename,
        "document_type": document_type,
        "status": status,
        "records": records,
    }

    if error:
        result["error"] = error

    return result