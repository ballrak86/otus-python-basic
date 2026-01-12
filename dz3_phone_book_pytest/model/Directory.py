from .Contact import Contact


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
