import os
from dotenv import load_dotenv
import random
from faker import Faker
import pytest
import requests
from constants import REGISTER_ENDPOINT, BASE_URL_AUTH, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from custom_requester.custom_requester import CustomRequester
from tests.api.api_manager import ApiManagerAuth, ApiManagerMovies, ApiManagerPayment
from utils.data_generator import DataGenerator


faker = Faker()

# Загружаем логин пароль Администратора из .env
load_dotenv()

# ----------------------------
# Сессия и HTTP-клиенты
# ----------------------------

@pytest.fixture(scope="session")
def session():
    """Фикстура для создания HTTP-сессии."""
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def requester():
    """Фикстура для создания экземпляра CustomRequester."""
    session_obj = requests.Session()
    return CustomRequester(session=session_obj)


@pytest.fixture(scope="session")
def api_manager_auth(session):
    """Фикстура для создания экземпляра ApiManagerAuth."""
    return ApiManagerAuth(session)


@pytest.fixture(scope="session")
def api_manager_movies(session):
    """Фикстура для создания экземпляра ApiManagerMovies."""
    return ApiManagerMovies(session)


@pytest.fixture(scope="session")
def api_manager_payment(session):
    """Фикстура для создания экземпляра ApiManagerPayment."""
    return ApiManagerPayment(session)


# ----------------------------
# Данные для тестов
# ----------------------------

@pytest.fixture()
def test_user():
    """Генерация случайного пользователя для тестов."""
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture()
def test_movie():
    """Генерация случайных параметров для создания фильма."""
    fake_local = Faker("ru_RU")
    return {
        "name": fake_local.sentence(nb_words=3),
        "imageUrl": f"https://{fake_local.domain_name()}/image/{fake_local.uuid4()}",
        "price": random.randint(100, 400),
        "description": fake_local.sentence(nb_words=10),
        "location": "SPB",
        "published": True,
        "genreId": random.randint(1, 5)
    }


@pytest.fixture()
def test_poster():
    """Генерация случайных параметров для просмотра афиши."""
    max_price = random.randint(400, 500)
    return {
        "pageSize": random.randint(1, 20),
        "page": random.randint(1, 5),
        "minPrice": random.randint(1, max_price - 1),
        "maxPrice": max_price,
        "locations": "MSK",
        "published": True,
        "genreId": random.randint(1, 5)
    }


# ----------------------------
# Аутентификация
# ----------------------------

@pytest.fixture()
def admin_api(api_manager_auth):
    """Аутентификация под админом для тестов с правами администратора."""
    api_manager_auth.auth_api.authenticate(os.getenv("SUPER_ADMIN_EMAIL"), os.getenv("SUPER_ADMIN_PASSWORD"))
    return api_manager_auth


@pytest.fixture()
def authorized_user(api_manager_auth, registered_user):
    """Аутентификация зарегистрированного пользователя."""
    api_manager_auth.auth_api.authenticate(
        registered_user["email"],
        registered_user["password"]
    )
    return registered_user


# ----------------------------
# Регистрация пользователя
# ----------------------------

@pytest.fixture()
def registered_user(requester, test_user):
    """Фикстура для регистрации и получения данных зарегистрированного пользователя."""
    response = requester.send_request(
        method="POST",
        base_url=BASE_URL_AUTH,
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered = test_user.copy()
    registered["id"] = response_data["id"]
    return registered