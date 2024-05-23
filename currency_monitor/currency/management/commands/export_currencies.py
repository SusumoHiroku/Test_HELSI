import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from currency.models import Currency, Rate
from currency.services_test import fetch_currency_data


class Command(BaseCommand):
    help = 'Export currencies to a CSV file'

    def handle(self, *args, **kwargs):
        fetch_currency_data()

        currencies = Currency.objects.all()
        filename = f'currencies_{timezone.now().strftime("%Y_%m_%d_%H_%M")}.csv'

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name A', 'Name B', 'Alpha3 A', 'Alpha3 B', 'Rate Buy', 'Rate Sell', 'Rate Cross'])
            for currency in currencies:
                latest_rate = Rate.objects.filter(currency=currency).order_by('-date').first()
                if latest_rate:
                    writer.writerow([
                        currency.name_a,
                        currency.name_b,
                        currency.alpha3_a,
                        currency.alpha3_b,
                        latest_rate.rate_buy,
                        latest_rate.rate_sell,
                        latest_rate.rate_cross
                    ])
                else:
                    writer.writerow([
                        currency.name_a,
                        currency.name_b,
                        currency.alpha3_a,
                        currency.alpha3_b,
                        'N/A',
                        'N/A',
                        'N/A'
                    ])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported currencies to {filename}'))
