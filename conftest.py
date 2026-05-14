import pytest
from helpers import register_new_courier_and_return_login_password, delete_courier_by_login_password

@pytest.fixture
def created_courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    yield login, password, first_name
    delete_courier_by_login_password(login, password)