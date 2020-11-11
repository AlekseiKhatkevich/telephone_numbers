import pytest
from yarl import URL
from ascertain.tasks import download_csv_files, upload_csv_to_db
import celery.exceptions
from telephone_numbers import constants
from unittest.mock import patch
from ascertain.handle_csv import DownloadCSV


class TestDownloadCSVFilesCeleryTask:
    """
    Тесты задачи Celery 'download_csv_files' по загрузке CSV файлов.
    """
    @patch.object(DownloadCSV, '__call__')
    def test_success(self, handler_class):
        """
        Тест того, вызывается ли класс "DownloadCSV" который и занимается загрузкой и сохранением
        CSV файлов.
        """
        download_csv_files(constants.CSV_URLS)
        handler_class.assert_called()

    @pytest.mark.parametrize(
        'wrong_url',
        [
            URL('https://rossvyaz.gov.ru/data/does-not-exsts.csv'),
            URL('not-an-url'),
        ])
    def test_failure(self, wrong_url):
        """
        Тест того, будет ли задача поставлена на повторное выполнение если один из респонсов != 200 или
        было возвращено хотя бы одно исключение.
        1) Респонс != 200
        2) Exception
        """
        wrong_url = URL('https://rossvyaz.gov.ru/data/does-not-exsts.csv')

        with pytest.raises(celery.exceptions.Retry):
            # noinspection PyTypeChecker
            download_csv_files([wrong_url, ])

