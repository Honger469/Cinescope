import requests
import pytest
from constants import BASE_URL, HEADERS
class TestBookings:
    json = {"username": "admin", "password": "password123"}

    def test_booking(self, auth_session, booking_data_factory):
        """Проверка полного жизненного цикла бронирования: создание, изменение, получение, удаление."""
        # Создаём бронирование
        data = booking_data_factory()
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == data["totalprice"], "Заданная стоим-ть не с-ет"

        # PUT бронирования
        print("\nПробуем put")
        data = booking_data_factory(lastname="puted Gosling")
        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=data)
        assert put_booking.json()["lastname"] == data["lastname"], "Фамилия не обновилась"

        # Patch бронирования
        print("\nПробуем patch")
        data = booking_data_factory(firstname="patched Ryan", additionalneeds="patched Pianop")
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=data)
        assert patch_booking.status_code == 200, "Ошибка при создании брони"
        assert patch_booking.json()["firstname"] == data["firstname"], "Заданное имя не совпадает"
        assert (
            patch_booking.json()["additionalneeds"] == data["additionalneeds"]
        ), "Заданное имя не совпадает"
        assert patch_booking.json()["lastname"] == data["lastname"], "Заданная фамилия не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

class TestBookingsNegative:
    json = {"username": "admin", "password": "password123"}
    @pytest.mark.parametrize("field,value", [
        ("totalprice", "abc"),  # неправильный тип
        ("firstname", ""),  # пустая строка
        ("lastname", ""),  # пустая строка
        ("totalprice", None),  # ключ есть, но значение None
        ("firstname", None),  # ключ есть, но значение None
        ("lastname", None),  # ключ есть, но значение None
        ("totalprice", "MISSING"),  # ключ удален
        ("firstname", "MISSING")   # ключ удален
    ])
    def test_negative(self, auth_session, booking_data_factory, field, value):
        data = booking_data_factory()

        if value == "MISSING":
            data.pop(field, None)  # удаляем ключ из словаря
        else:
            data[field] = value  # изменяем или оставляем None

        response = auth_session.post(f"{BASE_URL}/booking", json=data)
        print(f" StatusCode = {response.status_code}")
        print(f"Проверка поля {field}={value}: статус {response.status_code}")

        assert response.status_code == 400

    def test_negative_del(self, auth_session, booking_data_factory):
        data = booking_data_factory()
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=data)
        response = requests.delete(f"{BASE_URL}/booking/{create_booking.json().get('bookingid')}")
        get_booking = auth_session.get(f"{BASE_URL}/booking/{create_booking.json().get('bookingid')}")
        print(get_booking.json()["lastname"])
        print(f"\nПроверка удаления бронирования без прав. Статус {response.status_code}")

        assert response.status_code == 403

