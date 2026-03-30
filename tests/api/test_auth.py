import pytest
import requests
from constants import BASE_URL_AUTH, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
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

    def test_login_user(self, api_manager_auth: ApiManagerAuth, registered_user):
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


class TestAuthNegative:
    @pytest.mark.parametrize("field_register, value_register", [
        ("email", "abc"),  # некорректный email
        ("fullName", ""),  # пустая строка
        ("password", None),  # ключ есть, но значение None
    ])

    def test_negative_register(self, api_manager_auth: ApiManagerAuth, test_user, field_register, value_register):
        data = test_user

        if value_register == "MISSING":
            data.pop(field_register, None)  # удаляем ключ из словаря
        else:
            data[field_register] = value_register  # изменяем или оставляем None

        print(f"\nНегативный тест. Проверка поля {field_register}={value_register}")

        expected_status = 400   # Важно! Ожидаемый статус-код
        api_manager_auth.auth_api.register_user(data, expected_status)

    @pytest.mark.parametrize("field_auth, value_auth", [
        ("email", "abc"),  # некорректный email
        ("email", ""),  # пустая строка
        ("password", "1"),  # неверный пароль
        ("password", ""),  # пустая строка
    ])

    def test_negative_auth(self, api_manager_auth: ApiManagerAuth, registered_user, field_auth, value_auth):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        if value_auth == "MISSING":
            login_data.pop(field_auth, None)  # удаляем ключ из словаря
        else:
            login_data[field_auth] = value_auth  # изменяем или оставляем None

        print(f"\nНегативный тест. Проверка поля {field_auth}={value_auth}")

        expected_status = 401   # Важно! Ожидаемый статус-код
        api_manager_auth.auth_api.login_user(login_data, expected_status)

