import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_monitor.settings')

app = Celery('currency_monitor')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'fetch-currency-every-4-hours': {
        'task': 'currency.tasks.fetch_currency_data_task',
        'schedule': crontab(minute=0, hour='*/2'),
    },
}
