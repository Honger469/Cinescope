import pytest
import requests

from conftest import test_user
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:
    def test_reg_auth_user(self, test_user):

        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.post(register_url, json=test_user, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # Проверки
        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_reg = response.json()
        assert response_reg["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_reg, "ID пользователя отсутствует в ответе"
        assert "roles" in response_reg, "Роли пользователя отсутствуют в ответе"

        # Проверяем, что роль USER назначена по умолчанию
        assert "USER" in response_reg["roles"], "Роль USER должна быть у пользователя"

        # URL для авторизации
        auth_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

        data_auth = {
            "email": response_reg["email"],
            "password": test_user["password"]
        }
        # Отправка запроса на авторизацию
        response_auth = requests.post(auth_url, json=data_auth, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {response_auth.status_code}")
        print(f"Response body: {response_auth.text}")

        # Проверки
        response_auth_json = response_auth.json()
        assert response_auth.status_code in (200, 201), "Ошибка авторизации пользователя"
        assert response_auth_json.get("accessToken"), "Токен не возвращён"
        # assert response_auth_json.get("email") is not None, "Email не возвращён после авторизации"
        # assert response_auth_json.get("email") == response_reg["email"], "Email не совпадает"


    class TestAuthAPINegative:
        @pytest.mark.parametrize("field,value", [
            ("email", "abc123321"),  # несуществующий эмейл
            ("password", "abc123321"),  # неверный пароль
            ("password", "MISSING")  # не передан эмейл
        ])

        def test_reg_auth_user_negative(self, test_user, field, value):
            # URL для авторизации
            auth_url = f"{BASE_URL}{LOGIN_ENDPOINT}"

            data_auth = {
                "email": test_user["email"],
                "password": test_user["password"]
            }

            if value == "MISSING":
                data_auth.pop(field, None)  # удаляем ключ из словаря
            else:
                data_auth[field] = value  # изменяем или оставляем None

            # Отправка запроса на авторизацию
            response_auth = requests.post(auth_url, json=data_auth, headers=HEADERS)

            # Логируем ответ для диагностики
            print(f"Response status: {response_auth.status_code}")
            print(f"Response body: {response_auth.text}")

            # Проверки
            print(f"Проверка поля {field}={value}: статус {response_auth.status_code}")

            message = response_auth.json().get("message")
            assert message, "Поле 'message' отсутствует или пустое в ответе"
            assert response_auth.status_code in (400, 401, 500)