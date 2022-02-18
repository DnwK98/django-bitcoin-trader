import requests
import json
from datetime import datetime
from typing import List


class Kline:
    def __init__(self, d: dict):
        self.datetime = datetime.fromtimestamp(d[0] / 1000)
        self.value = d[1]


class Binance:
    def __init__(self):
        self.url = 'https://api.binance.com'
        pass

    def test(self) -> int:
        data = requests.get(self.url + '/api/v3/time')
        response = json.loads(data.text)
        return int(response['serverTime'])

    def klines(self, day, interval='1h') -> List[Kline]:
        start = datetime.strptime(day + ' 00:00', '%Y-%m-%d %H:%M')
        mid = datetime.strptime(day + ' 12:00', '%Y-%m-%d %H:%M')
        end = datetime.strptime(day + ' 23:59', '%Y-%m-%d %H:%M')
        data = requests.get(self.url + '/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}&limit={}'.format(
            'BTCUSDT',
            interval,
            int(start.timestamp()) * 1000,
            int(mid.timestamp()) * 1000,
            1000
        ))
        data = json.loads(data.text)

        response = []
        for d in data:
            response.append(Kline(d))

        data = requests.get(
            self.url + '/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}&limit={}'.format(
                'BTCUSDT',
                interval,
                int(mid.timestamp()) * 1000 + 1,
                int(end.timestamp()) * 1000,
                1000
            ))
        data = json.loads(data.text)

        for d in data:
            response.append(Kline(d))

        return response


class BinanceCachingDecorator(Binance):
    def __init__(self, wrapped: Binance):
        super().__init__()
        self.wrapped = wrapped
        self.cache = {}

    def test(self) -> int:
        return self.wrapped.test()

    def klines(self, day, interval='1h') -> list:
        if day + interval in self.cache:
            return self.cache[day + interval]
        if len(self.cache) > 20:
            self.cache.clear()

        data = self.wrapped.klines(day, interval)
        self.cache[day + interval] = data
        return data
