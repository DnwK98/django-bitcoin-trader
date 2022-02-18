from app.service.binance import Binance
from datetime import datetime, timedelta
from app.models import BtcValue


class SyncService:
    def __init__(self, client: Binance):
        self.client = client

    def sync(self, from_day: str, to_day: str):
        current = datetime.strptime(from_day + ' 00:00', '%Y-%m-%d %H:%M')
        to = datetime.strptime(to_day + ' 00:00', '%Y-%m-%d %H:%M')

        while current <= to:
            print(f"Sync {current.strftime('%Y-%m-%d')}")
            self.__remove_day(current)
            data = self.client.klines(current.strftime('%Y-%m-%d'), '5m')
            records = []
            for d in data:
                record = BtcValue()
                record.date = d.datetime
                record.value = d.value
                records.append(record)
            BtcValue.objects.bulk_create(records)
            current += timedelta(days=1)

    def __remove_day(self, current):
        BtcValue.objects\
            .filter(date__gte=current.strftime('%Y-%m-%d 00:00'),
                    date__lte=current.strftime('%Y-%m-%d 23:59'))\
            .delete()

