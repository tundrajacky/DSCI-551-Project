import numpy as np
import pandas as pd
import json
import requests as rq

def userUpload(zipcode,date,ctype):
    data = {'Zip_Codes': zipcode, 'Days_of_Mon': date, 'Crimes': ctype}
    json_obj = json.dumps(data, indent = 4)
    resp = rq.post('https://safety-la-apr-default-rtdb.firebaseio.com/upload.json', data=json_obj)
    return resp

def crimetypes():
    df = pd.read_csv('safetyLA_Apr.csv')
    return df['Crimes'].unique()

def getCases(area, number):
    js = rq.get('https://safety-la-apr-default-rtdb.firebaseio.com/cases.json?orderBy="Areas"&equalTo="'+ area + '"').json()
    df = pd.DataFrame.from_dict(js)
    df = df.transpose()
    df = df.loc[:, df.columns!='Areas']
    df = df.set_index('Case_No')
    df = df.sort_values(by=['Days_of_Mon'],ascending=False)
    return df.head(number)

def getArea(zipcode):
    js = rq.get('https://safety-la-apr-default-rtdb.firebaseio.com/cases/.json?orderBy="Zip_Codes"&equalTo="'+ zipcode +'"&limitToLast=1').json()
    if js is None:
        return None
    else:
        for key in js.keys():
            return js.get(key).get('Areas')

def getIndex(area):
    js = rq.get('https://safety-la-apr-default-rtdb.firebaseio.com/areas.json?orderBy="Areas"&equalTo="'+ area + '"').json()
    df = pd.DataFrame.from_dict(js)
    df = df.transpose()
    return int(df.iat[0,2])

def getAreaStats(area):
    js = rq.get('https://safety-la-apr-default-rtdb.firebaseio.com/areas.json?orderBy="Areas"&equalTo="'+ area + '"').json()
    df = pd.DataFrame.from_dict(js)
    df = df.transpose()
    numbers = df.iat[0, 1]
    data = {'Light Crime': numbers[0], 'Medium Crime': numbers[1], 'Severe Crime': numbers[2]}
    stats = pd.DataFrame(data, index=[0])
    return stats

def overview():
    plot_area = pd.read_csv('area_summary.csv',names = ['Area','Crime_class','Count'],skiprows = 1)
    plot_area = plot_area.pivot_table('Count', ['Area'], 'Crime_class')
    return plot_area
