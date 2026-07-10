import re


def split_jobs(text: str):
    """
    แยกข้อความออกเป็นแต่ละ JOB
    """

    pattern = r"(JOB\d{4}-\d{3})"

    matches = list(re.finditer(pattern, text))

    jobs = []

    for i, m in enumerate(matches):

        start = m.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        jobs.append(text[start:end].strip())

    return jobs


def extract_job(text: str):

    data = {
        "job_no": "",
        "machine_model": "",
        "complaint": "",
        "detail": "",
        "sap_no": "",
        "serial_no": "",
    }

    # --------------------------
    # Job No
    # --------------------------
    m = re.search(r"JOB\d{4}-\d{3}", text)

    if m:
        data["job_no"] = m.group(0)

    # --------------------------
    # Machine Model
    # --------------------------
    m = re.search(
        r"\b(DI-\d+|DP-\d+|SI-\d+|SP-\d+|XD-\d+|X-DRY\d+|IM\d+X\d+X\d+)\b",
        text,
        re.I,
    )

    if m:
        data["machine_model"] = m.group(1).replace("-", "")

    # --------------------------
    # SAP
    # --------------------------
    m = re.search(r"SAP\d+", text)

    if m:
        data["sap_no"] = m.group(0)

    # --------------------------
    # Serial Number
    # --------------------------
    m = re.search(r"[A-Z]\d{6,}/\d{6,}", text)

    if m:
        data["serial_no"] = m.group(0)

    # --------------------------
    # อ่านทีละบรรทัด
    # --------------------------
    lines = [x.strip() for x in text.splitlines()]

    for line in lines:

        if "Complaint" in line:

            if ":" in line:
                data["complaint"] = line.split(":", 1)[1].strip()

        elif "Detail" in line:

            if ":" in line:
                data["detail"] = line.split(":", 1)[1].strip()

    return data