from database.db import connect

from parsers.pdf_reader import read_pdf
from parsers.service_report_parser import extract_service_data


def import_service_pdf(file_path):

    # ==========================================
    # อ่าน PDF
    # ==========================================

    pages = read_pdf(file_path)

    full_text = "\n".join(
        page["text"]
        for page in pages
    )

    # ==========================================
    # แยกข้อมูลจาก PDF
    # ==========================================

    data = extract_service_data(full_text)

    conn = connect()
    cursor = conn.cursor()

    # ==========================================
    # บันทึกลง documents
    # ==========================================

    for page in pages:

        cursor.execute(
            """
            INSERT INTO documents
            (
                filename,
                document_type,
                page,
                content
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                file_path.name,
                "service_report",
                page["page"],
                page["text"],
            ),
        )

    # ==========================================
    # บันทึกลง repair_history
    # ==========================================

    cursor.execute(
        """
        INSERT INTO repair_history
        (
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
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            data.get("job_no", ""),
            data.get("machine_model", ""),
            data.get("complaint", ""),
            data.get("detail", ""),
            data.get("repair_action", ""),
            data.get("result", ""),
            data.get("sap_no", ""),
            data.get("serial_no", ""),
            file_path.name,
        ),
    )

    conn.commit()
    conn.close()

    return len(pages)