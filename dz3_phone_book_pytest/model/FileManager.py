class FileManager:
    filename = 'phone_book.json'

    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(FileManager.filename, self.mode, encoding='UTF-8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
