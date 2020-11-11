import tempfile
from pathlib import Path

from django.db.models import Min
from rest_framework.test import APITestCase

from ascertain.handle_csv import DatabaseCSVUpload
from ascertain.models import TelephoneNumbersModel
from telephone_numbers import error_messages
from telephone_numbers.custom_exceptions import EmptyFolder


class TestUploadCSVtoDatabasePositive(APITestCase):
    """
    Позитивный тест класса "DatabaseCSVUpload" отвечающего за загрузку данных из CSV файлов
    в базу данных.
    """
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.path = Path(r'ascertain\tests\csv')

    def test_class(self):
        """
        Тест класса "DatabaseCSVUpload". При вызове должен считать все CSV файлы в заданной папке и
        записать данные из них в таблицу.
        """
        handler = DatabaseCSVUpload(self.path, delimiter=',')
        handler()
        print(Path(__file__).parent.absolute())

        self.assertEqual(
            TelephoneNumbersModel.objects.all().count(),
            9,
        )
        #  проверяем сбросился ли счетчик рк.
        self.assertEqual(
            TelephoneNumbersModel.objects.aggregate(pk__min=Min('pk'))['pk__min'],
            1,
        )


class TestUploadCSVtoDatabaseNegative(APITestCase):
    """
    Негативный тест класса "DatabaseCSVUpload" отвечающего за загрузку данных из CSV файлов
    в базу данных.
    """
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.path = Path(r'ascertain\tests\csv')

    def test_get_csv_files_empty_folder(self):
        """
        Тестируем будет ли вызвано исключение "EmptyFolder" в случае попытки чтения CSV
        файлов из паки где их нет.
        """
        with self.assertRaisesMessage(EmptyFolder, error_messages.EMPTY_FOLDER.message):
            with tempfile.TemporaryDirectory() as temp_dir:
                handler = DatabaseCSVUpload(temp_dir, delimiter=',')
                handler()

    def test_cant_write_to_db(self):
        """
        Тестируем будут ли сохранены старые данные в базе данных при неудачной попытке записать
        новые.
        """
        #  Записываем корректные данные в БД.
        handler_correct = DatabaseCSVUpload(self.path, delimiter=',')
        handler_correct()
        original = list(TelephoneNumbersModel.objects.all().values())

        # А теперь данные которые вызовут IntegrityError.
        path = Path(r'ascertain\tests\wrong_csv')
        handler_incorrect = DatabaseCSVUpload(path, delimiter=',')
        handler_incorrect()
        restored = list(TelephoneNumbersModel.objects.all().values())

        self.assertListEqual(
            original,
            restored,
        )