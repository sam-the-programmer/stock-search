print('\nImporting dependencies...', end='\r')
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

random_state = 200

print('Parsing data...          ', end='\r')
raw = pd.read_csv('Data/FTSE Full.csv')
plt.plot(raw['High Price'])
plt.plot(raw['Low Price'])
plt.show()


print('Preprocessing data...', end='\r')
for i in range(len(raw.Date)):
    raw.Date[i] = int(str(raw.Date[i]).replace('/', '').replace('-', '').replace('Jan', '01').replace('Feb', '02').replace('Mar', '03').replace('Apr', '04').replace('May', '05').replace('Jun', '06').replace('Jul', '07').replace('Aug', '08').replace('Sep', '09').replace('Oct', '10').replace('Nov', '11').replace('Dec', '12'))

X = np.array(raw.Date).reshape(-1, 1)

y_high = np.array(raw['High Price']).reshape(-1, 1)
y_low = np.array(raw['Low Price']).reshape(-1, 1)

print('Training models...   ', end='\r')
high_model = RandomForestRegressor(random_state=random_state)
high_model.fit(X, y_high)

low_model = RandomForestRegressor(random_state=random_state)
low_model.fit(X, y_low)

print('Predicting data...   ', end='\r')
high_preds = high_model.predict(X)
high_mae = mean_absolute_error(y_high, high_preds)

low_preds = low_model.predict(X)
low_mae = mean_absolute_error(y_low, low_preds)

print('Model training and predictions complete!')
plt.title('High Accuracy')
plt.scatter(range(len(y_high)), y_high)
plt.scatter(range(len(high_preds)), high_preds)
plt.show()

plt.title('Low Accuracy')
plt.scatter(range(len(y_low)), y_low)
plt.scatter(range(len(low_preds)), low_preds)
plt.show()

plt.title('High Predictions Compared with Data')
plt.plot(high_preds, color='g')
plt.plot(raw['High Price'], color='r')
plt.show()

plt.title('Low Predictions Compared with Data')
plt.plot(low_preds, color='g')
plt.plot(raw['Low Price'], color='r')
plt.show()