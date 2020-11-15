from pathlib import Path

import pytest
from django.http import QueryDict
from psycopg2.extras import NumericRange


@pytest.fixture(scope='function')
def data_for_model() -> dict:
    """
    Возвращает данные для позитивного создания экземпляра класса модели 'TelephoneNumbersModel'
    """
    data = {
        'abc_or_def': 917,
        'numbers_range': NumericRange(3400000, 3900000, '[)'),
        'volume': 500000,
        'operator': 'ПАО "Мобильные ТелеСистемы"',
        'region': 'Республика Башкортостан',
    }

    return data


@pytest.fixture(scope='function')
def query_dict() -> QueryDict:
    """
    Возвращает "QueryDict"
    """
    return QueryDict(mutable=True)


@pytest.fixture(scope='function')
def dummy_cache(settings) -> None:
    """
    Устанавливает 'django.core.cache.backends.dummy.DummyCache' в качестве кэш бэкэнда.
    """
    DUMMY_CACHE = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    settings.CACHES = DUMMY_CACHE
