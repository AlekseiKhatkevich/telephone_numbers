import asyncio
from pathlib import Path
from typing import Container, Iterable, Optional, Union

import aiofiles
import aiohttp
from aiohttp.client import ClientResponse
from rest_framework import status

from telephone_numbers import constants


class Download_CSV:
    """
    Скачивает CSV файлы с данными телефонных номеров.
    rossvyaz.gov.ru обновляет данные файлы каждый день в 12 ночи, изменяя 'etag', 'last-modified'
    (проверял лично) и пр. Поэтому при загрузке CSV в базу по ночам раз в сутки клиентское кеширование
     не имеет смысла. Все равно 'etag' каждый раз новый и мы реально не знаем обновился ли файл и 'etag'
     или просто 'etag'.
    """

    def __init__(self,
                 urls: Iterable = constants.CSV_URLS,
                 path: Union[Path, str] = Path('ascertain/csv_files'),
                 chunk_size: int = 100000,
                 response_timeout: Optional[Union[float, int]] = 60,
                 ) -> None:
        self.urls = urls
        self.path = Path(path)
        self.chunk_size = chunk_size
        self.response_timeout = response_timeout

    def get_path(self, url: str) -> Path:
        """
        Создает путь к записываемому csv файлу путем конкатенации 'path' и последней части 'url''.
        'ascertain/csv_files' + 'ABC-3xx.csv' = 'ascertain/csv_files/ABC-3xx.csv'
        """
        return self.path / url.split('/')[-1]

    async def download_one_csv(self,
                               session: aiohttp.ClientSession,
                               url: str,
                               ) -> ClientResponse:
        """
        Получает содержимое CSV файла с сервера и записывает его в файл.
        В случае любого статуса за исключением 200 рейзит HttpProcessingError.
        """
        async with session.get(url) as response:

            if response.status == status.HTTP_200_OK:
                await asyncio.create_task(self.write_one_file(response, url))

            return response

    async def write_one_file(self, response: ClientResponse, url: str) -> None:
        """
        Записывает полезную нагрузку респонса в файл потоково кусками по 'chunk_size'.
        """
        async with aiofiles.open(self.get_path(url), mode='wb') as file:

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
                        self.download_one_csv(session, url), self.response_timeout
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


