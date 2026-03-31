# constants.py
BASE_URL_AUTH = "https://auth.dev-cinescope.coconutqa.ru"
BASE_URL_MOVIES = "https://api.dev-cinescope.coconutqa.ru"
BASE_URL_PAYMENT = "https://payment.dev-cinescope.coconutqa.ru"

# Креды SUPER_ADMIN
SUPER_ADMIN_EMAIL = "api1@gmail.com"
SUPER_ADMIN_PASSWORD = "asdqwe123Q"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
LOGOUT_ENDPOINT = "/logout"

MOVIE_ENDPOINT = "/movies"

PAYMENT_CREATE_ENDPOINT = "/create"