import allure
import pytest
import requests
from data import URL, order_data


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = order_data.copy()
        payload["color"] = color
        response = requests.post(f"{URL}/api/v1/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()