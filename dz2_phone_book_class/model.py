class EmptyData(Exception):
    def __init__(self, message: str):
        self.message = f'{message} cannot be empty'
        super().__init__(self.message)


class CheckIsDigit(Exception):
    def __init__(self, message: str):
        self.message = f'{message} is not a digit'
        super().__init__(self.message)


class Contact:
    def __init__(self, name: str, phone: int, comment: str) -> None:
        if name == '' or phone == '':
            raise ValueError("name or phone cannot be empty")
        # if not phone.isdigit():
        #     raise ValueError("phone can contain only numbers")
        self.name = name
        self.phone = phone
        self.comment = comment


class Directory(Contact):
    max_id = 0

    def __init__(self, id_directory: int, name: str, phone: int, comment: str) -> None:
        super().__init__(name, phone, comment)
        self.id_directory = id_directory
        if self.id_directory >= Directory.max_id:
            Directory.max_id = self.id_directory + 1

    @classmethod
    def new_contact(cls, json_contact: dict):
        return cls(**json_contact)

    def set_contact(self, id_directory: int, name: str, phone: int, comment: str) -> None:
        self.id_directory = id_directory
        self.name = name
        self.phone = phone
        self.comment = comment

    def find_contact(self, value):
        if value == self.id_directory or value == self.name or value == self.phone or value == self.comment:
            return self
        else:
            return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and all(
            getattr(self, attr) == getattr(other, attr) for attr in vars(self))

    def __repr__(self):
        return f'{self.id_directory} {self.name} {self.phone} {self.comment}'


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
