import asyncio
from pathlib import Path

import aiofiles
import aiohttp
from rest_framework import status
import datetime
from telephone_numbers import constants


#RuntimeError: Event loop is closed
# аннотация
# описание методов


class Download_CSV:
    """
    Скачивает CSV файлы с данными телефонных номеров.
    """

    def __init__(self,
                 urls=constants.CSV_URLS,
                 path=Path('ascertain/csv_files'),
                 ) -> None:
        self.urls = urls
        self.path = path

    def get_path(self, url):
        """
        """
        return self.path / url.split('/')[-1]

    async def download_one_csv(self, session: aiohttp.ClientSession, url: str):
        """
        Скачивает один CSV файл.
        """
        async with session.get(url) as response:
            await self.write_one_file(response, url)

            return response
            # if response.status == status.HTTP_200_OK:
            #     async with aiofiles.open(self.get_path(url), mode='wb') as file:
            #         while True:
            #             chunk = await response.content.read(1000)
            #             if not chunk:
            #                 break
            #             await file.write(chunk)

    async def write_one_file(self, response, url):
        """
        """
        if response.status == status.HTTP_200_OK:
            async with aiofiles.open(self.get_path(url), mode='wb') as file:
                while True:
                    chunk = await response.content.read(1000)
                    if not chunk:
                        break
                    await file.write(chunk)

    async def download_all_csv(self):
        """
        """
        async with aiohttp.ClientSession() as session:
            mutual_content = await asyncio.gather(
                *[self.download_one_csv(session, url)for url in self.urls],
                return_exceptions=True,
            )

        return mutual_content

    def __call__(self, *args, **kwargs):
        """

        """
        a =datetime.datetime.now()
        mutual_content = asyncio.run(self.download_all_csv())
        delta = datetime.datetime.now() -a
        print(delta)
        return mutual_content
