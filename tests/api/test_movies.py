import pytest
from tests.api.api_manager import ApiManagerMovies
class TestMoviesAPI:
    def test_get_poster(self, api_manager_movies: ApiManagerMovies, test_poster):
        """
                Тест на получение афиши.
        """
        response = api_manager_movies.movies_api.get_poster_movie(test_poster)
        response_data = response.json()

        # Проверки
        # Проверяем, что ключ 'movies' есть
        assert "movies" in response_data, "Ключ 'movies' отсутствует в ответе"

        # Если хотим проверить хотя бы один фильм:
        if response_data["movies"]:
            assert "id" in response_data["movies"][0], "ID фильма отсутствует в ответе"
        else:
            print("Список фильмов пуст на этой странице")
        assert "pageCount" in response_data, "Ключ 'pageCount' отсутствует в ответе"
        assert "count" in response_data, "Ключ count отсутствует в ответе"
        assert "page" in response_data, "Ключ page отсутствуют в ответе"
        assert "pageSize" in response_data, "Ключ pageSize отсутствуют в ответе"


class TestMoviesAPINegative:
    @pytest.mark.parametrize("field, value", [
        ("pageSize", "21"),  # некорректное количество страниц
        ("page", 21),  # некорректный номер страницы
        ("minPrice", 10000)  # минимальная цена больше максимальной цены
    ])
    def test_get_poster_negative(self, api_manager_movies: ApiManagerMovies, test_poster, field, value):
        data = test_poster

        if value == "MISSING":
            data.pop(field, None)  # удаляем ключ из словаря
        else:
            data[field] = value  # изменяем или оставляем None

        print(f"\nНегативный тест. Проверка поля {field}={value}")

        expected_status = 400  # Важно! Ожидаемый статус-код
        api_manager_movies.movies_api.get_poster_movie(data, expected_status)
