import pytest
import requests
from constants import BASE_URL, HEADERS
import os
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('FTP_PROXY', None)
@pytest.fixture
def auth_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    auth_response = s.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"},
        verify=False                                         # <-- это только для тестов
    )
    token = auth_response.json().get("token")
    assert token, f"Ошибка автотестов: {auth_response.text}"
    s.headers.update({"Cookie": f"token={token}"})
    return s
@pytest.fixture
def booking_data_factory():
    def _booking_data(**kwargs):
        data = {
            "firstname": "John",
            "lastname": "Smith",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-10"
            },
            "additionalneeds": "Breakfast"
        }
        data.update(kwargs)
        return data
    return _booking_data