"""
LaundryBot V7 Enterprise
Prompt Service
"""

import logging
from pathlib import Path

from config import (
    Config,
)

logger = logging.getLogger(
    __name__,
)


class PromptService:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        self.prompt_folder = Path(

            Config.PROMPT_FOLDER,

        ).resolve()

        self.cache = {}

        logger.info(

            "Prompt Service Initialized"

        )

    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        exists = self.prompt_folder.exists()

        return {

            "success": exists,

            "service": "prompt_service",

            "prompt_folder": str(

                self.prompt_folder,

            ),

            "cache_size": len(

                self.cache,

            ),

            "status": (

                "ok"

                if exists

                else "missing"

            ),

        }
    # ==========================================================
    # Load Prompt
    # ==========================================================

    def load(

        self,

        filename,

        use_cache=True,

    ):

        filename = str(

            filename or "",

        ).strip()

        if filename == "":

            raise ValueError(

                "Prompt filename is required."

            )

        if use_cache and filename in self.cache:

            logger.info(

                "Using cached prompt : %s",

                filename,

            )

            return self.cache[

                filename

            ]

        path = self.prompt_folder / filename

        if not path.is_file():

            logger.error(

                "Prompt file not found : %s",

                path,

            )

            raise FileNotFoundError(

                path,

            )

        try:

            logger.info(

                "Loading prompt : %s",

                filename,

            )

            prompt = path.read_text(

                encoding="utf-8",

            )

            prompt = prompt.strip()

            if prompt == "":

                raise ValueError(

                    f"Prompt file is empty : {filename}"

                )

            self.cache[

                filename

            ] = prompt

            logger.info(

                "Prompt loaded successfully."

            )

            return prompt

        except Exception as e:

            logger.exception(

                "Unable to load prompt %s : %s",

                filename,

                e,

            )

            raise
    # ==========================================================
    # Render Prompt
    # ==========================================================

    def render(

        self,

        filename,

        **kwargs,

    ):

        prompt = self.load(

            filename,

        )

        if not kwargs:

            return prompt

        logger.info(

            "Rendering prompt : %s",

            filename,

        )

        for key, value in kwargs.items():

            if value is None:

                value = ""

            prompt = prompt.replace(

                "{{" + key + "}}",

                str(

                    value,

                ),

            )

        logger.info(

            "Prompt rendered successfully."

        )

        return prompt

    # ==========================================================
    # Render Text
    # ==========================================================

    def render_text(

        self,

        prompt,

        **kwargs,

    ):

        if prompt is None:

            return ""

        prompt = str(

            prompt,

        )

        for key, value in kwargs.items():

            if value is None:

                value = ""

            prompt = prompt.replace(

                "{{" + key + "}}",

                str(

                    value,

                ),

            )

        return prompt
    # ==========================================================
    # Repair Prompt
    # ==========================================================

    def repair_prompt(

        self,

        **kwargs,

    ):

        return self.render(

            "repair_prompt.txt",

            **kwargs,

        )

    # ==========================================================
    # RAG Prompt
    # ==========================================================

    def rag_prompt(

        self,

        **kwargs,

    ):

        return self.render(

            "rag_prompt.txt",

            **kwargs,

        )

    # ==========================================================
    # PM Prompt
    # ==========================================================

    def pm_prompt(

        self,

        **kwargs,

    ):

        return self.render(

            "pm_prompt.txt",

            **kwargs,

        )

    # ==========================================================
    # Checklist Prompt
    # ==========================================================

    def checklist_prompt(

        self,

        **kwargs,

    ):

        return self.render(

            "checklist_prompt.txt",

            **kwargs,

        )

    # ==========================================================
    # Dashboard Prompt
    # ==========================================================

    def dashboard_prompt(

        self,

        **kwargs,

    ):

        return self.render(

            "dashboard_prompt.txt",

            **kwargs,

        )

    # ==========================================================
    # Generic Prompt
    # ==========================================================

    def prompt(

        self,

        filename,

        **kwargs,

    ):

        return self.render(

            filename,

            **kwargs,

        )

    # ==========================================================
    # Build Repair Prompt
    # ==========================================================

    def build_repair_prompt(

        self,

        report_text,

    ):

        logger.info(

            "Building repair prompt."

        )

        return self.repair_prompt(

            report_text=report_text,

        )
    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(

        self,

    ):

        return {

            "prompt_folder": str(

                self.prompt_folder,

            ),

            "cache_size": len(

                self.cache,

            ),

            "cached_files": sorted(

                self.cache.keys(),

            ),

        }

    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        exists = self.prompt_folder.exists()

        readable = (

            self.prompt_folder.is_dir()

            if exists

            else False

        )

        return {

            "success": exists and readable,

            "service": "prompt_service",

            "prompt_folder": str(

                self.prompt_folder,

            ),

            "cache_size": len(

                self.cache,

            ),

            "status": (

                "ok"

                if exists and readable

                else "missing"

            ),

        }

    # ==========================================================
    # Version
    # ==========================================================

    def version(

        self,

    ):

        return {

            "name": "LaundryBot V7 Enterprise",

            "module": "Prompt Service",

            "version": getattr(

                Config,

                "VERSION",

                "7.0",

            ),

        }
    # ==========================================================
    # Clear Cache
    # ==========================================================

    def clear_cache(

        self,

    ):

        logger.info(

            "Clearing prompt cache."

        )

        self.cache.clear()

    # ==========================================================
    # Reload Prompt
    # ==========================================================

    def reload(

        self,

        filename,

    ):

        filename = str(

            filename or "",

        ).strip()

        if filename == "":

            raise ValueError(

                "Prompt filename is required."

            )

        logger.info(

            "Reloading prompt : %s",

            filename,

        )

        self.cache.pop(

            filename,

            None,

        )

        return self.load(

            filename,

            use_cache=False,

        )

    # ==========================================================
    # Reload All Prompts
    # ==========================================================

    def reload_all(

        self,

    ):

        logger.info(

            "Reloading all prompts."

        )

        self.clear_cache()

        loaded = []

        for path in sorted(

            self.prompt_folder.glob(

                "*.txt",

            )

        ):

            self.load(

                path.name,

                use_cache=False,

            )

            loaded.append(

                path.name,

            )

        logger.info(

            "Reloaded %s prompt(s).",

            len(

                loaded,

            ),

        )

        return loaded
