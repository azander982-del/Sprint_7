import allure
import requests
from data import URL
from helpers import (
    register_new_courier_and_return_login_password,
    delete_courier_by_login_password,
    generate_random_string
)


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3, "Курьер не создался"
        login, password, first_name = login_pass
        delete_courier_by_login_password(login, password)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response_first = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response_first.status_code == 201

        response_second = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response_second.status_code == 409
        assert response_second.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        delete_courier_by_login_password(login, password)

    @allure.title("Создание курьера без обязательного поля логин")
    def test_create_courier_missing_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Создание курьера без обязательного поля пароль")
    def test_create_courier_missing_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Создание курьера без обязательного поля имя")
    def test_create_courier_missing_first_name(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response.status_code == 201

    @allure.title("Создание курьера с уже существующим логином возвращает ошибку")
    def test_create_courier_existing_login_fails(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response_first = requests.post(f"{URL}/api/v1/courier", json=payload)
        assert response_first.status_code == 201

        payload2 = {
            "login": login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response_second = requests.post(f"{URL}/api/v1/courier", json=payload2)
        assert response_second.status_code == 409
        assert response_second.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        delete_courier_by_login_password(login, password)