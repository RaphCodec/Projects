import pandas as pd
import streamlit as st
import plotly.express as px
import pygwalker as pyg
import psutil


#this page config section must always be the first sction of streamlit code
PAGE_TITLE = 'Comics Project | Raphael Clifton'
PAGE_ICON = '🧙‍♂️'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout = 'wide')

st.title(':blue[DC] vs :red[Marvel]\nStats and Analysis')

dc = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/dc-wikia-data.csv')
marvel = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/marvel-wikia-data.csv')

tab1, tab2, tab3 = st.tabs(["Graphs", "Data", "About"])

html_output = pyg.walk(dc, env='Streamlit')
tab2.dataframe(dc)
tab2.dataframe(marvel)


dcCharacterCounts = dc['ALIGN'].value_counts()

dc_blue = ['#0476F2']

dcCharacterType = px.bar(x=dcCharacterCounts.index,
                         y=dcCharacterCounts.values,
                         title = 'DC Character Types',
                         labels={'x': 'Character Type', 'y': 'Count'},
                         color_discrete_sequence = dc_blue
                         )
dcCharacterType.update_xaxes(showgrid=False).update_yaxes(showgrid=False, range = [0,8_000])

tab1.plotly_chart(dcCharacterType, sharing = 'streamlit')

marvelCharacterCounts = marvel['ALIGN'].value_counts()

marvel_red = ['#ED1D24']

marvelCharacterType = px.bar(x=marvelCharacterCounts.index,
                             y=marvelCharacterCounts.values,
                             title = 'Marvel Character Types',
                             labels={'x': 'Character Type', 'y': 'Count'},
                             color_discrete_sequence = marvel_red                             
                             )

marvelCharacterType.update_xaxes(showgrid=False).update_yaxes(showgrid=False, range = [0,8_000])


tab1.plotly_chart(marvelCharacterType, sharing = 'streamlit')