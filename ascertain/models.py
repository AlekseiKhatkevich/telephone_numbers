import re

from django.contrib.postgres.fields import IntegerRangeField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.functional import cached_property
from psycopg2.extras import NumericRange

from telephone_numbers import error_messages


class TelephoneNumbersModel(models.Model):
    """
    Модель представляет базу телефонных номеров по операторам связи.
    """
    abc_or_def = models.PositiveSmallIntegerField(
        verbose_name='АВС/DEF',
        validators=[
            RegexValidator(
                re.compile(r'^[\d]{3}$'),
                *error_messages.ABC_OR_DEF_LENGTH,
            ), ]
    )
    numbers_range = IntegerRangeField(
        verbose_name='Диапазон номеров без АВС/DEF.'
    )
    volume = models.PositiveSmallIntegerField(
        verbose_name='Емкость диапазона номеров',
    )
    operator = models.CharField(
        verbose_name='Наименование оператора связи',
        max_length=50,
    )
    region = models.CharField(
        verbose_name='Местоположение оператора связи',
        max_length=100,
    )
    update_date = models.DateTimeField(
        verbose_name='Время последнего обновления данных',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Диапазон телефонных номеров'
        verbose_name_plural = 'Диапазоны телефонных номеров'
        unique_together = ('abc_or_def', 'numbers_range',)
        required_db_vendor = 'postgresql'

    def __str__(self):
        return f'ABC/DEF {self.abc_or_def}, range {self.numbers_range}'

    def __repr__(self):
        return f'{self.pk=} ~ {self.abc_or_def=} ~ {self.numbers_range=}'

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)

    # todo
    @cached_property
    def get_absolute_url(self):
        pass


test = dict(
    abc_or_def=301,
    numbers_range=NumericRange(2110000, 2129999, bounds='[]',),
    volume=20000,
    operator='ПАО "Ростелеком"',
    region='г. Улан-Удэ|Республика Бурятия',
)
