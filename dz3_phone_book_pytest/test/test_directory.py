import pytest
import controller
import model


@pytest.mark.parametrize('name, phone, comment', [('alex', '89292145235', 'test'),
                                                  ('vasya', '9232145235', 'pony'),
                                                  ('toma', '9292141235', 'clock')])
def test_add_contact(lst_phone_book, name, phone, comment):
    """Проверка создания контакта"""
    next_id = model.Directory.max_id
    assert controller.create_contact(lst_phone_book, name=name, phone=phone, comment=comment) == {'name': name,
                                                                                                  'phone': int(phone),
                                                                                                  'comment': comment,
                                                                                                  'id_directory': next_id}


@pytest.mark.parametrize('name, phone, comment, attr_empty_data',
                         [('alex', '89292145235', '', 'comment'),
                          ('vasya', '', 'pony', 'phone'),
                          ('', '9292141235', 'clock', 'name')])
def test_add_contact_empty_data(lst_phone_book, name, phone, comment, attr_empty_data):
    """Проверка создания контакта с пустыми данными"""
    assert controller.create_contact(lst_phone_book, name=name, phone=phone,
                                     comment=comment) == f'Error: {attr_empty_data} cannot be empty'


@pytest.mark.parametrize('name, phone, comment', [('alex', 'd89292145235', 'test'), ('vasya', '+9232145235', 'pony')])
def test_add_contact_check_digit(lst_phone_book, name, phone, comment):
    """Проверка создания контакта с символами и буквами в номере телефона"""
    assert controller.create_contact(lst_phone_book, name=name, phone=phone,
                                     comment=comment) == f'Error: phone is not a digit'


def test_find_contact(lst_phone_book, contact_in_file):
    """Проверка поиска контакта"""
    search_box, found_contact = contact_in_file
    assert controller.find_contact(lst_phone_book, search_box) == found_contact


def test_find_contact_empty_data(lst_phone_book):
    """Проверка поиска контакта с пустыми данными"""
    assert controller.find_contact(lst_phone_book, '') == f'Error: value cannot be empty'


def test_find_contact_not_exist(lst_phone_book):
    """Проверка поиска несуществующего контакта"""
    not_exist_id = str(model.Directory.max_id + 1)
    assert controller.find_contact(lst_phone_book, not_exist_id) == "Contact not found"


@pytest.mark.parametrize('name, phone, comment', [('alex', '89292145235', 'test'),
                                                  ('vasya', '9232145235', 'pony'),
                                                  ('toma', '9292141235', 'clock')])
def test_edit_contact(lst_phone_book, name, phone, comment):
    """Проверка изменения контакта"""
    id_directory = 1
    assert controller.edit_contact(lst_phone_book, name=name, phone=phone, comment=comment,
                                   id_directory=str(id_directory)) == {'name': name, 'phone': int(phone),
                                                                       'comment': comment, 'id_directory': id_directory}


@pytest.mark.parametrize('name, phone, comment, attr_empty_data',
                         [('alex', '89292145235', '', 'comment'),
                          ('vasya', '', 'pony', 'phone'),
                          ('', '9292141235', 'clock', 'name')])
def test_edit_contact_empty_data(lst_phone_book, name, phone, comment, attr_empty_data):
    """Проверка изменения контакта с пустыми данными"""
    id_directory = 1
    assert controller.edit_contact(lst_phone_book, name=name, phone=phone, comment=comment,
                                   id_directory=str(id_directory)) == f'Error: {attr_empty_data} cannot be empty'


@pytest.mark.parametrize('name, phone, comment', [('alex', 'd89292145235', 'test'), ('vasya', '+9232145235', 'pony')])
def test_edit_contact_check_digit(lst_phone_book, name, phone, comment):
    """Проверка изменения контакта с символами и буквами в номере телефона"""
    id_directory = 1
    assert controller.edit_contact(lst_phone_book, name=name, phone=phone, comment=comment,
                                   id_directory=str(id_directory)) == f'Error: phone is not a digit'


def test_edit_contact_not_exist(lst_phone_book):
    """Проверка изменения несуществующего контакта"""
    not_exist_id = str(model.Directory.max_id + 1)
    assert controller.edit_contact(lst_phone_book, name='test', phone='456546', comment='test',
                                   id_directory=not_exist_id) == "Contact not found"


def test_delete_contact(lst_phone_book, id_directory_in_file):
    """Проверка удаления контакта"""
    assert controller.delete_contact(lst_phone_book, id_directory_in_file) == controller.find_contact(lst_phone_book,
                                                                                                      id_directory_in_file)


def test_delete_contact_empty_data(lst_phone_book):
    """Проверка удаления контакта с пустыми данным"""
    assert controller.delete_contact(lst_phone_book, '') == f'Error: id cannot be empty'


def test_delete_contact_check_digit(lst_phone_book):
    """Проверка удаления контакта с символами и буквами в номере телефона"""
    assert controller.delete_contact(lst_phone_book, 'not_digit') == f'Error: id is not a digit'


def test_delete_contact_not_exist(lst_phone_book):
    """Проверка удаления несуществующего контакта"""
    not_exist_id = str(model.Directory.max_id + 1)
    assert controller.find_contact(lst_phone_book, not_exist_id) == "Contact not found"


def test_open_file(lst_phone_book):
    """Проверка открытия файла"""
    assert controller.open_file('1') == lst_phone_book


def test_save_phone_book(lst_phone_book):
    """Проверка открытия сохранения файла"""
    next_id = model.Directory.max_id
    controller.create_contact(lst_phone_book, name='test', phone='8904175456', comment='test')
    print(lst_phone_book)
    assert controller.save_phone_book(lst_phone_book) == controller.open_file('1')
    controller.delete_contact(lst_phone_book, str(next_id))
    assert controller.save_phone_book(lst_phone_book) == controller.open_file('1')


if __name__ == '__main__':
    pytest.main(['-vv'])
