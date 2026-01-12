def start_telephone_book() -> None:
    print("""Welcome to Phone Book
        First please open phone book
        1. default phone_book.csv'
        2. Your file json with the structure 'id_directory', 'name', 'phone', 'comment'""")


def menu() -> None:
    print("""**************
    Select Phone Book menu:
        1. Save Phone Book
        2. Show all contacts
        3. Create a contact
        4. Find a contact
        5. Edit a contact
        6. Delete a contact
        7. Exit
    """)


def input_from_user(text: str) -> str:
    input_text = input(text)
    return input_text


def output(text: str) -> None:
    print(text)


def print_contact(lst_phone_book: list) -> None:
    for item in lst_phone_book:
        print(item)
