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