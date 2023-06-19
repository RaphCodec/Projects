import streamlit as st
import pandas as pd
import sqlite3
import platform


conn = sqlite3.connect('HousingData.db')

df = pd.read_sql('SELECT * FROM HousingData', con=conn)

PAGE_TITLE = 'Housing Project | Raphael Clifton'
PAGE_ICON = ':house:'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON)


st.title('Housing Data')
st.subheader('By Raphael Clifton')
st.write('This is a project that analyzes dummy housing data, using streamlit.  The purpose is to examine the functionality of strealit')


col1, col2, col3 = st.columns(3)
col1.metric(label = 'Averge Initial Price', value = f'${round(df.InitialPrice.mean(),2)}')
col2.metric(label = 'Averge Sold Price', value = f'${round(df.SoldPrice.mean(),2)}')
col1.metric(label = 'Averge Difference', value = f'${round(df.InitialPrice.mean() - df.SoldPrice.mean(),2)}')


edited_df = st.data_editor(df)

st.markdown(f'there are {len(edited_df)} rows')

with st.sidebar:
    st.write(platform.system(),
             'process', platform.processor(),
             '\n', platform.machine()
             )