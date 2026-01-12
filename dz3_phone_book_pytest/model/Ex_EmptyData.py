from .Ex_CustomException import CustomException


class EmptyData(CustomException):
    def __init__(self, message: str):
        self.message = message
        self.string = 'cannot be empty'
        super().__init__(self.message, self.string)
