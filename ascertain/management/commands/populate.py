from django.core.management.base import BaseCommand

from ascertain.tasks import download_csv_files, upload_csv_to_db


class Command(BaseCommand):
    help = 'Скачивает CSV файлы с "rossvyaz.gov.ru" и записывает их в базу данных.'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        chain = download_csv_files.s() | upload_csv_to_db.s()
        chain()

        self.stdout.write(
            self.style.SUCCESS(
                'Запущенна загрузка CSV файлов и их запись в базу данных.'
                'Задача выполняется в бэкграунде.'
                'Придется подождать минутку до ее выполнения.'
                '(У вас же запущен Celery??? Если нет - то самое время его запустить!)'
            )
        )
