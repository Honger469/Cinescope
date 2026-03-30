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