import pdfplumber

from parsers.repair_parser import split_jobs
from parsers.ai_repair_parser import parse_job

pdf = "repair_reports/เคลียร์เบี้ยเลี้ยงช่าง.pdf"

text = ""

with pdfplumber.open(pdf) as doc:

    for page in doc.pages:

        t = page.extract_text()

        if t:
            text += t + "\n"

jobs = split_jobs(text)

job = parse_job(jobs[2])

print(job)
