import random

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from ascertain.models import TelephoneNumbersModel
from telephone_numbers import error_messages


@pytest.fixture(scope='function')
def correct_msisdn_data_in_db(db, data_for_model: dict) -> TelephoneNumbersModel:
    """
    Создает одну запись в Базе данных телефонных номеров.
    """
    return TelephoneNumbersModel.objects.create(**data_for_model)


@pytest.fixture(scope='function')
def correct_msisdn(correct_msisdn_data_in_db: TelephoneNumbersModel) -> int:
    """
    Генерация рандомоного номера в диапазоне номеров фикстуры "correct_msisdn_data_in_db".
    """
    ndc = correct_msisdn_data_in_db.abc_or_def
    sn = random.randrange(
        correct_msisdn_data_in_db.numbers_range.lower,
        correct_msisdn_data_in_db.numbers_range.upper,
    )

    return int(f'7{ndc}{sn}')


@pytest.mark.django_db
class TestOperatorEndpointPositive:
    """
    Позитивные тесты эндпойнта 'operator/<msisdn:msisdn>/ GET'.
    """
    def test_response(self, client, correct_msisdn_data_in_db, django_assert_num_queries, correct_msisdn):
        """
        Тестируем положительный респонс.
        """
        expected_response = {
            'number': correct_msisdn,
            'operator': correct_msisdn_data_in_db.operator,
            'region': correct_msisdn_data_in_db.region,
        }

        with django_assert_num_queries(1):
            response = client.get(
                reverse('operator', args=(correct_msisdn,)),
                data=None,
                content_type='application/json',
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response


@pytest.mark.django_db
class TestOperatorEndpointNegative:
    """
    Негативные тесты эндпойнта 'operator/<msisdn:msisdn>/ GET'.
    """
    DUMMY_CACHE = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    def test_404(self, client, settings):
        """
        Тестирование ситуации когда прислан правильный MSISDN, но данного телефонного номера нет
        в базе данных.
        """
        settings.CACHES = self.DUMMY_CACHE
        number_not_in_db = 71111111111

        response = client.get(
            reverse('operator', args=(number_not_in_db,)),
            data=None,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == error_messages.NUMBER_NOT_FOUND.message

    def test_multiple_objects_returned(self, client, correct_msisdn_data_in_db, correct_msisdn, settings):
        """
        Тестируем ситуацию когда в базе есть 2 или более записей в диапазонах которых
        находится данный телефонный номер.
        """
        settings.CACHES = self.DUMMY_CACHE
        # Дублируем существующую запись.
        correct_msisdn_data_in_db.pk += 1
        correct_msisdn_data_in_db.save()

        response = client.get(
            reverse('operator', args=(correct_msisdn,)),
            data=None,
            content_type='application/json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == error_messages.MULTIPLE_NUMBERS.message


