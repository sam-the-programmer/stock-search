print('\nImporting dependencies...')

import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import AdaBoostRegressor, ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor

style.use('ggplot')


def preprocess_data(data: pd.DataFrame, column: str, shifts: int, valid_split=0.2):
    to_shift = []
    for i in range(shifts):
        to_shift.append(data[column].shift(-i-1).values)
    
    raw_x = pd.DataFrame([list(a) for a in zip(*to_shift)], index=data.index).dropna()

    X_train = raw_x.iloc[: len(raw_x)-int(len(raw_x)*valid_split)]
    X_valid = raw_x.iloc[len(raw_x)-int(len(raw_x)*valid_split) :]
    y_train = data[column].iloc[: len(raw_x)-int(len(raw_x)*valid_split)]
    y_valid = data[column].iloc[len(raw_x)-int(len(raw_x)*valid_split) :-100]
    
    try:
        assert len(X_train) == len(y_train)
        assert len(X_valid) == len(y_valid)
    except AssertionError:
        print('                       ')
        print(f'X train {len(X_train)}')
        print(f'y train {len(y_train)}')
        print(f'X valid {len(X_valid)}')
        print(f'y valid {len(y_valid)}')
        print('                       ')
        exit()
    
    return X_train.astype(np.float), X_valid.astype(np.float), y_train.astype(np.float), y_valid.astype(np.float)
    


if __name__ == '__main__':
    print('Getting datasets...')
    raw = yf.download('K', period='10y', progress=False)
    # raw = pd.read_csv('Data/FTSE Index Yahoo.csv')

    X_train, X_valid, y_train, y_valid = preprocess_data(
        raw, 'Adj Close',
        100, valid_split=0.1
    )
    
    print('\nCreating models...\n')
    # linear_svr = SVR(kernel = 'linear', C = 1000.0)
    # polynomial_svr = SVR(kernel = 'poly', C = 1000.0, degree = 2)
    # rbf_svr = SVR(kernel = 'rbf', C=1000.0, gamma=0.15)
    
    ada_reg = AdaBoostRegressor(random_state=1)
    lin_reg = LinearRegression()
    
    dec_tree = DecisionTreeRegressor(random_state=1)
    extr_trees = ExtraTreesRegressor(random_state=1)
    extr_tree = ExtraTreeRegressor(random_state=1)
    rand_tree = RandomForestRegressor(random_state=1)
    
    grad_reg = GradientBoostingRegressor()
    
    print('Fitting Adaboost Regressor...')
    ada_reg.fit(X_train, y_train)
    
    print('Fitting Linear Regressor...')
    lin_reg.fit(X_train, y_train)
    
    print('Fitting Decision Tree Regressor...')
    dec_tree.fit(X_train, y_train)
    
    print('Fitting Extra Trees Regressor...')
    extr_trees.fit(X_train, y_train)
    
    print('Fitting Extra Tree Regressor...')
    extr_tree.fit(X_train, y_train)
    
    print('Fitting Random Forest...')
    rand_tree.fit(X_train, y_train)

    print('Fitting Gradient Boosting Regressor...')
    grad_reg.fit(X_train, y_train)

    '''
    print('Fitting Linear SVR...   ')
    linear_svr.fit(X_train, y_train)
    
    print('Fitting Polynomial SVR...')
    polynomial_svr.fit(X_train, y_train)
    
    print('Fitting RBF SVR...')
    rbf_svr.fit(X_train, y_train)
    '''
    
    print('Trained models!')
    
    
    
    
    print('\nValidating models...')
    plt.plot(y_valid[1:], color='b', linewidth=2.5, label='Real Data')

    print('Getting predictions...')
    int_preds = [
        ada_reg.predict(X_valid),
        lin_reg.predict(X_valid),
        dec_tree.predict(X_valid),
        extr_trees.predict(X_valid),
        extr_tree.predict(X_valid),
        rand_tree.predict(X_valid),
        
        grad_reg.predict(X_valid)
    ]
    
    preds = []
    for i in int_preds:
        df = pd.DataFrame(i, index=y_valid.index)
        preds.append(df.shift(1, fill_value=np.nan).dropna())
        
    
    
    errors = []
    models = [
        'Adaboost Regressor',
        'Linear Regressor',
        'Decision Tree Regressor',
        'Extra Trees Regressor',
        'Extra Tree Regressor',
        'Random Forest Regressor',
        'Gradient Boosting Regressor'
    ]
    
    print('Plotting predictions...\n')
    plt.plot(preds[0], label='Adaboost')
    plt.plot(preds[1], label='Linear Regression')
    plt.plot(preds[2], label='Decision Tree')
    plt.plot(preds[3], label='Extra Trees')
    plt.plot(preds[4], label='Extra Tree')
    plt.plot(preds[5], label='Random Forest')
    plt.plot(preds[6], label='Gradient Booster')
    
    # plt.plot(preds[7], label='Linear SVR')
    # plt.plot(preds[8], label='Poly SVR')
    # plt.plot(preds[9], label='RBF SVR')
    plt.legend()
    plt.show()

    for i in range(len(preds)):
        errors.append(round(mean_absolute_error(y_valid[1:], preds[i]), 2))
        
    for i in range(len(errors)): print(f'{models[i]} Error: {errors[i]}')
    
    print('\nDone!')