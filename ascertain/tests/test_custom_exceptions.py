import pytest

from telephone_numbers import error_messages
from telephone_numbers.custom_exceptions import EmptyFolder


class TestCustomExceptionsPositiveTest:
    """
    Позитивные тесты кастомных исключений.
    """
    def test_EmptyFolder(self):
        """
        Тест исключения "EmptyFolder".
        """
        with pytest.raises(EmptyFolder, match=error_messages.EMPTY_FOLDER.message):
            raise EmptyFolder()
