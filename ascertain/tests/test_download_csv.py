import csv
import string
from pathlib import Path
from yarl import URL
from rest_framework import status

from ascertain.handle_csv import DownloadCSV
from telephone_numbers import constants


class TestDownloadCSVPositive:
    """
    Позитивный тест класса "DownloadCSV" отвечающего за загрузку CSV файлов из интернета на
    локальную машину.
    """
    urls = (constants.CSV_URLS[-1],)

    @staticmethod
    def is_csv(infile):
        """
        Является ли файл валидным CSV файлом.
        Цельнотянуто отсюда -
         https://stackoverflow.com/questions/2984888/check-if-file-has-a-csv-format-with-python
        """
        try:
            with open(infile, newline='', encoding='utf-8') as csvfile:
                start = csvfile.read(1028)
                # isprintable does not allow newlines, printable does not allow umlauts...
                if not all([c in string.printable or c.isprintable() for c in start]):
                    return False
                dialect = csv.Sniffer().sniff(start)
                return True
        except csv.Error:
            # Could not get a csv dialect -> probably not a csv.
            return False

    def test_class(self, tmp_path):
        """
        Тест того, что класс  "DownloadCSV"  при вызове его как callable загружает CSV
        файлы и записывает их на диск. Закачиваем только один самый малый CSV файл.
        """
        handler = DownloadCSV(urls=self.urls, path=tmp_path)

        [response] = handler()
        assert response.status == status.HTTP_200_OK

        #  Убеждаемся в том, что файл сохранен на диск.
        [url] = self.urls
        path_to_file = Path(tmp_path) / url.name
        assert path_to_file.exists()

        # Убеждаемся в том, что сохраненный файл является валидным CSV файлом.
        assert self.is_csv(path_to_file)


class TestDownloadCSVNegative:
    """
     Негативный тест класса "DownloadCSV" отвечающего за загрузку CSV файлов из интернета на
    локальную машину.
    """
    urls = (
        constants.CSV_URLS[-1],
        URL('https://rossvyaz.gov.ru/data/does-not-exists.csv')
    )

    def test_download_errors_url(self, tmp_path):
        """
        В случае получения не 200-го респонса или исключения с одного из урлов другие файлы должны быть
        закачанны тем не менее.
        """
        handler = DownloadCSV(urls=self.urls, path=tmp_path)

        responses = handler()
        assert any(response.status != status.HTTP_200_OK for response in responses)

        correct_url = constants.CSV_URLS[-1]
        path_to_file = Path(tmp_path) / correct_url.name
        assert path_to_file.exists()

