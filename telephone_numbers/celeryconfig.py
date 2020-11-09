from django.conf import settings
from celery.schedules import crontab
from telephone_numbers import constants
from celery import signature

broker_url = fr'redis://{settings.REDIS_LOCATION}/{settings.REDIS_CELERY_DB}'
result_backend = fr'redis://{settings.REDIS_LOCATION}/{settings.REDIS_CELERY_RESULT_BACKEND_DB}'
task_serializer = 'pickle'
accept_content = ['pickle', 'json', ]
timezone = 'Europe/Moscow'
broker_transport_options = {'visibility_timeout': 300}
enable_utc = True

beat_schedule = {
    'chained': {
        'task': 'ascertain.tasks.download_csv_files',
        'schedule': crontab(hour=20, minute=19, ),
        'options': {
            'link': signature('ascertain.tasks.upload_csv_to_db'),
        },
        'args': (constants.CSV_URLS,)
    }
}
