import random
import string
import time

from faker import Faker
faker = Faker()

class DataGenerator:
    
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"
         
    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)


    @staticmethod
    def generate_random_page():
        """
        Генерация количества страницы
        Генерация номера страницы в пределах количества страниц
        """
        millis = int(time.time() * 1000)
        random.seed(millis)
        page_size = random.randint(1, 50)
        return random.randint(1, page_size), page_size

    @staticmethod
    def generate_random_min_max_price():
        """
        Генерация количества страницы
        Генерация номера страницы в пределах количества страниц
        """
        max_price = random.randint(1, 5000)
        return random.randint(1, max_price), max_price

    @staticmethod
    def generate_random_genre_id():
        """
        Генерация номера страницы
        """
        return random.randint(1, 10)
