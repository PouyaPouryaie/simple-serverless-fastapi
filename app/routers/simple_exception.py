
class CustomException(Exception):
    def __init__(self, statusCode: int, message: str):
        self.statusCode = statusCode
        self.message = message