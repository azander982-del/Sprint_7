import allure
import requests
from data import URL
from helpers import (
    register_new_courier_and_return_login_password,
    delete_courier_by_login_password,
    generate_random_string
)

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, created_courier):
        login, password, first_name = created_courier
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{URL}/api/v1/courier/login", json=payload)
        assert response.status_code == 200
        assert "id" in response.json(), "ID не возвращён"

    @allure.title("Логин с неверным паролем")
    def test_login_courier_wrong_password(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        requests.post(f"{URL}/api/v1/courier", json=payload)

        wrong_payload = {
            "login": login,
            "password": "wrong_password"
        }
        response = requests.post(f"{URL}/api/v1/courier/login", json=wrong_payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

        delete_courier_by_login_password(login, password)

    @allure.title("Логин с несуществующим логином")
    def test_login_courier_nonexistent_login(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier/login", json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Логин без обязательного поля логин")
    def test_login_courier_missing_login(self):
        payload = {
            "password": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier/login", json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Логин без обязательного поля пароль")
    def test_login_courier_missing_password(self):
        payload = {
            "login": generate_random_string(10)
        }
        response = requests.post(f"{URL}/api/v1/courier/login", json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"