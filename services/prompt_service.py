"""
LaundryBot V7 Enterprise
Prompt Service
"""

from pathlib import Path

from config import Config


class PromptService:

    def __init__(self):

        self.prompt_folder = Path(
            Config.PROMPT_FOLDER
        )

    # ==========================================================
    # Load Prompt
    # ==========================================================

    def load(

        self,

        filename,

    ):

        path = self.prompt_folder / filename

        if not path.exists():

            raise FileNotFoundError(

                f"Prompt file not found : {path}"

            )

        return path.read_text(

            encoding="utf-8",

        )

    # ==========================================================
    # Repair Prompt
    # ==========================================================

    def repair_prompt(

        self,

    ):

        return self.load(

            "repair_prompt.txt",

        )

    # ==========================================================
    # PM Prompt
    # ==========================================================

    def pm_prompt(

        self,

    ):

        return self.load(

            "pm_prompt.txt",

        )

    # ==========================================================
    # Checklist Prompt
    # ==========================================================

    def checklist_prompt(

        self,

    ):

        return self.load(

            "checklist_prompt.txt",

        )

    # ==========================================================
    # Dashboard Prompt
    # ==========================================================

    def dashboard_prompt(

        self,

    ):

        return self.load(

            "dashboard_prompt.txt",

        )

    # ==========================================================
    # Build Repair Prompt
    # ==========================================================

    def build_repair_prompt(

        self,

        report_text,

    ):

        prompt = self.repair_prompt()

        return f"""

{prompt}

============================================================
REPAIR REPORT
============================================================

{report_text}

"""


prompt_service = PromptService()