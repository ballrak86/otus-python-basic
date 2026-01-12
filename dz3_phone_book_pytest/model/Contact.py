class Contact:
    def __init__(self, name: str, phone: int, comment: str) -> None:
        if name == '' or phone == '':
            raise ValueError("name or phone cannot be empty")
        self.name = name
        self.phone = phone
        self.comment = comment
