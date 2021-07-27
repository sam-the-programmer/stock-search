print('\nImporting dependencies...', end='\r')
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

import os

os.environ['TF_CPP_MIN_LOG_LEVEL']  =  '3'
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from tensorflow.keras.layers import Dense, LSTM, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
os.environ['TF_CPP_MIN_LOG_LEVEL']  =  '0'


random_state = 10

print('Parsing data...          ', end='\r')
raw = pd.read_csv('Data/FTSE Full.csv')
# plt.plot(raw['High Price'])
# plt.plot(raw['Low Price'])
# plt.show()

print('Preprocessing data...', end='\r')
print('                     ')
for i in range(len(raw.Date)):
    raw.Date[i] = int(str(raw.Date[i]).replace('/', '').replace('-', '').replace('Jan', '01').replace('Feb', '02').replace('Mar', '03').replace('Apr', '04').replace('May', '05').replace('Jun', '06').replace('Jul', '07').replace('Aug', '08').replace('Sep', '09').replace('Oct', '10').replace('Nov', '11').replace('Dec', '12'))

X = np.array(raw.Date).reshape(-1, 1)

y_high = np.array(raw['High Price']).reshape(-1, 1)
y_low = np.array(raw['Low Price']).reshape(-1, 1)

X, y_high, y_low = shuffle(X, y_high, y_low)

scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

high_model = Sequential([
    LSTM(1, return_sequences=True, input_shape=(1,)),
    Dense(25, activation='relu'),
    Dense(1, activation='relu')
])

high_model.compile(optimizer=Adam(decay=1e-4),
                   loss='mean_absolute_error',
                   metrics=['accuracy'])

high_model.save('Models/LSTMModel.h5')

history = high_model.fit(X, y_high,
                         batch_size=512,
                         epochs=200,
                         verbose=2,
                         validation_split=0.05)

plt.title('Graph Showing Loss Compared to Epochs')
plt.plot(history.history['loss'])
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_loss'])
plt.plot(history.history['val_accuracy'])
plt.show()