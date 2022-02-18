from django.core.management.base import BaseCommand
from app.service.binance import Binance, BinanceCachingDecorator
from app.service.sync import SyncService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--from')
        parser.add_argument('--to')

    def handle(self, *args, **options):
        date_from = options['from']
        date_to = options['to']
        print(f"Sync from {date_from} to {date_to}")

        binance = BinanceCachingDecorator(Binance())
        service = SyncService(binance)

        service.sync(date_from, date_to)
