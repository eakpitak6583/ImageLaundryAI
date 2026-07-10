import fitz


def read_pdf(file_path):
    """
    อ่านข้อความจาก PDF

    Parameters
    ----------
    file_path : Path | str
        ตำแหน่งไฟล์ PDF

    Returns
    -------
    list
        [
            {
                "page": 1,
                "text": "ข้อความ..."
            },
            ...
        ]
    """

    pages = []

    try:

        with fitz.open(file_path) as doc:

            for page_no, page in enumerate(doc, start=1):

                text = page.get_text("text").strip()

                pages.append(
                    {
                        "page": page_no,
                        "text": text,
                    }
                )

    except Exception as e:

        print(f"Error reading PDF : {file_path}")
        print(e)

    return pages