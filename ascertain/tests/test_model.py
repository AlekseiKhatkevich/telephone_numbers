import pytest
from psycopg2.extras import NumericRange
import os
from ascertain.models import TelephoneNumbersModel


@pytest.mark.django_db
class TestTelephoneNumbersModelPositive:
    """"
    Позитивные тесты модели 'TelephoneNumbersModel'
    """
    @staticmethod
    @pytest.fixture(scope='function')
    def data_for_model() -> dict:
        """
        Возвращает данные для позитивного создания экземпляра класса модели 'TelephoneNumbersModel'
        """
        data = dict(
            abc_or_def=228,
            numbers_range=NumericRange(666, 667, '[)'),
            volume=1,
            operator='ОГО "Спецсвязь"',
            region='г. ххххххххх-58 | ВЧ № 00000004',
        )

        return data

    def test_create_model_instance(self, data_for_model):
        """
        Тестирование возможности создания одного экземпляра модели "TelephoneNumbersModel"
        и записи его в БД при условии предоставления правильных входных аргументов.
        """
        TelephoneNumbersModel.objects.create(**data_for_model)

        assert TelephoneNumbersModel.objects.filter(**data_for_model).exists()
