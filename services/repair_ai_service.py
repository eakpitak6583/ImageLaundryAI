    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):

        self.client = OpenAI(

            api_key=Config.OPENAI_API_KEY,

        )

        logger.info(

            "Repair AI Service Initialized"

        )
    # ==========================================================
    # Build Prompt
    # ==========================================================

    def build_prompt(

        self,

        report_text,

    ):

        prompt = prompt_service.repair_prompt()

        if report_text is None:

            report_text = ""

        report_text = str(

            report_text

        ).strip()

        return f"""

{prompt}

============================================================
REPAIR REPORT
============================================================

{report_text}

============================================================
IMPORTANT
============================================================

- อ่านรายงานทั้งหมด
- รองรับใบงานซ่อมทั้ง 2 รูปแบบ
- หากไม่มีข้อมูลให้คืนค่าเป็น ""
- ตอบกลับเป็น JSON เท่านั้น
- ห้ามอธิบายเพิ่มเติม
- ห้ามใส่ Markdown
- ห้ามใส่ ```json

"""
    # ==========================================================
    # Read PDF
    # ==========================================================

    def read_pdf(

        self,

        filepath,

    ):

        logger.info(

            "Reading PDF : %s",

            filepath,

        )

        if not filepath:

            raise ValueError(

                "PDF path is empty."

            )

        text = pdf_service.read(

            filepath

        )

        if text is None:

            text = ""

        text = str(

            text

        ).strip()

        if text == "":

            raise ValueError(

                "Unable to extract text from PDF."

            )

        logger.info(

            "PDF loaded successfully (%d characters)",

            len(text),

        )

        return text
