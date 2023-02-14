from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

#Homework 19.7.2
def test_simple_add_new_pet_with_valid_data(name='Вася', animal_type='кот', age='2'):
    """Проверяем, что можно добавить питомца с корректными данными упрощенно (без фото)"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_pet_foto(pet_photo='images/P1040103.jpg'):
    """Проверяем возможность обновления фотографии питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pets_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("There is no my pets")


#Негативные тесты:
def test_get_api_key_for_unvalid_user(email="123@mail.ru", password=valid_password):
    """ Проверяем, что запрос api ключа при указании ошибочного email возвращает статус 403 (как указано в требованиях Swagger) """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_unvalid_data(name="!!!", animal_type="!!!",
                                     age="!!!", pet_photo=""):
    """Проверяем, что в ответ на попытку добавть питомца с некорректно заполненными данными приложение возращает статус ответа 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] != name
#Поведение приложения в данном негативном тесте не соответсвует требованиям- БАГ


def test_add_new_pet_with_incorrect_key(name="Dan", animal_type="cat",
                                     age="5", pet_photo='images/P1040103.jpg'):
    """Проверяем, что в ответ на попытку добавть питомца с указанием некорректного ключа приложение возращает статус ответа 403"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = '123456789'

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] != name
#Поведение приложения в данном негативном тесте не соответсвует требованиям- БАГ

def test_get_all_pets_with_unvalid_filter(filter='123456'):
    """ Проверяем что запрос невалидного значения для фильтрации возвращает статус ответа 500 и фильтрация не осуществляется"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_get_all_pets_with_unvalid_key(filter='my_pets'):
    """ Проверяем что запрос "моих" питомцев при невалидном ключе возвращает ответ сервера 403"""

    auth_key = "12345"
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
#Поведение приложения в данном негативном тесте не соответсвует требованиям- БАГ


def test_delete_pet_with_unvalid_key():
    """Проверяем возможность удаления питомца при невалидном ключе (в соотсветсвии с требованиями ожидается статус ответс от  сервера 400)"""

    auth_key = "789456"
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Dan", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца

    assert status == 400
    assert pet_id in my_pets.values()

def test_add_pet_with_unvalid_age_simple(name="Nine", animal_type="cat",
                                     age="-5"):
    """Проверяем, что в ответ на попытку добавть питомца с отрицательным значением возраста, приложение возращает статус ответа 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert age not in result['age']
 #Поведение приложения в данном негативном тесте не соответсвует требованиям- БАГ

def test_add_pet_with_a_lot_of_letters_in_name(name= 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                                               animal_type='cat', age='2'):
 """Проверяем, что в ответ на попытку добавить питомца со слишком большим количеством символов в параметре Имя
 приложение возращает статус ответа 400 и не добавит питомца"""


    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] != name



