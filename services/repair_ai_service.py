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
    # ==========================================================
    # Ask OpenAI
    # ==========================================================

    def ask_ai(

        self,

        report_text,

    ):

        logger.info(

            "Sending repair report to OpenAI..."

        )

        prompt = self.build_prompt(

            report_text

        )

        try:

            response = self.client.responses.create(

                model=Config.MODEL_NAME,

                input=prompt,

            )

            result = response.output_text.strip()

            if result == "":

                raise ValueError(

                    "OpenAI returned empty response."

                )

            logger.info(

                "OpenAI response received."

            )

            return result

        except Exception as e:

            logger.exception(

                "OpenAI Error : %s",

                e,

            )

            raise
    # ==========================================================
    # Parse JSON
    # ==========================================================

    def parse_json(

        self,

        text,

    ):

        if text is None:

            raise ValueError(

                "OpenAI response is None."

            )

        text = str(

            text

        ).strip()

        if text == "":

            raise ValueError(

                "OpenAI returned empty response."

            )

        logger.info(

            "Parsing OpenAI JSON..."

        )

        if text.startswith(

            "```json"

        ):

            text = (

                text

                .replace(

                    "```json",

                    "",

                )

                .replace(

                    "```",

                    "",

                )

                .strip()

            )

        elif text.startswith(

            "```"

        ):

            text = (

                text

                .replace(

                    "```",

                    "",

                )

                .strip()

            )

        start = text.find("{")

        end = text.rfind("}")

        if start != -1 and end != -1:

            text = text[

                start:end + 1

            ]

        try:

            data = json.loads(

                text

            )

        except json.JSONDecodeError as e:

            logger.exception(

                "Invalid JSON : %s",

                e,

            )

            logger.error(

                text

            )

            raise ValueError(

                "OpenAI returned invalid JSON."

            )

        logger.info(

            "JSON parsed successfully."

        )

        return data

