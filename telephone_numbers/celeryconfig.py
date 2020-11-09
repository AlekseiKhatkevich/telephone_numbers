from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

broker_url = fr'redis://{os.getenv("REDIS_LOCATION")}/{os.getenv("REDIS_CELERY_DB")}'
task_serializer = 'pickle'
accept_content = ['pickle']
timezone = 'Europe/Moscow'
broker_transport_options = {'visibility_timeout': 300}
enable_utc = True


# beat_schedule = {
# }
