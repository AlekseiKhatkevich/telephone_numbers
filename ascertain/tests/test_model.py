import pytest

from ascertain.models import TelephoneNumbersModel


@pytest.mark.django_db
class TestTelephoneNumbersModelPositive:
    """"
    Позитивные тесты модели 'TelephoneNumbersModel'
    """
    def test_create_model_instance(self, data_for_model):
        """
        Тестирование возможности создания одного экземпляра модели "TelephoneNumbersModel"
        и записи его в БД при условии предоставления правильных входных аргументов.
        """
        TelephoneNumbersModel.objects.create(**data_for_model)

        assert TelephoneNumbersModel.objects.filter(**data_for_model).exists()

