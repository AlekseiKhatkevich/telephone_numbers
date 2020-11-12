import pytest
from django.urls import resolve
from django.urls.exceptions import NoReverseMatch
from rest_framework.reverse import reverse


class TestCustomPathConvertersPositive:
    """
    Позитивные тесты на кастомные конвертеры урлов.
    """
    name = 'operator'
    correct_number = 79173453223
    correct_url = reverse(name, args=(correct_number,))

    def test_msisdn_converter(self):
        """
        Тест того пропустит ли конвертер MSISDNConverter
        телефонный номер в корректном формате MSISDN для России.
        """
        resolver_match = resolve(self.correct_url)

        assert resolver_match.url_name == self.name

    def test_url_kwargs(self):
        """
        Тест того, распарсит ли конвертер MSISDNConverter MSISDN на CC, NDC, SN и полный номер
        """
        resolver_match = resolve(self.correct_url)
        kwargs_dict = resolver_match.kwargs['msisdn']

        expected_dict = dict(
            number=self.correct_number,
            cc=7,
            ndc=917,
            sn=3453223,
        )

        assert kwargs_dict == expected_dict

    def test_reverse(self):
        """
        Тест того работает ли нормально "reverse" с данным конвертером MSISDNConverter
        и вернет ли он полны урл по базовому имени.
        """
        url = reverse('operator', args=(self.correct_number,))

        assert url == self.correct_url


class TestCustomPathConvertersNegative:
    """
    Негативные тесты на кастомные конвертеры урлов.
    """
    name = 'operator'
    incorrect_numbers = (19173453223, 791734532231, 7917345322,)

    @pytest.mark.parametrize('wrong_msisdn', incorrect_numbers)
    def test_msisdn_converter_wrong_msisdn(self, wrong_msisdn):
        """
        Тестируем будет ли конвертер  MSISDNConverter возбуждать исключения при попытках подать
        на него номера в неправильном формате MSISDN для России.
        """
        with pytest.raises(NoReverseMatch):
            url = reverse(self.name, args=(wrong_msisdn,))
            resolve(url)