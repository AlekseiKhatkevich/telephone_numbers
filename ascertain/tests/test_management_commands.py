from unittest.mock import patch

import pytest
from django.core import management

from ascertain.tasks import download_csv_files, upload_csv_to_db


class TestManagementCommandsPositive:
    """
    Позитивные тесты менеджмент команд.
    """
    @pytest.mark.django_db
    @patch.object(upload_csv_to_db, 's', autospec=True)
    @patch.object(download_csv_files, 's', autospec=True)
    def test_populate(self, downloader, uploader):
        """
        Тестируем вызываются ли задачи celery "upload_csv_to_db" и "download_csv_files"
        при выполнении менеджмент команды "populate".
        """
        management.call_command('populate')

        downloader.assert_called_once()
        uploader.assert_called_once()