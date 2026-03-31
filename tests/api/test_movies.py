import pytest
from tests.api.api_manager import ApiManagerMovies
from faker import Faker
fake = Faker("ru_RU")

class TestMoviesAPI:

    def test_create_get_delete_movie(self, admin_api, test_movie, api_manager_movies):
        """
                Позитивный тест на создание, получение, удаление фильма.
        """
        print("\nПозитивный тест. Создание, получение, удаление фильма")
        data = test_movie
        response = api_manager_movies.movies_api.create_movie(data)
        response_created = response.json()

        # Проверки
        assert "id" in response_created, "Ключ отсутствует в ответе"
        assert "name" in response_created, "Ключ отсутствует в ответе"
        assert "price" in response_created, "Ключ отсутствуют в ответе"
        assert "description" in response_created, "Ключ отсутствуют в ответе"

        """
                Позитивный тест на получение фильма.
        """
        response = api_manager_movies.movies_api.get_movie(response_created["id"])
        response_got = response.json()

        # Проверки
        assert "id" in response_got, "Ключ отсутствует в ответе"
        assert "name" in response_got, "Ключ отсутствует в ответе"
        assert "price" in response_got, "Ключ отсутствуют в ответе"
        assert "description" in response_got, "Ключ отсутствуют в ответе"

        """
                        Позитивный тест на редактирование фильма.
        """
        data["name"] = fake.sentence(nb_words=3)
        data["description"] = fake.sentence(nb_words=8)
        response = api_manager_movies.movies_api.change_movie(response_created["id"], data)
        response_changed = response.json()

        # Проверки
        assert "id" in response_changed, "Ключ отсутствует в ответе"
        assert "price" in response_changed, "Ключ отсутствуют в ответе"
        assert response_changed["name"] == data["name"], "Название не изменилось"
        assert response_changed["description"] == data["description"], "Описание не изменилось"

        """
                Позитивный тест на удаление фильма.
        """
        api_manager_movies.movies_api.delete_movie(response_created["id"])

        # Проверки
        api_manager_movies.movies_api.get_movie(response_created["id"], 404)

    @pytest.mark.parametrize("field_get, value_get", [
        ("Default", True),  #  Не отправляем ничего
        ("page", "MISSING"),  # Не отправляем page
        ("pageSize", 1),  # Граничное значение
        ("minPrice", 1),  # Граничное значение
        ("maxPrice", 2),  # Граничное значение
        ("genreId", 1)  # Граничное значение
    ])
    def test_get_poster(self, api_manager_movies: ApiManagerMovies, test_poster, field_get, value_get):
        """
                Позитивные тесты на получение афиши.
        """
        print(f"\nПозитивный тест. Получение афиши. Проверка поля {field_get}={value_get}")
        if field_get == "Default":  # Сервер подставит значения по умолчанию
            data = {}
        else:
            data = test_poster
            if value_get == "MISSING":  #  Не отправляем этот ключ
                data.pop(field_get, None)  # удаляем ключ из словаря
            else:
                data[field_get] = value_get  # изменяем или оставляем None
            if data["minPrice"] > data["maxPrice"]: #   в позитивном тесте должно быть minPrice < maxPrice
                data["minPrice"] = data["maxPrice"] - 1
        response = api_manager_movies.movies_api.get_poster_movie(data)
        response_data = response.json()

        # Проверки
        # Проверяем, что ключ 'movies' есть
        assert "movies" in response_data, "Ключ 'movies' отсутствует в ответе"

        # Сначала делаем logout
        api_manager_movies.auth_api.logout()  # выход из аккаунта

        # Если хотим проверить хотя бы один фильм:
        if response_data["movies"]:
            assert "id" in response_data["movies"][0], "ID фильма отсутствует в ответе"
        else:
            print("Список фильмов пуст на этой странице")
        assert "pageCount" in response_data, "Ключ 'pageCount' отсутствует в ответе"
        assert "count" in response_data, "Ключ count отсутствует в ответе"
        assert "page" in response_data, "Ключ page отсутствуют в ответе"
        assert "pageSize" in response_data, "Ключ pageSize отсутствуют в ответе"

"""
                     Негативные тесты:
"""
class TestMoviesAPINegative:
    @pytest.mark.parametrize("field_create_negative, value_create_negative", [
        ("not_access", True),  # Без нужных прав
        ("name", ""),  # Пустое название
        ("name", "MISSING")  # Не отправляется название
    ])
    def test_create_movie(self, admin_api, test_movie, api_manager_movies, field_create_negative, value_create_negative):
        """
                Негативные тесты на создание фильма.
        """
        print(f"\nНегативный тест. Проверка поля {field_create_negative}={value_create_negative}")

        data = test_movie
        if value_create_negative == "MISSING":
            data.pop(field_create_negative, None)  # удаляем ключ из словаря
        else:
            data[field_create_negative] = value_create_negative  # изменяем или оставляем None


        expected_status = 400  # Ожидаемый статус-код

        if field_create_negative == "not_access":
            api_manager_movies.auth_api.logout()  # Выход из аккаунта
            expected_status = 401  # Ожидаемый статус-код

        response = api_manager_movies.movies_api.create_movie(data, expected_status)
        pass

    @pytest.mark.parametrize("field_negative, value_negative", [
        ("page", 0),  # Невалидные граничные значения
        ("pageSize", 0),   # Невалидные граничные значения
        ("pageSize", 21),  # Невалидные граничные значения
        ("minPrice", 0),  #  Невалидные граничные значения
        ("maxPrice", 1),  # Невалидные граничные значения
        ("minPrice", 10000),  #  minPrice > maxPrice
        ("page", "abc"),  #  Невалидные значения
        ("pageSize", "abc"),  #  Невалидные значения
        ("minPrice", "abc"),  #  Невалидные значения
        ("maxPrice", "abc"),  #  Невалидные значения
        ("genreId", "abc")  #  Невалидные значения
    ])
    def test_get_poster_negative(self, api_manager_movies: ApiManagerMovies, test_poster,
                                 field_negative, value_negative):
        """
                Негативные тесты на получение афиши.
        """

        print(f"\nНегативный тест. Проверка поля {field_negative}={value_negative}")

        data = test_poster

        if value_negative == "MISSING":
            data.pop(field_negative, None)  # удаляем ключ из словаря
        else:
            data[field_negative] = value_negative  # изменяем или оставляем None

        expected_status = 400   # Ожидаемый статус-код
        api_manager_movies.movies_api.get_poster_movie(data, expected_status)

