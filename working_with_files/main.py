import csv

phone_book_file = 'phone_book.csv'
need_save = False

def menu():
    print("""Welcome to Phone Book
        1. Save Phone Book
        2. Show all contacts
        3. Create a contact
        4. Find a contact
        5. Edit a contact
        6. Delete a contact
        7. Exit
    """)
    while True:
        menu_item = input('Select a menu item:')
        if menu_item in ['1', '2', '3', '4', '5', '6', '7']:
            sub_menu(menu_item)
            break
        else:
            print('Invalid input')

def sub_menu(menu_item):
    match menu_item:
        case "1":
            save_phone_book()
            menu()
        case "2":
            show_contacts()
            menu()
        case "3":
            create_contact()
            menu()
        case "4":
            find_contact()
            menu()
        case "5":
            edit_contact()
            menu()
        case "6":
            delete_contact()
            menu()
        case "7":
            exit_phone_book()

def save_phone_book():
    print("Saving Phone Book")
    global need_save
    if need_save:
        with open(phone_book_file, 'w', encoding='UTF-8') as file:
            csv_writer = csv.DictWriter(file, ['id', 'name', 'phone', 'comment'],lineterminator='\n')
            csv_writer.writeheader()
            csv_writer.writerows(lst_phone_book)
            need_save = False
    else:
        print('Phone book not need save')

def show_contacts():
    print("Showing all contacts")
    for item in lst_phone_book:
        print(item)

def create_contact():
    print("Creating contact")
    global need_save
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    comment = input("Enter comment: ")
    lst = []
    for item in lst_phone_book:
        lst.append(item['id'])
    id_num = int(max(lst)) + 1
    lst_phone_book.append({'id': str(id_num), 'name': name, 'phone': phone, 'comment': comment})
    need_save = True

def find_contact():
    print("Finding a contact")
    find_data = input("Enter id or name or phone or comment: ")
    check_found = 0
    for item in lst_phone_book:
        id_num, name, phone, comment = item.values()
        if find_data == id_num or find_data == name or find_data == phone or find_data == comment:
            print(item)
            check_found += 1
    if not check_found:
        print("Contact not found")

def edit_contact():
    print("Editing contact")
    global need_save
    id_edit_contact = input("Enter id edite contact: ")
    name = input("Enter new name: ")
    phone = input("Enter new phone: ")
    comment = input("Enter new comment: ")
    check_found = 0
    for num, item in enumerate(lst_phone_book, start=0):
        if item['id'] == id_edit_contact:
            lst_phone_book[num]['name'] = name
            lst_phone_book[num]['phone'] = phone
            lst_phone_book[num]['comment'] = comment
            check_found += 1
            need_save = True
    if not check_found:
        print("Contact not found")

def delete_contact():
    print("Deleting contact")
    global need_save
    id_del_contact = input("Enter id delete contact: ")
    check_found = 0
    for num, item in enumerate(lst_phone_book, start=0):
        if item['id'] == id_del_contact:
            lst_phone_book.pop(num)
            check_found += 1
            need_save = True
    if not check_found:
        print("Contact not found")

def exit_phone_book():
    print("Exiting Phone Book")
    if need_save:
        print('Phone book not saved')
        while True:
            exit_input = input("Do you want to save phone book? (y/n)")
            if exit_input == 'y':
                save_phone_book()
                break
            elif exit_input == 'n':
                break
            else:
                print('Invalid input')

print("""Welcome to Phone Book
    First please open phone book
    1. default phone_book.csv'
    2. Your file with the structure 'id', 'name', 'phone', 'comment'""")
while True:
    open_file_item = input('Select a menu item:')
    if open_file_item == '1':
        with open(phone_book_file, 'r', encoding='UTF-8') as file:
            csv_reader = csv.DictReader(file, ['id', 'name', 'phone', 'comment'])
            next(csv_reader)
            lst_phone_book = list(csv_reader)
        break
    elif open_file_item == '2':
        while True:
            phone_book_file = input('Write file name:')
            try:
                with open(phone_book_file, 'r', encoding='UTF-8') as file:
                    csv_reader = csv.DictReader(file, ['id', 'name', 'phone', 'comment'])
                    next(csv_reader)
                    lst_phone_book = list(csv_reader)
                    break
            except FileNotFoundError:
                print('Файл не найден.')
                continue
        break
    else:
        print('Invalid input')

menu()
