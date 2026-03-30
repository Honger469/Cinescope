from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT, BASE_URL_AUTH


class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session):
        super().__init__(session=session)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            base_url=BASE_URL_AUTH,
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            base_url=BASE_URL_AUTH,
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }

        response = self.login_user(login_data).json()

        if "accessToken" not in response:
            raise AssertionError("No accessToken in login response")

        token = response["accessToken"]
        self._update_session_headers(authorization=f"Bearer {token}")
        return token