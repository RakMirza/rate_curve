# Web scraping pkgs
from bs4 import  BeautifulSoup
import requests
#  Core Pkgs
import streamlit as st 
import time
# Data viz paks
import matplotlib.pyplot as plt 
import matplotlib
# EDA 
import pandas as pd 
import numpy as np


@st.cache
def fetch_data():        
    url  = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield"
    req = requests.get(url)
    content = BeautifulSoup(req.text, 'lxml')
    table = content.find('table', {'class' :'t-chart'})
    headers = []
    for i in table.find_all('th'):
        title = i.text.strip()
        headers.append(title)
    df = pd.DataFrame(columns = headers)
    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        row_data = [tr.text.strip() for tr in data]
        length = len(df)
        df.loc[length] = row_data
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        new_data = df.loc[:,['1 mo', '2 mo', '3 mo', '6 mo', '1 yr', '2 yr', '3 yr', '5 yr','7 yr', '10 yr', '20 yr', '30 yr']]
        new_data= new_data.astype(np.float)
        new_data = pd.concat([df['Date'],new_data],axis= 1)
    return new_data

data = fetch_data()

st.subheader("Daily Treasury Yield Curve Rates")
st.write(data)

st.bar_chart(data.iloc[:,1:])
# define figure
fig, ax = plt.subplots(1, figsize=(16, 6))
                


