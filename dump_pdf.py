from importer.pdf_reader import read_pdf

text = read_pdf("service_reports/pdf/Service Control Order JOB6903-1019.pdf")

with open(
    "service_reports/debug.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("Done")