import pdfplumber

with pdfplumber.open("repair_reports/เคลียร์เบี้ยเลี้ยงช่าง.pdf") as pdf:

    text = ""

    for page in pdf.pages:
        text += page.extract_text() + "\n"

print(text[:3000])
