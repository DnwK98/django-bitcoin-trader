import os
import numpy as np
import tensorflow as tf
from app.service.data_provider import DataProvider, Scaler
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
from app.models import BtcValue


class DecisionService:
    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.model_path = os.path.realpath(os.path.dirname(__file__) + '/../../var/model.hdf5')

    def learn(self):
        data = self.data_provider.provide_data(since='2021-01-01', to='2021-12-14')
        test = self.data_provider.provide_data(since='2021-12-15', to='2021-12-30')
        model = self._model()

        model.fit(data[0], data[1], batch_size=32, epochs=50, verbose=1, shuffle=False,
                  validation_data=(test[0], test[1]))

        model.save(self.model_path)

    def predict(self):
        scaler = Scaler()
        model = tf.keras.models.load_model(self.model_path)

        data = BtcValue.objects.all().order_by('-date')[0:4][::-1]
        data = list(map(lambda v: v.value, data))
        for i in range(0, 3):
            x_array = np.empty((0, 3), dtype=float)
            x = list(map(lambda v: scaler.scale_down(v), data[-3::]))

            x_array = np.append(x_array, np.array([x]), axis=0)
            x_array = np.reshape(x_array, (x_array.shape[0], x_array.shape[1], 1))

            data.append(scaler.scale_up(model.predict(x_array)[0][0]))

        return data[-3::]

    def test_model(self):
        scaler = Scaler()
        model = tf.keras.models.load_model(self.model_path)
        data = self.data_provider.provide_data(since='2021-12-29', to='2021-12-30')
        i = 0
        predicted_values = []
        for x in data[0]:
            predicted = model.predict(np.array([x]))
            predicted_values.append(predicted[0][0])
            i += 1

        plt.figure(figsize=(16, 7))
        plt.plot(list(map(lambda t: scaler.scale_up(t), predicted_values)), 'r', marker='.', label='Predicted')
        plt.plot(list(map(lambda t: scaler.scale_up(t), data[1])), marker='.', label='Actual')
        plt.legend()
        plt.show()

    def _model(self):
        model = Sequential()
        shape = (3, 1)

        model.add(LSTM(units=128, activation='relu', return_sequences=True, input_shape=shape))
        model.add(Dropout(0.2))

        model.add(LSTM(units=64, activation='relu', input_shape=shape))
        model.add(Dropout(0.1))

        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.summary()

        return model
