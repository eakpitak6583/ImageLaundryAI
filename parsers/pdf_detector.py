from parsers.pdf_reader import read_pdf


def detect_pdf_type(file_path):

    pages = read_pdf(file_path)

    text = ""

    for page in pages[:2]:
        text += page["text"].lower()

    if "service control order" in text:
        return "service"

    if "บทสรุปงานซ่อม" in text:
        return "summary"

    return "unknown"