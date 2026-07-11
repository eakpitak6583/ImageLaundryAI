"""
LaundryBot V7 Enterprise
Prompt Service
"""

from pathlib import Path

from config import Config


class PromptService:

    def __init__(self):

        self.prompt_path = (
            Path(Config.BASE_DIR)
            / "prompts"
        )

    # =====================================================
    # Load Prompt
    # =====================================================

    def load(self, filename):

        path = self.prompt_path / filename

        if not path.exists():

            raise FileNotFoundError(

                f"Prompt not found : {filename}"

            )

        return path.read_text(

            encoding="utf-8"

        )

    # =====================================================
    # Repair Prompt
    # =====================================================

    def repair_prompt(self):

        return self.load(

            "repair_prompt.txt"

        )

    # =====================================================
    # PM Prompt
    # =====================================================

    def pm_prompt(self):

        return self.load(

            "pm_prompt.txt"

        )

    # =====================================================
    # Checklist Prompt
    # =====================================================

    def checklist_prompt(self):

        return self.load(

            "checklist_prompt.txt"

        )

    # =====================================================
    # Dashboard Prompt
    # =====================================================

    def dashboard_prompt(self):

        return self.load(

            "dashboard_prompt.txt"

        )


prompt_service = PromptService()