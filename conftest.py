import random

from faker import Faker
import pytest
import requests
from constants import REGISTER_ENDPOINT, BASE_URL_AUTH, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from custom_requester.custom_requester import CustomRequester
from tests.api.api_manager import ApiManagerAuth, ApiManagerMovies
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager_auth(session):
    """
    Фикстура для создания экземпляра ApiManagerAuth.
    """
    return ApiManagerAuth(session)

@pytest.fixture(scope="session")
def api_manager_movies(session):
    """
    Фикстура для создания экземпляра ApiManagerAuth.
    """
    return ApiManagerMovies(session)

@pytest.fixture()
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture()
def admin_api(api_manager_auth):
    """
    Аутентификация под админом для получения нужных прав, если они нужны для теста
    """
    admin_email = SUPER_ADMIN_EMAIL
    admin_password = SUPER_ADMIN_PASSWORD

    api_manager_auth.auth_api.authenticate(admin_email, admin_password)
    return api_manager_auth

@pytest.fixture()
def test_poster():
    """
    Генерация случайных параметров для просмотра афиши.
    """
    random_max_price = random.randint(400, 500)
    return {
        "pageSize": random.randint(1, 20),
        "page": random.randint(1, 5),
        "minPrice": random.randint(1, random_max_price-1),
        "maxPrice": random_max_price,
        "locations": "MSK",
        "published": True,
        "genreId": random.randint(1, 5)
    }

@pytest.fixture()
def test_movie():
    """
    Генерация случайных параметров для создания фильма.
    """
    fake = Faker("ru_RU")
    return {
        "name":  fake.sentence(nb_words=3),
        "imageUrl": f"https://{fake.domain_name()}/image/{fake.uuid4()}",
        "price": random.randint(100, 400),
        "description": fake.sentence(nb_words=10),
        "location": "SPB",
        "published": True,
        "genreId": random.randint(1, 5)
    }

@pytest.fixture()
def authorized_user(api_manager_auth, registered_user):
    api_manager_auth.auth_api.authenticate(
        registered_user["email"],
        registered_user["password"]
    )
    return registered_user

@pytest.fixture()
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        base_url=BASE_URL_AUTH,
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session)
