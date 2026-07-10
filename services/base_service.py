class BaseService:

    def success(self, data=None):
        return {
            "success": True,
            "data": data
        }

    def error(self, message):
        return {
            "success": False,
            "message": message
        }