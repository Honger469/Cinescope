from constants import MOVIE_ENDPOINT, BASE_URL_MOVIES
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """
      Класс для работы с фильмами.
      """
    def __init__(self, session):
        super().__init__(session=session)

    def get_poster_movie(self, test_poster, expected_status=200):
        """
        Получение афиш фильмов.
        :param test_poster: Данные афиши.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=BASE_URL_MOVIES,
            endpoint=MOVIE_ENDPOINT,
            params=test_poster,
            expected_status=expected_status
        )

    def create_movie(self, movies_data, expected_status=201):
        """
        Создание нового фильма.
        :param movies_data: Данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=movies_data,
            expected_status=expected_status
        )