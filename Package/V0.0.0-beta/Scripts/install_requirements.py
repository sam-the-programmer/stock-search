from subprocess import run
import sys

try:
    if sys.platform == 'win32':
        run('py -m pip install numpy')
        run('py -m pip install pandas')
        run('py -m pip install quandl')
        run('py -m pip install streamlit')
        run('py -m pip install yfinance')
        run('py -m pip install matplotlib')
    else:
        run('python -m pip install numpy')
        run('python -m pip install pandas')
        run('python -m pip install quandl')
        run('python -m pip install streamlit')
        run('python -m pip install yfinance')
        run('python -m pip install matplotlib')
except:
    raise ImportError('You need numpy, pandas, quandl, streamlit and yfinance to run these scripts. You also need a Python version that supports the os and subprocess modules.')