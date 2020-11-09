from celery import shared_task
from rest_framework import status

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
def download_csv_files(self, urls_list=constants.CSV_URLS):
    """
    """
    downloader = DownloadCSV(urls_list)

    responses = downloader()
    bad_responses = [*filter(lambda response: response.status != status.HTTP_200_OK, responses)]

    if bad_responses:
        urls_to_retry = [response.url for response in bad_responses]
        self.retry([urls_to_retry, ],)


@shared_task
def upload_csv_to_db(*args, **kwargs):
    """
    """
    uploader = DatabaseCSVUpload()
    uploader()

