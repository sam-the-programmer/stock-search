print('\nImporting dependencies...', end='\r')
import warnings

warnings.filterwarnings('ignore')

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

os.environ['TF_CPP_MIN_LOG_LEVEL']  =  '3'
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from tensorflow.keras.layers import Dense, Dropout, LSTM, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

os.environ['TF_CPP_MIN_LOG_LEVEL']  =  '0'


random_state = 10

print('Parsing data...          ', end='\r')
raw = pd.read_csv('Data/FTSE Full.csv') #yf.download('AAPL', period='10y', progress=False).dropna().reset_index()


print('Preprocessing data...', end='\r')
for i in range(len(raw.Date)):
    raw.Date[i] = int(str(raw.Date[i]).replace('/', '').replace('-', '').replace('Jan', '01').replace('Feb', '02').replace('Mar', '03').replace('Apr', '04').replace('May', '05').replace('Jun', '06').replace('Jul', '07').replace('Aug', '08').replace('Sep', '09').replace('Oct', '10').replace('Nov', '11').replace('Dec', '12')[:-8])

print('                     ')

raw_np = [list(a) for a in zip(
    raw.Date.values,
    raw['High'].shift(-1).values,
    raw['High'].shift(-2).values,
    raw['High'].shift(-3).values,
    raw['High'].shift(-4).values,
    raw['High'].shift(-5).values,
    raw['High'].shift(-6).values, 
    raw['High'].shift(-7).values,
    raw['High'].shift(-8).values,
    raw['High'].shift(-9).values,
    raw['High'].shift(-10).values,
    raw['High'].shift(-11).values,
    raw['High'].shift(-12).values,
    raw['High'].shift(-13).values,
    raw['High'].shift(-14).values,
    raw['High'].shift(-15).values,
    raw['High'].shift(-16).values,
    raw['High'].shift(-17).values,
    raw['High'].shift(-18).values,
    raw['High'].shift(-19).values,
    raw['High'].shift(-20).values,
    raw['High'].shift(-21).values,
    raw['High'].shift(-22).values,
    raw['High'].shift(-23).values,
    raw['High'].shift(-24).values,
    raw['High'].shift(-25).values,
    raw['High'].shift(-26).values,
    raw['High'].shift(-27).values,
    raw['High'].shift(-28).values,
    raw['High'].shift(-29).values,
    raw['High'].shift(-30).values,
    raw['High'].shift(-31).values,
    raw['High'].shift(-32).values,
    raw['High'].shift(-33).values,
    raw['High'].shift(-34).values,
    raw['High'].shift(-35).values,
    raw['High'].shift(-36).values,
    raw['High'].shift(-37).values, 
    raw['High'].shift(-38).values,
    raw['High'].shift(-39).values,
    raw['High'].shift(-40).values,
    raw['High'].shift(-41).values,
    raw['High'].shift(-42).values,
    raw['High'].shift(-43).values,
    raw['High'].shift(-44).values,
    raw['High'].shift(-45).values,
    raw['High'].shift(-46).values,
    raw['High'].shift(-47).values,
    raw['High'].shift(-48).values,
    raw['High'].shift(-49).values,
    raw['High'].shift(-50).values,
    raw['High'].shift(-51).values,
    raw['High'].shift(-52).values,
    raw['High'].shift(-53).values,
    raw['High'].shift(-54).values,
    raw['High'].shift(-55).values,
    raw['High'].shift(-56).values,
    raw['High'].shift(-57).values,
    raw['High'].shift(-58).values,
    raw['High'].shift(-59).values,
    raw['High'].shift(-50).values,
    )]

X = ~np.isnan(np.array(raw_np).astype(np.float))

y_high = np.array(raw['High']).reshape(-1, 1)#[:-50, :]
y_low = np.array(raw['Low']).reshape(-1, 1)#[:-50, :]

X, y_high, y_low = shuffle(X, y_high, y_low)

scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)


# high_model = Sequential([
#     Dense(128, activation='relu', input_shape=(61,)),
#     Dense(128, activation='relu'),
#     Dense(256, activation='relu'),
#     Dense(256, activation='relu'),
#     Dense(128, activation='relu'),
#     Dropout(0.1),
#     Dense(1, activation='relu')
# ])

high_model = Sequential([
    GRU(50, activation='relu'),
    Dense(25, activation='relu'),
    Dense(1, activation='relu')
])

high_model.compile(optimizer=Adam(lr=1e-3, decay=1e-4),
                   loss='mean_absolute_error',
                   metrics=['accuracy'])

high_model.save('Models/HighModel.h5')

history = high_model.fit(X, y_high,
                         batch_size=512,
                         epochs=40,
                         verbose=1,
                         validation_split=0.2)

plt.title('Graph Showing Loss Compared to Epochs')
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()

plt.title('Graph Showing Predictions Compared to Reality on Training Data')
plt.plot(high_model.predict(X), label='Predictions')
plt.plot(raw.High, label='Reality')
plt.legend()
plt.show()