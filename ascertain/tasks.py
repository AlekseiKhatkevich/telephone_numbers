from typing import Iterable

from celery import Task, shared_task
from django.db.utils import OperationalError
from rest_framework import status
from yarl import URL

from ascertain.handle_csv import DatabaseCSVUpload, DownloadCSV
from telephone_numbers import constants


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=30 * 60,
    max_retries=8,
    soft_time_limit=5 * 60,
    time_limit=10 * 60,
)
def download_csv_files(self: Task, urls_list: Iterable[URL] = constants.CSV_URLS) -> None:
    """
    Задача по загрузке CSV файлов на сервер.
    Загружаем все файлы с помощью DownloadCSV.
    Если один или более респонсов полученных с удаленного сервера имеют статус != 200,
    то соответствующие файлы не были загружены и сохранены DownloadCSV. В данном случае эти файлы
    загружаются повторно через определенный интервал 'default_retry_delay'
    ('max_retries' попыток в сумме).
    Все исключения передаются из DownloadCSV и обрабатываются здесь.
    """
    downloader = DownloadCSV(urls_list)

    responses = downloader()

    # Повтор задачи при наличии исключений переданных из DownloadCSV.
    exceptions = [*filter(lambda response: isinstance(response, Exception), responses)]
    if exceptions:
        self.retry()

    # Повтор задачи при наличии не 200х респонсов переданных из DownloadCSV.
    bad_responses = [*filter(lambda response: response.status != status.HTTP_200_OK, responses)]
    if bad_responses:
        urls_to_retry = [response.url for response in bad_responses]
        self.retry([urls_to_retry, ],)


@shared_task(
    autoretry_for=(OperationalError,),
    default_retry_delay=60 * 60,
    max_retries=4,
    soft_time_limit=5 * 60,
    time_limit=10 * 60,
)
def upload_csv_to_db(*args, **kwargs) -> None:
    """
    Задача загружает данные из сохраненных CSV файлов в базу данных с помощью DatabaseCSVUpload.
    Задача должна запускаться после успешного выполнения задачи 'download_csv_files'.
    """
    uploader = DatabaseCSVUpload()
    uploader()

