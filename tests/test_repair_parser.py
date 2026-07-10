from pathlib import Path
import pdfplumber

from parsers.repair_parser import split_jobs, extract_job

pdf = "repair_reports/เคลียร์เบี้ยเลี้ยงช่าง.pdf"

text = ""

with pdfplumber.open(pdf) as doc:

    for page in doc.pages:

        t = page.extract_text()

        if t:
            text += t + "\n"

jobs = split_jobs(text)

print("=" * 60)
print("จำนวน JOB =", len(jobs))
print("=" * 60)

job = extract_job(jobs[2])

print()

for k, v in job.items():

    print(f"{k:15} : {v}")