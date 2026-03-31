import pytest
from tests.api.api_manager import ApiManagerMovies
class TestMoviesAPI:
    @pytest.mark.parametrize("field, value", [
        ("Default", True),  #  Не отправляем ничего
        ("page", "MISSING"),  # Не отправляем page
        ("pageSize", 1),  # Граничное значение
        ("minPrice", 1),  # Граничное значение
        ("maxPrice", 2),  # Граничное значение
        ("genreId", 1)  # Граничное значение
    ])
    def test_get_poster(self, api_manager_movies: ApiManagerMovies, test_poster, field, value):
        """
                Позитивные тесты на получение афиши.
        """
        print(f"\nПозитивный тест. Проверка поля {field}={value}")
        if field == "Default":  # Сервер подставит значения по умолчанию
            data = {}
        else:
            data = test_poster
            if value == "MISSING":  #  Не отправляем этот ключ
                data.pop(field, None)  # удаляем ключ из словаря
            else:
                data[field] = value  # изменяем или оставляем None
            if data["minPrice"] > data["maxPrice"]: #   в позитивном тесте должно быть minPrice < maxPrice
                data["minPrice"] = data["maxPrice"]-1
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
                                 field_negative, value_negative, expected_status = 400):
        """
                Негативные тесты на получение афиши.
        """

        print(f"\nНегативный тест. Проверка поля {field_negative}={value_negative}")

        data = test_poster

        if value_negative == "MISSING":
            data.pop(field_negative, None)  # удаляем ключ из словаря
        else:
            data[field_negative] = value_negative  # изменяем или оставляем None

        api_manager_movies.movies_api.get_poster_movie(data, expected_status)
