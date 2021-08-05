import streamlit as st

import Scripts.data as data
import Scripts.regression as algo
import Scripts.settings as setting_info


class MultiPage(object):
    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        self.pages.append({
            'title': title,
            'function': func
        })

    def run(self):

        page = st.sidebar.radio(
            'App Navigation',
            self.pages,
            format_func = lambda page: page['title'],
            index = 0
        )

        page['function']()


# Formatting methods
def footer():
    st.write("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
footer :after {
	content:'Thank you for using Stock Search.'; 
	visibility: visible;
	display: block;
	position: relative;
	padding: 5px;
	top: 2px;
}
</style>
""", unsafe_allow_html=True)

    st.write('''
<br/>
<hr/>

###### All data has been aqquired from [Quandl](https://www.quandl.com/) and [Yahoo! Finance](https://finance.yahoo.com/). 

<br/>
<br/>

> #### DISCLAIMER: THIS IS JUST A VISUALIZATION OF A DATA SCIENCE PROJECT
> ##### **UNDER NO CIRCUMSTANCES SHOULD THE CREATORS, PUBLISHERS OR COPYRIGHT HOLDERS BE MADE LIABLE TO ANY CLAIM, DAMAGE, LOSS OR OTHER LIABLILITY THAT ARISES IN USE OF THE SOFTWARE, IN CONNECTION WITH THE SOFTWARE OR ANY OTHER USE, PURPOSES OR ANY OTHER DEALINGS WITH THE SOFTWARE.**
> ##### **The creator of Stock Search is by no means a financial expert of any kind; this is just a visualisation of a project. Use this data and predictions at your own risk. The models may not be accurate and have wide error margins. Furthermore, some data may not be accurate to that minute, as the data interval times vary on the dataset.**
> #### STOCK SEARCH ACTIVELY DISCOURAGES USE OF THIS DATA FOR REAL SITUATIONS.

###### The creator recommends that:

> > ##### ***Stock Search should not be used for any real financial situations. Any use is at the user's own risk.***

#### Check out the <a href='https://github.com/Password-Classified/Stock-Search/blob/master/LICENSE'>License</a> on the Github repository for more information.


<br/>

###### Thanks to Numpy, Pandas, Quandl, Yahoo! Finance, yfinance, Streamlit and Python.
''', unsafe_allow_html=True)

    # Get your free Quandl API key there too to allow for more frequent download of real time data when using Stock Share. Currently, only a few datasets are


def title_func(title_name):
    title, logo = st.beta_columns([5, 1])

    title.title(title_name)
    logo.image('https://raw.githubusercontent.com/Password-Classified/Stock-Search/master/Package/V0.0.0-beta/Images/logo.png', width=100)


# Pages
def welcome():
    st.image('https://raw.githubusercontent.com/Password-Classified/Stock-Search/master/Package/V0.0.0-beta/Images/logo.png', width=520)
    st.write(f'''
# Stock Search

<br/>
''', unsafe_allow_html=True)
    
    # if not st.checkbox('Show Welcome Screen on Startup', value=True):
    #     setting_info.set_welcome_screen(False)

    st.markdown(f'''
###### **NOTE:** By using this application, you are agreeing to the <a href='https://github.com/Password-Classified/Stock-Search/blob/master/LICENSE'>License</a>

<br/>

Welcome! Stock Search is the latest, innovative way to explore stocks and prices
throughout time, back into the past and into the future. By using detailed
machine learning models, Stock Search's free ML
tools will outline estimates for rates in the future.

Please see the disclaimer:

> #### DISCLAIMER: THIS IS JUST A VISUALIZATION OF A DATA SCIENCE PROJECT
> ##### **UNDER NO CIRCUMSTANCES SHOULD THE CREATORS, PUBLISHERS OR COPYRIGHT HOLDERS BE MADE LIABLE TO ANY CLAIM, DAMAGE, LOSS OR OTHER LIABLILITY THAT ARISES IN USE OF THE SOFTWARE, IN CONNECTION WITH THE SOFTWARE OR ANY OTHER USE, PURPOSES OR ANY OTHER DEALINGS WITH THE SOFTWARE.**
> ##### **The creator of Stock Search is by no means a financial expert of any kind; this is just a visualisation of a project. Use this data and predictions at your own risk. The models may not be accurate and have wide error margins. Furthermore, some data may not be accurate to that minute, as the data interval times vary on the dataset.**
> #### STOCK SEARCH ACTIVELY DISCOURAGES USE OF THIS DATA FOR REAL SITUATIONS.

###### The creator recommends that:

> > ##### ***Stock Search should not be used for any real financial situations. Any use is at the user's own risk.***

#### Check out the <a href='https://github.com/Password-Classified/Stock-Search/blob/master/LICENSE'>License</a> on the Github repository for more information.

<br/>
<br/>

Use the left hand side sidebar to navigate through the pages. There are currently
{len(data.datasets)} datasets you can browse and analyse, with more added every update.

With interactive graphs and data visualization, stock predictions and searching
has never been so easy. Visualize financial data, such as the Apple stocks below:
<br/>
''', unsafe_allow_html=True)
    st.area_chart(data.get_data('Stocks: Apple Inc.')['Adj Close'])
    st.write('''
Then, you can have access to machine learning algorithms that allow you to
receive AI\'s predictions of future prices and trends.

These are just ***predictions***, so should not be thought of in any way as accurate,
future-seeing or anything of the such.


<br/>
<br/>
<hr/>

### Coming Soon
 + Stock Search API for developers
 + Regular updates to the application, user interface and algorithms
 + Any necessary bug fixes, interface changes, etc.

<br/>

##### END OF ARTICLE
''', unsafe_allow_html=True)

    footer()


def all_data():
    title_func('All Data')
    st.write('##### **NOTE**: Please read the disclaimer before continuing. This can be found in the footer and the welcome page.')
    st.text('\n')

    left_col, right_col = st.beta_columns([1, 1])

    data_name = left_col.selectbox('Choose Dataset', [
                                   key for key in data.datasets], help='Choose dataset from a wide variety from Quandl.com and Yahoo! Finance.')

    data_data = data.get_data(data_name)

    data_type = right_col.selectbox('Data Type', list(
        data_data), help='Choose which column of data to display. E.g. "Value", "High" or "Low"')

    st.markdown('<br/><br/>', unsafe_allow_html=True)

    st.area_chart(data_data[data_type])

    algo.get_preds_wrapper(data_data, data_type)

    footer()


def exchange_rates_data():
    title_func('Exchange Rates Data')

    left_col, right_col = st.beta_columns([1, 1])

    data_name = left_col.selectbox('Choose Dataset', [
                                   key for key in data.exchange_rates], help='Choose dataset from a wide variety from Quandl.com and Yahoo! Finance.')

    data_data = data.get_data('Exchange Rates: ' + data_name)

    data_type = right_col.selectbox('Data Type', list(
        data_data), help='Choose which column of data to display. E.g. "Value", "High" or "Low"')

    st.markdown('<br/><br/>', unsafe_allow_html=True)

    st.area_chart(data_data[data_type])

    algo.get_preds_wrapper(data_data, data_type)

    footer()
    
def crypto_data():
    title_func('Cryptocurrency Data')

    left_col, right_col = st.beta_columns([1, 1])

    data_name = left_col.selectbox('Choose Dataset', [
                                   key for key in data.cryptos], help='Choose dataset from a wide variety from Quandl.com and Yahoo! Finance.')

    data_data = data.get_data('Cryptocurrencies: ' + data_name)

    data_type = right_col.selectbox('Data Type', list(
        data_data), help='Choose which column of data to display. E.g. "Value", "High" or "Low"')

    st.markdown('<br/><br/>', unsafe_allow_html=True)

    st.area_chart(data_data[data_type])

    algo.get_preds_wrapper(data_data, data_type)

    footer()


api_key_string = ''


def settings():
    st.write('''
## Stock Search Settings

There are currently no settings yet. Quandl API keys will be introduced in later updates.
''')
    global api_key_string
    api_key_string = 0
    # api_key_string = st.text_input(
    #     'Quandl API Key',
    #     type='password',
    #     help='Choose Quandl API key. Fill this with your API key for more data downloads per timeframe. Without API key, max is 20 downloads per 10 minutes.'
    # )

    footer()
