import json
import model
import view


def start_app():
    """Запуск телефонного справочника"""
    view.start_telephone_book()
    open_file_item = input_open_file()
    lst_phone_book = open_file(open_file_item)
    print_menu(lst_phone_book)


def input_open_file() -> str:
    open_file_item = ''
    while open_file_item not in ['1', '2']:
        open_file_item = view.input_from_user('Select a menu item: ')
        if open_file_item not in ['1', '2']:
            view.output("Value error")
    return open_file_item


def open_file(open_file_item) -> list:
    """Открываем нужный файл и возвращаем список содержащий объекты с контактами"""
    if open_file_item == '1':
        with model.FileManager("r") as file:
            json_reader = json.load(file)
            lst_phone_book = []
            for item in json_reader:
                lst_phone_book.append(model.Directory.new_contact(item))
            view.print_contact(lst_phone_book)
    elif open_file_item == '2':
        while True:
            model.FileManager.filename = view.input_from_user('Write file name: ')
            try:
                with model.FileManager("r") as file:
                    json_reader = json.load(file)
                    lst_phone_book = []
                    for item in json_reader:
                        lst_phone_book.append(model.Directory.new_contact(item))
                    return lst_phone_book
            except FileNotFoundError:
                view.output('File not found')
                model.FileManager.filename = 'phone_book.json'
    return lst_phone_book


def print_menu(lst_phone_book: list) -> None:
    """Выводим меню и проверяем валидность ввода"""
    menu_item = ''
    while menu_item not in ['1', '2', '3', '4', '5', '6', '7']:
        view.menu()
        menu_item = view.input_from_user('Select a menu item: ')
        if menu_item in ['1', '2', '3', '4', '5', '6', '7']:
            sub_menu(menu_item, lst_phone_book)
            break
        else:
            view.output("Value error")
            continue


def sub_menu(menu_item, lst_phone_book):
    """Обрабатываем выбранный пункт меню"""
    match menu_item:
        case "1":
            save_phone_book(lst_phone_book)
            print_menu(lst_phone_book)
        case "2":
            show_contacts(lst_phone_book)
            print_menu(lst_phone_book)
        case "3":
            name, phone, comment = input_create_contact()
            create_contact(lst_phone_book, name, phone, comment)
            print_menu(lst_phone_book)
        case "4":
            value = input_find_contact()
            find_contact(lst_phone_book, value)
            print_menu(lst_phone_book)
        case "5":
            id_directory, name, phone, comment = input_edit_contact()
            edit_contact(lst_phone_book, id_directory, name, phone, comment)
            print_menu(lst_phone_book)
        case "6":
            id_directory = input_delete_contact()
            delete_contact(lst_phone_book, id_directory)
            print_menu(lst_phone_book)
        case "7":
            exit_phone_book(lst_phone_book)


def check_changes(lst_phone_book: list) -> bool:
    """Сравниваем измененный список объектов с первоначальным списком"""
    with model.FileManager("r") as file:
        json_reader = json.load(file)
        lst_phone_book_old = []
        find_changes = False
        if len(lst_phone_book) != len(lst_phone_book_old):
            find_changes = True
            return find_changes
        for item in json_reader:
            lst_phone_book_old.append(model.Directory.new_contact(item))
        for item in lst_phone_book:
            for item_old in lst_phone_book_old:
                if item.id_directory == item_old.id_directory:
                    if item != item_old:
                        find_changes = True
                        break
            if find_changes:
                break
    return find_changes


def save_phone_book(lst_phone_book: list) -> list:
    """Сохраняем изменения если они были"""
    view.output("Saving Phone Book")
    if check_changes(lst_phone_book):
        with model.FileManager("w") as file:
            json.dump([item.__dict__ for item in lst_phone_book], file, indent=4, ensure_ascii=False)
    else:
        view.output("Phone book not need save")
    return lst_phone_book


def show_contacts(lst_phone_book: list) -> None:
    """Выводим список контактов"""
    view.output("Showing all contacts")
    view.print_contact(lst_phone_book)


def input_create_contact() -> list:
    """Получение данных от пользователя"""
    view.output("Creating contact")
    name = view.input_from_user("Enter name: ")
    phone = view.input_from_user("Enter phone: ")
    comment = view.input_from_user("Enter comment: ")
    return [name, phone, comment]


def create_contact(lst_phone_book: list, name: str, phone: str, comment: str) -> dict | str:
    """Создание контакта"""
    next_id = model.Directory.max_id
    try:
        checking_for_empty_data(name, 'name')
        checking_for_empty_data(phone, 'phone')
        checking_for_empty_data(comment, 'comment')
    except model.EmptyData as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    try:
        phone = convert_to_digits(phone, 'phone')
    except model.CheckIsDigit as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    dct = {'id_directory': next_id,
           'name': name,
           'phone': phone,
           'comment': comment}
    lst_phone_book.append(model.Directory.new_contact(dct))
    view.print_contact(lst_phone_book)
    return vars(lst_phone_book[-1])


def input_find_contact() -> str:
    """Получение данных от пользователя"""
    view.output("Finding a contact")
    value = view.input_from_user("Enter id or name or phone or comment: ")
    return value


def find_contact(lst_phone_book: list, value: str) -> str:
    """Поиск в справочнике"""
    try:
        checking_for_empty_data(value, 'value')
    except model.EmptyData as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    try:
        value = convert_to_digits(value, 'id')
    except model.CheckIsDigit:
        pass
    for item in lst_phone_book:
        if item.find_contact(value):
            view.output(item.find_contact(value))
            return str(item.find_contact(value))
    view.output("Contact not found")
    return "Contact not found"


def input_edit_contact() -> list:
    """Получение данных от пользователя"""
    view.output("Editing contact")
    id_directory = view.input_from_user("Enter id edit contact: ")
    name = view.input_from_user("Enter name: ")
    phone = view.input_from_user("Enter phone: ")
    comment = view.input_from_user("Enter comment: ")
    return [id_directory, name, phone, comment]


def edit_contact(lst_phone_book: list, id_directory: str, name: str, phone: str, comment: str) -> dict | str:
    """Изменение контакта"""
    try:
        checking_for_empty_data(id_directory, 'id')
        checking_for_empty_data(name, 'name')
        checking_for_empty_data(phone, 'phone')
        checking_for_empty_data(comment, 'comment')
    except model.EmptyData as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    try:
        id_directory = convert_to_digits(id_directory, 'id')
        phone = convert_to_digits(phone, 'phone')
    except model.CheckIsDigit as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    for item in lst_phone_book:
        if item.id_directory == id_directory:
            item.set_contact(id_directory, name, phone, comment)
            view.print_contact(lst_phone_book)
            return vars(lst_phone_book[0])
    view.output("Contact not found")
    return "Contact not found"


def input_delete_contact() -> str:
    """Удаление контакта"""
    view.output("Deleting contact")
    id_directory = view.input_from_user("Enter id delete contact: ")
    return id_directory


def delete_contact(lst_phone_book: list, id_directory: str) -> str | None:
    try:
        checking_for_empty_data(id_directory, 'id')
    except model.EmptyData as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    try:
        id_directory = convert_to_digits(id_directory, 'id')
    except model.CheckIsDigit as error:
        view.output(f"Error: {error}")
        return f"Error: {error}"
    for num, item in enumerate(lst_phone_book, start=0):
        if item.id_directory == id_directory:
            lst_phone_book.pop(num)
            view.print_contact(lst_phone_book)
            return "Contact not found"
    view.output("Contact not found")
    return "Contact not found"


def exit_phone_book(lst_phone_book):
    """Проверка на изменение и выход из справочника"""
    view.output("Exiting Phone Book")
    if check_changes:
        view.output('Phone book not saved')
        exit_input = ''
        while exit_input not in ['y', 'n']:
            exit_input = view.input_from_user("Do you want to save phone book? (y/n)")
            if exit_input == 'y':
                with model.FileManager("w") as file:
                    json.dump([item.__dict__ for item in lst_phone_book], file, indent=4, ensure_ascii=False)
                break
            elif exit_input == 'n':
                break
            else:
                view.output('Invalid input')


def convert_to_digits(value, message):
    if value.isdigit():
        return int(value)
    else:
        raise model.CheckIsDigit(message)


def checking_for_empty_data(value, message):
    if value:
        return value
    else:
        raise model.EmptyData(message)
