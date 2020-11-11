from collections import namedtuple

error_message = namedtuple('error_message', ('message', 'code',))

EMPTY_FOLDER = error_message(
    'В папке нет ни одного CSV файла. Нечего загружать.',
    'empty_folder',
)
