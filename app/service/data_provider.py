import numpy as np
from app.models import BtcValue


class DataProvider:

    def provide_data(self, since: str = '1970-01-01', to: str = '2100-01-01'):
        return self._provide_normal_data(since, to)

    def get_day_data(self):
        return BtcValue.objects.all().order_by('-date')[0:288][::-1]

    def get_month_data(self):
        return BtcValue.objects.all().order_by('-date')[0:8640][::-1]

    def _provide_normal_data(self, since: str, to: str):
        scaler = Scaler()
        data = BtcValue.objects.filter(date__gte=since, date__lte=to).all()
        x_array = np.empty((0, 3), dtype=float)
        y_array = np.array([])
        for i in range(2, len(data) - 1):
            values = [
                # data[i - 48],
                # data[i - 24],
                # data[i - 12],
                data[i - 2],
                data[i - 1],
                data[i]
            ]
            x = list(map(lambda x: scaler.scale_down(x.value), values))
            y = scaler.scale_down(data[i + 1].value)

            x_array = np.append(x_array, np.array([x]), axis=0)
            y_array = np.append(y_array, y)
        x_array = np.reshape(x_array, (x_array.shape[0], x_array.shape[1], 1))

        return x_array, y_array

    def _provide_diff_data(self, since: str = '1970-01-01', to: str = '2100-01-01'):
        scaler = Scaler()
        data = BtcValue.objects.filter(date__gte=since, date__lte=to).all()
        x_array = np.empty((0, 4), dtype=float)
        y_array = np.array([])
        for i in range(3, len(data) - 1):
            x = [
                # data[i - 4].value - data[i - 5].value,
                # data[i - 3].value - data[i - 4].value,
                data[i - 2].value - data[i - 3].value,
                data[i - 2].value - data[i - 3].value,
                data[i - 1].value - data[i - 2].value,
                data[i].value - data[i - 1].value
            ]
            x = list(map(lambda v: scaler.scale_down(v), x))
            y = scaler.scale_down(data[i + 1].value - data[i].value)

            x_array = np.append(x_array, np.array([x]), axis=0)
            y_array = np.append(y_array, y)

        x_array = np.reshape(x_array, (x_array.shape[0], x_array.shape[1], 1))

        return x_array, y_array


    def _provide_diff_long_data(self, since: str = '1970-01-01', to: str = '2100-01-01'):
        scaler = Scaler()
        data = BtcValue.objects.filter(date__gte=since, date__lte=to).all()
        x_array = np.empty((0, 6), dtype=float)
        y_array = np.array([])
        for i in range(48, len(data) - 1):
            x = [
                data[i - 48].value - data[i - 24].value,
                data[i - 24].value - data[i - 12].value,
                data[i - 12].value - data[i - 3].value,
                data[i - 2].value - data[i - 3].value,
                data[i - 1].value - data[i - 2].value,
                data[i].value - data[i - 1].value
            ]
            x = list(map(lambda v: scaler.scale_down(v), x))
            y = scaler.scale_down(data[i + 1].value - data[i].value)

            x_array = np.append(x_array, np.array([x]), axis=0)
            y_array = np.append(y_array, y)

        x_array = np.reshape(x_array, (x_array.shape[0], x_array.shape[1], 1))

        return x_array, y_array

    def _provide_legacy_data(self, since: str = '1970-01-01', to: str = '2100-01-01'):
        scaler = Scaler()
        data = BtcValue.objects.filter(date__gte=since, date__lte=to).all()
        x_array = np.empty((0, 8), dtype=float)
        y_array = np.array([])
        for i in range(672, len(data) - 1):
            values = [data[i - 672], data[i - 192], data[i - 96], data[i - 16],
                      data[i - 3], data[i - 2], data[i - 1], data[i]]
            x = list(map(lambda x: scaler.scale_down(x.value), values))
            y = scaler.scale_down(data[i + 1].value)

            x_array = np.append(x_array, np.array([x]), axis=0)
            y_array = np.append(y_array, y)
        x_array = np.reshape(x_array, (x_array.shape[0], x_array.shape[1], 1))

        return x_array, y_array


class Scaler:
    min = 25000
    max = 70000

    def scale_up(self, val):
        return val * (self.max - self.min) + self.min

    def scale_down(self, val):
        return (val - self.min) / (self.max - self.min)
