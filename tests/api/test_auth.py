import pytest
from tests.api.api_manager import ApiManagerAuth


class TestAuthAPI:

    def test_register_and_login_user(self, api_manager_auth: ApiManagerAuth, registered_user):
        """
        Позитивный тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        # Сначала делаем logout
        api_manager_auth.auth_api.logout()

        response = api_manager_auth.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_change_user(self, admin_api, registered_user):
        """
        Позитивный тест на изменение пользователя.
        """
        user_id = registered_user["id"]
        new_verified = True
        new_banned = False
        new_data = {"verified": new_verified, "banned": new_banned}

        response = admin_api.user_api.change_user(user_id, new_data, expected_status=200)
        response_data = response.json()

        # Проверки
        assert response_data["verified"] is new_verified, "Статус верификации не изменился"
        assert response_data["banned"] is new_banned, "Статус banned не изменился"


# ----------------------------
# Негативные тесты
# ----------------------------


class TestAuthNegative:

    @pytest.mark.parametrize("field_register, value_register", [
        ("email", "abc"),  # некорректный email
        ("fullName", ""),  # пустая строка
        ("password", "MISSING"),  # ключ есть, но значение None
    ])

    def test_negative_register(self, api_manager_auth: ApiManagerAuth, test_user, field_register, value_register):
        """
            Негативные тесты на регистрацию.
        """

        # Сначала делаем logout
        api_manager_auth.auth_api.logout()  # выход из аккаунта

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
        """
            Негативные тесты на авторизацию.
        """

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        if value_auth == "MISSING":
            login_data.pop(field_auth, None)  # удаляем ключ из словаря
        else:
            login_data[field_auth] = value_auth  # изменяем или оставляем None

        print(f"\nНегативный тест. Проверка поля {field_auth}={value_auth}")

        expected_status = 401   # Ожидаемый статус-код

        # Сначала делаем logout
        api_manager_auth.auth_api.logout()  # выход из аккаунта

        api_manager_auth.auth_api.login_user(login_data, expected_status)

    def test_negative_change_user(self, api_manager_auth, authorized_user, registered_user):
        """
            Негативный тест на попытку изменения пользователя без соответствующих прав.
        """
        print(f"\nНегативный тест. Попытка изменения пользователя без соответствующих прав")
        user_id = registered_user["id"]
        new_data = {"verified": True, "banned": False}
        api_manager_auth.user_api.change_user(user_id, new_data, expected_status=403)

