# The Instruction of this package: https://requests-html.kennethreitz.org/
from requests_html import HTMLSession
import pandas as pd
import datetime
import plotly
import plotly.graph_objs as go
import numpy as np
import time

# Define Stock set
portfolio = {'VIVE': [2020,8,25],
             'MICT': [2020,8,18],
             'APM': [2020,9,29],
             'WWR': [2020,10,6],
             'CCNC': [2020,10,19],
             'TTNP': [2020,10,28],
             'GTEC': [2020,11,10],
             'IMAC': [2020,11,12],
             'ATHE': [2020,11,16],
             'CBAT': [2020,11,16],
             'CNET': [2020,12,9],
             'FRAN': [2020,12,9]}
name = ['VIVE','MICT','APM','WWR','CCNC','TTNP','GTEC','IMAC','ATHE','CBAT','CNET','FRAN']

# Generate stock introday data.
def get_data(ticker, interval, current):
    # Connect Website
    sl = 'year1month'+str(current)
    link = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+ticker+'&interval='+interval+'&slice='+sl+'&apikey=ETP1VJQNQ6KUPF5N&adjusted=false'
    session = HTMLSession()
    r = session.get(link)
    
    # Grabe Data
    temp = r.text
    temp = temp.split('\r\n')
    gg = []
    for each in temp:
        gg.append(each.split(','))
    data = pd.DataFrame(gg)
    data = data.rename(columns={0: "time", 1: "open", 2: "high", 3:"low", 4:"close", 5:"volume"})
    data = data.dropna()
    data = data.drop(0)
    data.index = range(len(data))
    
    # transfer str to datatime.
    trans = []
    day = []
    month = []
    year = []
    hour = []
    mins = []
    pre = []
    for each in data['time']:
        o = datetime.datetime.strptime(each, '%Y-%m-%d %H:%M:%S')
        trans.append(o)
        day.append(o.day)
        month.append(o.month)
        year.append(o.year)
        hour.append(o.hour)
        mins.append(o.minute)
        pre.append(o.hour*100 + o.minute)
    data['time'] = trans
    data['day'] = day
    data['month'] = month
    data['year'] = year
    data['hour'] = hour
    data['min'] = mins
    data['pre'] = pre
    
    #data = data[(data['day'] == portfolio[ticker][2]) & (data['month'] == portfolio[ticker][1]) & (data['year'] == portfolio[ticker][0])]
    return data

data1 = get_data(ticker = 'GME', interval = '60min', current = 1)

