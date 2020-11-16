"""Конфигурационный файл Gunicorn"""

import sys
import threading
import traceback
from multiprocessing import cpu_count

from django.conf import settings


bind = '0.0.0.0:8000'
backlog = 1000
workers = cpu_count()
worker_class = 'gthread'
worker_connections = 1000
timeout = 30
graceful_timeout = 5
keepalive = 2
max_request = max_requests_jitter = 30

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

proc_name = 'Gunicorn WSGI сервер в докере.'

reload = settings.DEBUG


def worker_int(worker):
    worker.log.info('worker получил сигнал INT или QUIT ')

    #  Получаем traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append(f'\n# Поток: {id2name.get(threadId, "")}({threadId})')

        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append(f'Файл: {filename}, строка {lineno}, в {name}')
            if line:
                code.append(f'  {line.strip()}')

    worker.log.debug('\n'.join(code))


def worker_abort(worker):
    worker.log.info('worker получил сигнал SIGABRT')
