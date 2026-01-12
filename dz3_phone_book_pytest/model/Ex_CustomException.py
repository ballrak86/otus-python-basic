class CustomException(Exception):
    def __init__(self, message: str, string: str):
        self.message = f'{message} {string}'
        super().__init__(self.message)
