from pathlib import Path

import pytest
from psycopg2.extras import NumericRange

#  pytest_plugins = ('celery.contrib.pytest', )


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


@pytest.fixture(scope='module')
def path_to_test_csv_folder() -> Path:
    """
    Возвращает путь до папки с тестовыми CSV файлами.
    """
    return Path(r'ascertain\tests\csv')

