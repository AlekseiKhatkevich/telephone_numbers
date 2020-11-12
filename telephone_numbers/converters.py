class MSISDNConverter:
    """
    Path converter для проверки MSISDN на валидность.
        CC=1 цифра (7)
        NDC=3 цифры (например, 903)
        SN=7 цифр (1234567),
        итого — 11 цифр (итоговый пример: 7-903-1234567).

    Парсит номер в формате MSISDN на части CC, NDC, SN и полный номер.
    Возвращает во вью через резолвер словарь с этими частями.
    Обратно принимает MSISDN.
    """
    regex = r'7[0-9]{3}[0-9]{7}'

    def to_python(self, value):
        number = int(value)
        cc = int(value[0])
        ndc = int(value[1:4])
        sn = int(value[4:])

        return {'cc': cc, 'ndc': ndc, 'sn': sn, 'number': number}

    def to_url(self, value):
        return str(value)
