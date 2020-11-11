import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telephone_numbers.settings')

app = Celery('telephone_numbers')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('telephone_numbers.celeryconfig')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def mul(x, y):
    return x * y

# celery -A telephone_numbers worker --loglevel=INFO -E
# celery -A telephone_numbers  beat --loglevel=INFO --pidfile=
