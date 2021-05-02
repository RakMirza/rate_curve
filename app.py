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
import plotly.express as px

# EDA 
import pandas as pd 
import numpy as np


@st.cache
def fetch_data():        
    # data scrapping
    
    url  = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield"
    req = requests.get(url)
    content = BeautifulSoup(req.text, 'lxml')
    table = content.find('table', {'class' :'t-chart'})
    headers = [] 
    
    for i in table.find_all('th'):
        title = i.text.strip()
        headers.append(title)        
    # converting string from bs4 to dataframe    
    df = pd.DataFrame(columns= headers)
        
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
st.title("Daily Treasury Real Yield Curve Rates")
img = Image.open("pic_dollar.jpeg")
st.image(img, width=700, output_format="PNG")

if st.checkbox("View_data"):
    st.subheader("Current Yield Curve Rates")
    st.write(data)  

st.subheader(" Yield Curve Rates Visualization")

if st.checkbox("Visulaization"):    
    fig = px.line(data, x="Date", y=data.keys(),
                        hover_data={'Date': "|%B %d"},
                    template="simple_white")
    fig.update_xaxes(
        dtick="Date",
        visible=True, fixedrange=False)
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        font_family="Rockwell",
        )          
    st.plotly_chart(fig) 

select = ['Notes','Bills','Bond']
columns = st.multiselect(label='Choose Bills, Notes or Bonds  to display current rate in detail', options=select)

if  'Bills' in columns:
    fig1= px.bar(data, x="Date", y=["1 mo", "2 mo", "3 mo","6 mo", "1 yr"], facet_col="variable", color="value")
    st.plotly_chart(fig1)

if  'Notes' in columns:
    fig2 = px.bar(data, x="Date", y=["2 yr", "3 yr", "5 yr","7 yr", "10 yr"], facet_col="variable", color="value")
    st.plotly_chart(fig2)
    
if 'Bond' in columns:
    fig3 = px.bar(data, x="Date", y=["20 yr",'30 yr'], facet_col="variable", color="value")
    st.plotly_chart(fig3)
    
    
    
    
    
    



























                


