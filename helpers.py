import allure
import requests
import random
import string
from data import URL

@allure.step("Генерация случайной строки длиной {length}")
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

@allure.step("Регистрация нового курьера и возврат его логина, пароля и имени")
def register_new_courier_and_return_login_password():
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{URL}/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass

@allure.step("Удаление курьера по логину {login} и паролю")
def delete_courier_by_login_password(login, password):
    login_resp = requests.post(f'{URL}/api/v1/courier/login', json={
        "login": login,
        "password": password
    })
    courier_id = login_resp.json().get("id")
    if courier_id:
        requests.delete(f'{URL}/api/v1/courier/{courier_id}') 

@allure.step("Удаление курьера по id {courier_id}")
def delete_courier_by_id(courier_id):
    requests.delete(f'{URL}/api/v1/courier/{courier_id}')