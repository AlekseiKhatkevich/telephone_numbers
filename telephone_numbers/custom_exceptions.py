from typing import Optional

from telephone_numbers import error_messages


class EmptyFolder(Exception):
    """
    Представляет пустую папку или папку без нужных файлов.
    """

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None) -> None:
        _default_message, _default_code = error_messages.EMPTY_FOLDER

        self.message = message or _default_message
        self.code = code or _default_code

    def __str__(self) -> str:
        return self.message


