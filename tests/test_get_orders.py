import allure
import requests
from data import URL


@allure.feature("Получение списка заказов")
class TestGetOrders:

    @allure.title("Проверка, что список заказов возвращается")
    def test_get_orders_list(self):
        response = requests.get(f"{URL}/api/v1/orders")
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)