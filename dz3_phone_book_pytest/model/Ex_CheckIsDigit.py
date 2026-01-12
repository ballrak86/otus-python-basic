from .Ex_CustomException import CustomException


class CheckIsDigit(CustomException):
    def __init__(self, message: str):
        self.message = message
        self.string = 'is not a digit'
        super().__init__(self.message, self.string)
