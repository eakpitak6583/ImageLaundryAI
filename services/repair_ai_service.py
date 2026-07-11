"""
LaundryBot V7 Enterprise
Repair AI Service
"""

import json
import logging

from openai import OpenAI

from config import Config

from services.pdf_service import (
    pdf_service,
)

from services.prompt_service import (
    prompt_service,
)

from services.customer_mapper import (
    customer_mapper,
)

from services.machine_mapper import (
    machine_mapper,
)

from services.technician_mapper import (
    technician_mapper,
)


logger = logging.getLogger(__name__)


class RepairAIService:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

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

            filepath,

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

            report_text,

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

                text,

            )

        except json.JSONDecodeError as e:

            logger.exception(

                "Invalid JSON : %s",

                e,

            )

            logger.error(

                text,

            )

            raise ValueError(

                "OpenAI returned invalid JSON."

            )

        logger.info(

            "JSON parsed successfully."

        )

        return data

    # ==========================================================
    # Extract PDF
    # ==========================================================
        def extract_pdf(

        self,

        filepath,

    ):

        logger.info(

            "Starting AI Extraction..."

        )

        report_text = self.read_pdf(

            filepath,

        )

        logger.info(

            "Building AI Prompt..."

        )

        ai_response = self.ask_ai(

            report_text,

        )

        logger.info(

            "Parsing AI Response..."

        )

        data = self.parse_json(

            ai_response,

        )

        if not isinstance(

            data,

            dict,

        ):

            raise ValueError(

                "OpenAI response is not JSON Object."

            )

        logger.info(

            "AI Extraction Completed."

        )

        logger.info(

            "Fields Extracted : %s",

            len(data),

        )

        return data

    # ==========================================================
    # Normalize
    # ==========================================================

    def normalize(

        self,

        data,

    ):

        logger.info(

            "Normalizing AI data..."

        )

        if data is None:

            data = {}

        fields = [

            "job_no",

            "brand",

            "machine_model",

            "sap_no",

            "serial_no",

            "customer",

            "complaint",

            "detail",

            "repair_action",

            "result",

            "technician",

            "employee_code",

            "repair_date",

        ]

        result = {}

        for field in fields:

            value = data.get(

                field,

                "",

            )

            if value is None:

                value = ""

            if not isinstance(

                value,

                str,

            ):

                value = str(

                    value,

                )

            result[field] = value.strip()

        logger.info(

            "Normalize completed."

        )

        return result

    # ==========================================================
    # Validate
    # ==========================================================
        def validate(

        self,

        data,

    ):

        logger.info(

            "Validating AI data..."

        )

        if not isinstance(

            data,

            dict,

        ):

            raise ValueError(

                "AI data must be dictionary."

            )

        required_fields = [

            "machine_model",

            "complaint",

        ]

        for field in required_fields:

            value = str(

                data.get(

                    field,

                    "",

                )

            ).strip()

            if value == "":

                logger.warning(

                    "Missing required field : %s",

                    field,

                )

        optional_fields = [

            "job_no",

            "brand",

            "sap_no",

            "serial_no",

            "customer",

            "technician",

            "employee_code",

            "repair_action",

            "detail",

            "result",

            "repair_date",

        ]

        for field in optional_fields:

            data.setdefault(

                field,

                "",

            )

        logger.info(

            "Validation completed."

        )

        return data

    # ==========================================================
    # Detect Report Type
    # ==========================================================

    def detect_report_type(

        self,

        data,

    ):

        logger.info(

            "Detecting report type..."

        )

        if str(

            data.get(

                "job_no",

                "",

            )

        ).strip():

            return "service_report"

        if str(

            data.get(

                "complaint",

                "",

            )

        ).strip():

            return "repair_report"

        if (

            str(

                data.get(

                    "repair_action",

                    "",

                )

            ).strip()

            or

            str(

                data.get(

                    "result",

                    "",

                )

            ).strip()

        ):

            return "ai_repair"

        return "unknown"

    # ==========================================================
    # Clean Result
    # ==========================================================

    def clean_result(

        self,

        data,

    ):

        cleaned = {}

        for key, value in data.items():

            if value is None:

                value = ""

            value = str(

                value,

            )

            value = value.replace(

                "\u00A0",

                " ",

            )

            value = value.replace(

                "\r",

                " ",

            )

            value = value.replace(

                "\n",

                " ",

            )

            value = " ".join(

                value.split()

            )

            cleaned[key] = value.strip()

        return cleaned

    # ==========================================================
    # Default Fields
    # ==========================================================

    def default_fields(

        self,

        data,

    ):

        defaults = {

            "job_no": "",

            "repair_date": "",

            "brand": "",

            "machine_model": "",

            "sap_no": "",

            "serial_no": "",

            "customer": "",

            "complaint": "",

            "detail": "",

            "repair_action": "",

            "result": "",

            "technician": "",

            "employee_code": "",

            "document_type": "",

            "report_file": "",

            "customer_id": None,

            "machine_id": None,

            "technician_id": None,

        }

        for key, value in defaults.items():

            data.setdefault(

                key,

                value,

            )

        return data

    # ==========================================================
    # Prepare
    # ==========================================================

    def prepare(

        self,

        filepath,

    ):

        logger.info(

            "Preparing AI data..."

        )

        data = self.extract_pdf(

            filepath,

        )

        data = self.normalize(

            data,

        )

        data = self.validate(

            data,

        )

        data = self.clean_result(

            data,

        )

        data = self.default_fields(

            data,

        )

        data["document_type"] = self.detect_report_type(

            data,

        )

        logger.info(

            "Prepare completed."

        )

        return data

    # ==========================================================
    # Mapping
    # ==========================================================
        def mapping(

        self,

        data,

    ):

        logger.info(

            "Start Mapping..."

        )

        # ------------------------------------------------------
        # Customer
        # ------------------------------------------------------

        customer = customer_mapper.mapping(

            data,

        )

        if customer:

            data.update(

                customer,

            )

        logger.info(

            "Customer ID : %s",

            data.get(

                "customer_id",

            ),

        )

        # ------------------------------------------------------
        # Machine
        # ------------------------------------------------------

        machine = machine_mapper.mapping(

            data,

            data.get(

                "customer_id",

            ),

        )

        if machine:

            data.update(

                machine,

            )

        logger.info(

            "Machine ID : %s",

            data.get(

                "machine_id",

            ),

        )

        # ------------------------------------------------------
        # Technician
        # ------------------------------------------------------

        technician = technician_mapper.mapping(

            data,

        )

        if technician:

            data.update(

                technician,

            )

        logger.info(

            "Technician ID : %s",

            data.get(

                "technician_id",

            ),

        )

        logger.info(

            "Mapping completed."

        )

        return data

    # ==========================================================
    # Import PDF
    # ==========================================================

    def import_pdf(

        self,

        filepath,

    ):

        logger.info(

            "=" * 60

        )

        logger.info(

            "AI Repair Import Started"

        )

        logger.info(

            "File : %s",

            filepath,

        )

        data = self.prepare(

            filepath,

        )

        data = self.mapping(

            data,

        )

        data["report_file"] = filepath

        logger.info(

            "AI Repair Import Completed"

        )

        logger.info(

            "Job No : %s",

            data.get(

                "job_no",

            ),

        )

        logger.info(

            "Machine : %s",

            data.get(

                "machine_model",

            ),

        )

        logger.info(

            "Customer ID : %s",

            data.get(

                "customer_id",

            ),

        )

        logger.info(

            "Machine ID : %s",

            data.get(

                "machine_id",

            ),

        )

        logger.info(

            "Technician ID : %s",

            data.get(

                "technician_id",

            ),

        )

        logger.info(

            "=" * 60

        )

        return data

    # ==========================================================
    # Safe Import
    # ==========================================================

    def safe_import(

        self,

        filepath,

    ):

        logger.info(

            "Safe Import Started"

        )

        try:

            result = self.import_pdf(

                filepath,

            )

            logger.info(

                "Safe Import Success"

            )

            return result

        except FileNotFoundError:

            logger.exception(

                "PDF file not found."

            )

            raise

        except json.JSONDecodeError:

            logger.exception(

                "Invalid JSON returned from OpenAI."

            )

            raise

        except ValueError as e:

            logger.exception(

                "Validation Error : %s",

                e,

            )

            raise

        except Exception as e:

            logger.exception(

                "Unexpected Error : %s",

                e,

            )

            raise


# ==========================================================
# Singleton
# ==========================================================

repair_ai_service = RepairAIService()