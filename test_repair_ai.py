from services.repair_ai_service import repair_ai_service

data = repair_ai_service.import_pdf(
    "uploads/repair_reports/test.pdf"
)

print(data)