import asyncio
import csv
import itertools
from pathlib import Path
from typing import Container, Coroutine, Generator, Iterable, Iterator, Optional, Union

import aiofiles
import aiohttp
from aiohttp.client import ClientResponse
from asgiref.sync import sync_to_async
from django.core.management.color import no_style
from django.db import DatabaseError, InterfaceError, connection, models, transaction
from psycopg2.extras import NumericRange
from rest_framework import status
from yarl import URL

from ascertain.models import TelephoneNumbersModel
from telephone_numbers import constants


class DatabaseCSVUpload:
    """
    Зашружает данные из CSV файлов в 'path' в таблицу, предварительно удалив старые данные.
    """
    def __init__(self,
                 path: Union[Path, str] = Path('ascertain/csv_files'),
                 encoding: str = 'utf-8',
                 delimiter: str = ';',
                 batch_size: int = 2000,
                 model: models.Model = TelephoneNumbersModel,
                 ) -> None:
        self.path = Path(path)
        self.encoding = encoding
        self.delimiter = delimiter
        self.batch_size = batch_size
        self.model = model

    def get_csv_files(self) -> Generator[Path, None, None]:
        """
        Возвращает генератор с объектами pathlib.Path содержащими путь к CSV файлам
        в папке 'path'.
        """
        return self.path.glob('*.csv')

    def read_csv(self, file_path: Path) -> Iterator[dict]:
        """
        Читает один CSV файл, возвращает итератор строк этого файла, где каждая строка это словарь
        ключами которого являются поля хэедера CSV, а значениями - данные из соответвующих колонок.
        Пример:
            {
            'АВС/ DEF': '900',
            'От': '0000000',
            'До': '0061999',
            'Емкость': '62000',
            'Оператор': 'ООО "Т2 Мобайл"',
            'Регион': 'Краснодарский край',
               }
        """
        with file_path.open(newline='', encoding=self.encoding, errors='surrogateescape') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=self.delimiter, quotechar='|')

            yield from csv_reader

    def create_instance(self, row: dict) -> models.Model:
        """
        Создает один экземпляр класса модели из одной строчки CSV файла.
        """
        fields = {
            'abc_or_def': int(row['АВС/ DEF']),
            'numbers_range': NumericRange(
                int(row['От']),
                int(row['До']),
                bounds='[]',
            ),
            'volume': int(row['Емкость']),
            'operator': row['Оператор'],
            'region': row['Регион'],
        }

        return self.model(**fields)

    def write_csv_to_db(self, instances: itertools.chain) -> None:
        """
        Записывает данные в таблицу отправляя их партиями по 'batch_size'.
        """
        while True:
            batch = list(itertools.islice(instances, self.batch_size))
            if not batch:
                break
            else:
                self.model.objects.bulk_create(
                        batch,
                        ignore_conflicts=True,
                    )

    def reset_pk(self):
        """
        Сюрасывает счетчик PK модели в начальное положение.
        """
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [self.model, ])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

    def __call__(self, *args, **kwargs) -> str:
        """
        Запускает процесс загрузки данных из CSV файлов в таблицу.
        ход1
        1 - Для каждого CSV файла из 'path' получаем генератор строк.
        2 - Для каждой строки создаем экземпляр класса модели.
        3 - Создаем генератор экземпларов класса модели.
        4 - Помещаем данный генератор в пул генераторов.
        5 - Создаем общий генератор всех прошедших итераций.
        ход2
        Транзакционно:
        1 -  Удалем все данные из таблицы.
        2 - Сбрасываем счетчик PK
        3 - Записываем все данные в таблицу
        4 - Коммит данных или откат до сейвпойнта.
        """
        instances_gen_pool = []
        for file in self.get_csv_files():
            csv_generator = self.read_csv(file)
            # noinspection PyTypeChecker
            instances_gen = (self.create_instance(row) for row in csv_generator)
            instances_gen_pool.append(instances_gen)

        instances_final_gen = itertools.chain(*instances_gen_pool)

        try:
            with transaction.atomic():
                self.model.objects.all().delete()
                self.reset_pk()
                self.write_csv_to_db(instances_final_gen)
        except (DatabaseError, InterfaceError) as err:
            return f'При записи данных возникли исключения. Таблица {self.model._meta.db_table}' \
                   f'возвращенна к предыдущему состоянию. Данные об исключении:' \
                   f' \n {str(err)}'
        else:
            count = self.model.objects.all().count()
            return f'Созданно {count} записей в базе данных.'


class DownloadCSV:
    """
    Скачивает CSV файлы с данными телефонных номеров.
    rossvyaz.gov.ru обновляет данные файлы каждый день в 12 ночи, изменяя 'etag', 'last-modified'
    (проверял лично) и пр. Поэтому при загрузке CSV в базу по ночам раз в сутки клиентское кеширование
     не имеет смысла. Все равно 'etag' каждый раз новый и мы реально не знаем обновился ли файл и 'etag'
     или просто 'etag'.
    """

    def __init__(self,
                 urls: Iterable[URL] = constants.CSV_URLS,
                 path: Union[Path, str] = Path('ascertain/csv_files'),
                 chunk_size: int = 100000,
                 response_timeout: Optional[Union[float, int]] = 2 * 60,
                 ) -> None:
        self.urls = urls
        self.path = Path(path)
        self.chunk_size = chunk_size
        self.response_timeout = response_timeout

    @sync_to_async
    def get_path(self, url: URL) -> Coroutine[URL, None, URL]:
        """
        Создает путь к записываемому csv файлу путем конкатенации 'path' и последней части 'url''.
        'ascertain/csv_files' + 'ABC-3xx.csv' = 'ascertain/csv_files/ABC-3xx.csv'
        """
        return self.path / url.name

    async def download_one_csv(self,
                               session: aiohttp.ClientSession,
                               url: URL,
                               ) -> ClientResponse:
        """
        Получает содержимое CSV файла с сервера и записывает его в файл.
        В случае любого статуса за исключением 200 рейзит HttpProcessingError.
        """
        async with session.get(url) as response:

            if response.status == status.HTTP_200_OK:
                await asyncio.create_task(self.write_one_file(response, url))

            return response

    async def write_one_file(self, response: ClientResponse, url: URL) -> None:
        """
        Записывает полезную нагрузку респонса в файл потоково кусками по 'chunk_size'.
        """
        async with aiofiles.open(await self.get_path(url), mode='wb') as file:

            while True:
                chunk = await response.content.read(self.chunk_size)
                if not chunk:
                    break
                else:
                    await file.write(chunk)

    async def download_all_csv(self) -> Container:
        """
        Запускает загрузку и сохранение на диск всех файлов.
        """
        async with aiohttp.ClientSession() as session:
            mutual_response = await asyncio.gather(
                *[
                    asyncio.wait_for(
                        self.download_one_csv(session, url),
                        self.response_timeout
                    ) for url in self.urls
                ],
                return_exceptions=True,
            )

        return mutual_response

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Запускает весь процесс.
        1 - Ассинхронно загружаем csv файлы.
        2 - Ассинхронно записываем их на диск.
        """
        mutual_response = asyncio.run(self.download_all_csv())

        return mutual_response


