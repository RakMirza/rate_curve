# Web scraping pkgs
from bs4 import  BeautifulSoup
import requests
#  Core Pkgs
import streamlit as st 
from PIL import Image
import time
# Data viz paks
import matplotlib.pyplot as plt 
import matplotlib
import seaborn as sns

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



img = Image.open("trea_pic.png")
st.image(img, width=700, output_format="PNG")
st.subheader("Daily Treasury Yield Curve Rates")
st.write(data)

st.subheader(" Yield Curve Rates Visualization")
select = ['Notes','Bills','Bond']
columns = st.multiselect(label='Choose Bills, Notes or Bonds  to display current rate', options=select, default=select)
if  'Notes' in columns:
    sns.set_theme(style="whitegrid")
    fig1, ax1 = plt.subplots()    
    fig1 = plt.figure(figsize=(20, 8))
    ax1 = sns.lineplot(data=data, x='Date', y='1 mo')
    st.pyplot(fig1)

if  'Bills' in columns:
    sns.set_theme(style="whitegrid")
    fig2, ax2 = plt.subplots()    
    fig2 = plt.figure(figsize=(20, 8))
    ax2= sns.lineplot(data=data, x='Date', y='2 yr')
    st.pyplot(fig2)
    
if 'Bond' in columns:
    sns.set_theme(style="whitegrid")
    fig3, ax3 = plt.subplots()    
    fig3 = plt.figure(figsize=(20, 8))
    ax3= sns.lineplot(data=data, x='Date', y='30 yr')
    st.pyplot(fig3)

    

     

    










                


