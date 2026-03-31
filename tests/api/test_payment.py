import pytest
from tests.api.api_manager import ApiManagerPayment

class TestPaymentAPI:

    def test_get_user_payment(self, admin_api, api_manager_payment:ApiManagerPayment):
        """
                Позитивный тест на создание, получение платежей пользователя.
        """
        print("\nПозитивный тест. Создание, получение, удаление фильма")
        user_id = "0bfbe544-2f80-472f-af9b-b7986490a3d7"
        response = api_manager_payment.payment_api.get_user_id_payment(user_id)
        response_data = response.json()

        # Проверки
        if response_data:
            assert "id" in response_data[0]
            assert "userId" in response_data[0]
            assert "movieId" in response_data[0]
            assert "status" in response_data[0]
            assert "amount" in response_data[0]
            assert "total" in response_data[0]
            assert "createdAt" in response_data[0]
        else:
            print("Оплат не найдено")

