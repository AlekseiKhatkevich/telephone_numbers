from collections import namedtuple

error_message = namedtuple('error_message', ('message', 'code',))

ABC_OR_DEF_LENGTH = error_message(
    'Поле "abc_or_def" должно быть 3х значным интегром',
    'abc_or_def_length',
)