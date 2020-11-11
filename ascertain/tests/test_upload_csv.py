import pytest


@pytest.mark.django_db
class TestUploadCSVtoDatabasePositive:
    """
    Позитивный тест класса "DatabaseCSVUpload" отвечающего за загрузку данных из CSV файлов
    в базу данных.
    """