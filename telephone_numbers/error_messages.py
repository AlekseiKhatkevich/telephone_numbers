from collections import namedtuple

error_message = namedtuple('error_message', ('message', 'code',))

EMPTY_FOLDER = error_message(
    'В папке нет ни одного CSV файла. Нечего загружать.',
    'empty_folder',
)
NUMBER_NOT_FOUND = error_message(
    'Данный телефонный номер не найден в базе номеров.',
    'number_not_found',
)
MULTIPLE_NUMBERS = error_message(
    'Данный телефонный номер принадлежит более чем одному оператору связи.'
    'Чего быть не может в принципе. Но раз такое произошло то свяжитесь с администрацией.',
    'multiple_numbers',
)
