from pathlib import Path

import pytest
from django.db.models import Min

from ascertain.handle_csv import DatabaseCSVUpload
from ascertain.models import TelephoneNumbersModel
from telephone_numbers import error_messages
from telephone_numbers.custom_exceptions import EmptyFolder


@pytest.mark.django_db
def test_path():
    """
    Тест класса "DatabaseCSVUpload". При вызове должен считать все CSV файлы в заданной папке и
    записать данные из них в таблицу.
    """
    path = Path(r'ascertain\tests\csv')
    handler = DatabaseCSVUpload(path, delimiter=',')
    handler()

    assert TelephoneNumbersModel.objects.all().count() == 9
    #  проверяем сбросился ли счетчик рк.
    assert TelephoneNumbersModel.objects.aggregate(pk__min=Min('pk'))['pk__min'] == 1


@pytest.mark.django_db
def test_get_csv_files_empty_folder(tmp_path):
    """
    Тестируем будет ли вызвано исключение "EmptyFolder" в случае попытки чтения CSV
    файлов из паки где их нет.
    """
    with pytest.raises(EmptyFolder, match=error_messages.EMPTY_FOLDER.message):
        handler = DatabaseCSVUpload(tmp_path, delimiter=',')
        handler()


@pytest.mark.django_db
def test_cant_write_to_db():
    """
    Тестируем будут ли сохранены старые данные в базе данных при неудачной попытке записать новые.
    """
    path = Path(r'ascertain\tests\csv')
    #  Записываем корректные данные в БД.
    handler_correct = DatabaseCSVUpload(path, delimiter=',')
    handler_correct()
    original = list(TelephoneNumbersModel.objects.all().values())

    # А теперь данные которые вызовут IntegrityError.
    path = Path(r'ascertain\tests\wrong_csv')
    handler_incorrect = DatabaseCSVUpload(path, delimiter=',')
    handler_incorrect()
    restored = list(TelephoneNumbersModel.objects.all().values())

    assert original == restored
