import requests
from django.utils import timezone
from .models import Currency, Rate
from .utils import get_currency_info


def fetch_currency_data_from_api():
    url = 'https://api.monobank.ua/bank/currency'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching currency data from API: {e}")
        return []


def process_currency_data(data):
    for item in data:
        code_a = item['currencyCodeA']
        code_b = item['currencyCodeB']
        rate_buy = item.get('rateBuy')
        rate_sell = item.get('rateSell')
        rate_cross = item.get('rateCross')
        timestamp = item['date']

        name_a, alpha3_a = get_currency_info(code_a)
        name_b, alpha3_b = get_currency_info(code_b)

        if not name_a or not name_b:
            continue

        save_currency_data(code_a, code_b, name_a, name_b, alpha3_a, alpha3_b, rate_buy, rate_sell, rate_cross,
                           timestamp)


def save_currency_data(code_a, code_b, name_a, name_b, alpha3_a, alpha3_b, rate_buy, rate_sell, rate_cross, timestamp):
    currency, _ = Currency.objects.get_or_create(
        code_a=code_a, code_b=code_b,
        defaults={
            'name_a': name_a,
            'name_b': name_b,
            'alpha3_a': alpha3_a,
            'alpha3_b': alpha3_b
        }
    )

    Rate.objects.create(
        currency=currency,
        rate_buy=rate_buy,
        rate_sell=rate_sell,
        rate_cross=rate_cross,
        date=timezone.datetime.fromtimestamp(timestamp)
    )


def fetch_currency_data():
    data = fetch_currency_data_from_api()
    process_currency_data(data)
