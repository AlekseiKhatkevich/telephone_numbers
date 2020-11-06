from telephone_numbers import constants
import asyncio
import aiohttp


class Download_CSV:
    """
    Скачивает CSV файлы с данными телефонных номеров.
    """
    urls = constants.CSV_URLS

    @staticmethod
    async def download_one_csv(
            session: aiohttp.ClientSession,
            semaphore: asyncio.Semaphore
    ) -> tuple:
        """
        Checks response status on HEAD request being sent to url address.
        """
        async with semaphore, session.get(series.imdb_url) as response:
            return response

    async def get_status(
            self,
            max_workers: int = 20,
            response_timeout: int = 7,
    ) -> Generator[series_instance, None, None]:
        """
        Runs HEAD requests in event loop asynchronously, then constricts generator with
        series, status pairs if pair is not an exception.
        """
        semaphore = asyncio.Semaphore(max_workers)

        async with aiohttp.ClientSession() as session:
            series_to_statuses = await asyncio.gather(
                *(asyncio.wait_for(self.head_status(session, series, semaphore), response_timeout)
                  for series in await self.get_queryset()
                  ), return_exceptions=True,
            )

        return (pair for pair in series_to_statuses if not isinstance(pair, Exception))