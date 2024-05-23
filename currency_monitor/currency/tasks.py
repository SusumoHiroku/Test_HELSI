from celery import shared_task
# from .services import fetch_currency_data
from .services_test import fetch_currency_data



@shared_task
def fetch_currency_data_task():
    fetch_currency_data()
