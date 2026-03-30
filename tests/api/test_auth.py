import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from tests.api.api_manager import ApiManagerAuth

class TestAuthAPI:
    def test_register_user(self, api_manager_auth: ApiManagerAuth, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager_auth.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager_auth: ApiManagerAuth, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager_auth.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

class TestBookingsNegative:
    json = {"username": "admin", "password": "password123"}

    @pytest.mark.parametrize("field,value", [
        ("email", "abc"),  # некорректный email
        ("firstname", ""),  # пустая строка
        ("fullName", ""),  # пустая строка
        ("password", None),  # ключ есть, но значение None
    ])
    def test_negative(self, api_manager_auth: ApiManagerAuth, test_user, field, value):
        data = test_user

        if value == "MISSING":
            data.pop(field, None)  # удаляем ключ из словаря
        else:
            data[field] = value  # изменяем или оставляем None

        expected_status = 400   # Важно! Ожидаемый статус-код
        response = api_manager_auth.auth_api.register_user(test_user, expected_status)

        print(f"\nНегативный тест. Проверка поля {field}={value}")
