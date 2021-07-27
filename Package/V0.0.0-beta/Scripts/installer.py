import streamlit as st

st.set_page_config(
    page_title = 'Stock Search Installer',
    page_icon = 'Images/favicon.png',
    layout = 'centered')


st.image('Images/logo.png', width=400)

st.markdown('''
# Stock Search Installer

<br/>
<br/>
<hr/>

## **DISCLAIMER:** READ ALL
The algorithms cannot be precise enough to predict accurate day-to-day values,
so short-selling is not recommended. Any accuracy will be for longer time periods,
such as a few days to a few weeks, but the creator is not a financial advisor or expert
of any sort, so please don\'t take any of this as financial advice - this is simply a
data science visualization of a project. The creator recommends that:

> ***Stock Search is totally untested for any real financial situations. Any use is at the user's own risk.***

Use the predictions at your own risk, Stock Search may not be liable for anything that happens using this app,
predictions,financial losses or anything else associated with this application. By using Stock Search, you are
accepting these terms.
''', unsafe_allow_html=True)

st.markdown('''<style>
div.stButton > button:first-child {
background-color: #f63566;
color:white;
font-size:20px;
height:2em;
width:18em;
border-radius:10px 10px 10px 10px;
}</style>''', unsafe_allow_html=True)

if st.checkbox('By clicking this checkbox, you agree to the disclaimer above.'):
    if st.button('Install Stock Share'):
        with open('C:/ProgramData/Stock Search/app_data.json', 'w') as file:
                    file.write('''{
            "new": true,
            "welcome_screen": true
        }''')