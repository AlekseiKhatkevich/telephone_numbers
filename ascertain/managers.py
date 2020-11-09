import datetime

from django.db import connection, models


class TelephoneNumbersModelManager(models.Manager):
    """
    Менеджер модели TelephoneNumbersModel.
    """

    def table_update_time(self, timezone: str = 'Europe/Moscow') -> datetime.datetime:
        """
        Получает время последнего обновления таблицы модели 'TelephoneNumbersModelManager'.
        """
        sql = f"""
                SELECT  
                    pg_xact_commit_timestamp(xmin) at time zone '{timezone}'
                FROM  
                    {self.model._meta.db_table}
                LIMIT 1
                ;
                """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            [last_update_time] = cursor.fetchone()

        return last_update_time
