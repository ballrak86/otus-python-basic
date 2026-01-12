import pytest
import model
import json
from random import randint


@pytest.fixture()
def lst_phone_book():
    """Фикстура с данными из файла"""
    with model.FileManager("r") as file:
        json_reader = json.load(file)
        lst_phone_book = []
        for item in json_reader:
            lst_phone_book.append(model.Directory.new_contact(item))
        yield lst_phone_book


@pytest.fixture()
def contact_in_file():
    """Фикстура с рандомным атрибутом и рандомными данными в нем"""
    with model.FileManager("r") as file:
        json_reader = json.load(file)
        lst_phone_book = []
        for item in json_reader:
            lst_phone_book.append(model.Directory.new_contact(item))
        list_id = randint(0, len(lst_phone_book) - 1)
        column = list(vars(lst_phone_book[0]).keys())
        column_var = column[randint(0, len(column) - 1)]
        search_box = str(getattr(lst_phone_book[list_id], column_var))
        found_contact = str(lst_phone_book[list_id])
        yield [search_box, found_contact]


@pytest.fixture()
def id_directory_in_file():
    """Фикстура с рандомным id в справочнике"""
    with model.FileManager("r") as file:
        json_reader = json.load(file)
        lst_id_directory = []
        for item in json_reader:
            lst_id_directory.append(item['id_directory'])
        list_id = randint(0, len(lst_id_directory) - 1)
        yield str(lst_id_directory[list_id])
