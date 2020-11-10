class EmptyFolder(Exception):
    """
    Представляет пустую папку или папку без нужных файлов.
    """

    def __init__(self, message: str = None, code: str = None) -> None:
        _default_message = 'В папке нет ни одного CSV файла. Нечего загружать.'
        _default_code = 'empty_folder'

        self.message = message or _default_message
        self.code = code or _default_code

    def __str__(self) -> str:
        return self.message


