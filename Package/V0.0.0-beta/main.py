try:
    import streamlit as st

    from Scripts.data import *
    from Scripts.pages import *
    #import Scripts.settings as settings
except:
    import Scripts.install_requirements
    import streamlit as st

    from Scripts.data import *
    from Scripts.pages import *
    #import Scripts.settings as settings

# if settings.get_new():
#     import Scripts.installer
#     exit()

st.set_page_config(
    page_title='Stock Search',
    page_icon='https://github.com/Password-Classified/Stock-Search/blob/master/Package/V0.0.0-beta/Images/logo.png',
    layout='wide')

# Pages
app = MultiPage()

# if settings.get_welcome_screen():
app.add_page('Welcome', welcome)

app.add_page('All Data', all_data)
app.add_page('Cryptocurrencies', crypto_data)
app.add_page('Exchange Rates', exchange_rates_data)
app.add_page('Settings', settings)

app.run()