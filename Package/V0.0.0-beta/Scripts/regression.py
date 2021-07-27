import numpy as np
import pandas as pd
import streamlit as st
import warnings
import yfinance as yf

warnings.filterwarnings('ignore')

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor



def preprocess_data(data: pd.DataFrame, column: str, shifts: int, valid_split=0.2):
    to_shift = []
    for i in range(shifts):
        to_shift.append(data[column].shift(-i-1).values)
    
    raw_x = pd.DataFrame([list(a) for a in zip(*to_shift)], index=data.index).dropna()

    X_train = raw_x.iloc[: len(raw_x)-int(len(raw_x)*valid_split)]
    X_valid = raw_x.iloc[len(raw_x)-int(len(raw_x)*valid_split) :]
    y_train = data[column].iloc[: len(raw_x)-int(len(raw_x)*valid_split)]
    diff = len(data[column].iloc[len(raw_x)-int(len(raw_x)*valid_split) :-int(shifts/2)]) - len(X_valid)
    
    y_valid = data[column].iloc[len(raw_x)-int(len(raw_x)*valid_split) :-int(shifts/2 + diff)]
    
    try:
        assert len(X_train) == len(y_train)
        assert len(X_valid) == len(y_valid)
    except:
        print('                       ')
        print(f'X train {len(X_train)}')
        print(f'y train {len(y_train)}')
        print(f'X valid {len(X_valid)}')
        print(f'y valid {len(y_valid)}')
        print('                       ')
        exit()
    
    return X_train.astype(np.float), X_valid.astype(np.float), y_train.astype(np.float), y_valid.astype(np.float)

def shift_data(data: pd.DataFrame, column: str, shifts:int):
    to_shift = []
    for i in range(shifts):
        to_shift.append(data[column].shift(-i-1).values)
    
    return pd.DataFrame([list(a) for a in zip(*to_shift)], index=data.index).dropna()

@st.cache(show_spinner=False, allow_output_mutation=True)
def get_best_preds(raw, column, days):
    
    ada_reg = AdaBoostRegressor(random_state=1)
    lin_reg = LinearRegression()
    rid_reg = Ridge(random_state=1)
    dec_tree = DecisionTreeRegressor(random_state=1)
    extr_tree = ExtraTreeRegressor(random_state=1)
    rand_tree = RandomForestRegressor(random_state=1)
    grad_reg = GradientBoostingRegressor(random_state=1)
    
    
    X_train, X_valid, y_train, y_valid = preprocess_data(raw, column, days)
    
    ada_reg.fit(X_train, y_train)
    
    lin_reg.fit(X_train, y_train)
    
    rid_reg.fit(X_train, y_train)
    
    dec_tree.fit(X_train, y_train)
    
    extr_tree.fit(X_train, y_train)
    
    rand_tree.fit(X_train, y_train)
    
    grad_reg.fit(X_train, y_train)
    
    int_preds = [
        ada_reg.predict(X_valid),
        lin_reg.predict(X_valid),
        rid_reg.predict(X_valid),
        dec_tree.predict(X_valid),
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
        'Ridge Regressor',
        'Decision Tree Regressor',
        'Extra Tree Regressor',
        'Random Forest Regressor',
        'Gradient Boosting Regressor'
    ]
    
    
    for i in range(len(preds)):
        errors.append(round(mean_absolute_error(y_valid[1:], preds[i]), 2))
    
    X_train = shift_data(raw, column, days)
    y_train = pd.DataFrame(raw[column], index=X_train.index)

    ada_reg.fit(X_train, y_train)
    
    lin_reg.fit(X_train, y_train)
    
    rid_reg.fit(X_train, y_train)
    
    dec_tree.fit(X_train, y_train)
    
    extr_tree.fit(X_train, y_train)
    
    rand_tree.fit(X_train, y_train)
    
    grad_reg.fit(X_train, y_train)
    
    prediction_frame = pd.DataFrame(index=range(1, days+1))
    
    negative = days
    preds = [
        ada_reg.predict(X_train.iloc[-negative:]),
        lin_reg.predict(X_train.iloc[-negative:]),
        rid_reg.predict(X_train.iloc[-negative:]),
        dec_tree.predict(X_train.iloc[-negative:]),
        extr_tree.predict(X_train.iloc[-negative:]),
        rand_tree.predict(X_train.iloc[-negative:]),
        grad_reg.predict(X_train.iloc[-negative:])
        ]
    
    for i in range(len(preds)):
        prediction_frame[models[i]] = preds[i]
    
    return prediction_frame, errors, X_train
    


def get_preds_wrapper(data, column):
    st.markdown("""
<br/>
<br/>
<hr/>
    
## Predictions
    
View the predictions on a graph, starting from the end of the current data.
    
<br/>
<style>
div.stButton > button:first-child {
background-color: #f63566;
color:white;
font-size:20px;
height:2em;
width:18em;
border-radius:10px 10px 10px 10px;
}</style>""", unsafe_allow_html=True)
    
    models = [
        'Adaboost Regressor',
        'Linear Regressor',
        'Ridge Regressor',
        'Decision Tree Regressor',
        'Extra Tree Regressor',
        'Random Forest Regressor',
        'Gradient Boosting Regressor'
    ]
    
    col1, col2 = st.beta_columns([2.5, 1])
    left_col = col1.beta_container()
    right_col = col2.beta_container()
    
    num_days = right_col.slider('Forecast Days', 50, 100, help='Higher periods can result in longer training times. New data is appended, but may be less visible for smaller forecast days. Predictions may degrade over longer forecast lengths.')

    space = left_col.empty()
    
    if right_col.button('Get Predictions'):
        space.info('Training models - please wait, this could take some time...')
        preds, errors, tail = get_best_preds(data, column, num_days)
        st.write(tail)
    
    
    right_col.write('''
The **Error Rating** for the algorithms is not in a specified unit, scale varies between datasets and should only be used to compare models. Higher values indicate higher error margins.
''')

    
    raw_data_display = st.beta_expander('Raw Prediction Data', expanded=True)
    stats = st.beta_expander('Model Performance')
    
    
    
    if 'preds' in locals():
        # algorithms = right_col.multiselect('Choose algorithms:', ['Recommended', 'All', *models], help='Choose which algorithm\'s predictions to display in the graph.')
        
        table_place = right_col.empty()
        
        lowest_value = np.inf
        lowest_index = 0
        for i in range(len(errors)):
            if errors[i] > lowest_value:
                lowest_value = errors[i]
                lowest_index = i
        
        graphs = space.beta_container()
        
        table_place.table(pd.DataFrame(errors, index=models, columns=['Error Rating']))
        stat_contain = stats.beta_container()
        
        graphs.write('### Recommended Model')
        graphs.line_chart(preds.iloc(axis=1)['Recommended'], height=400)
        
        graphs.write('### All Models')
        graphs.line_chart(preds, height=400)
        
        
        if 'Mean' in preds.columns: preds.pop('Mean')
        if 'Recommended' in preds.columns: preds.pop('Recommended')
        
        preds.insert(0, 'Recommended', value=preds.iloc(axis=1)[lowest_index])
        preds.insert(0, 'Mean', value=preds.mean(axis=1))
        raw_data_display.write(preds)
        stat_contain.write(tail)
        stat_contain.write('Below is a bar chart of the model performance. Lower values means less error and higher accuracy, so look for the algorithms with the lowest values.')
        performance_chart = stat_contain.bar_chart(pd.DataFrame(errors, index=models), height=400)
        
    else:
        # algorithms = right_col.multiselect('Choose algorithms:', ['Recommended', 'All', *models], help='Choose which algorithm\'s predictions to display in the graph.')
    
        # if right_col.button('Update Graph'):
        #     space.line_chart(pd.DataFrame(np.zeros(shape=1), columns=['No Data Generated Yet']), height=400)
        table_place = right_col.empty()
        raw_data_display.info('No predictions generated yet')
        table_place.table(pd.DataFrame([['Untrained']], index=[models], columns=['Mean Error Rating']))
        space.line_chart(pd.DataFrame(np.zeros(shape=1), columns=['No Data Generated Yet']), height=400)
        stats.info('No predictions generated yet.')


if __name__ == '__main__':
    get_best_preds(yf.download('^FTSE', period='10y'), 'Open', 100)