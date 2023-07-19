import streamlit as st
import pandas as pd
import numpy as np
import time
import pyodbc

def update(df, conn):    
    #updating data
    update_stmt = f'''
    UPDATE {st.secrets["TABLE"]}
    SET
       [HouseName]          = ?
       ,[Description]       = ?
       ,[OnMarketDate]      = ?
       ,[SoldDate]          = ?
       ,[InitialPrice]      = ?
       ,[SoldPrice]         = ?
    WHERE
        [ID]                = ?
    '''
    cur = conn.cursor()
    cur.fast_executemany = True
    cur.executemany(update_stmt, df.values.tolist())
    conn.commit()

#this page config section must always be the first sction of streamlit code
PAGE_TITLE = 'View and Update Data'
PAGE_ICON = '🗄️'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout = 'wide')

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        f"""DRIVER={st.secrets["DRIVER"]};
        SERVER= {st.secrets["SERVER"]};
        DATABASE={st.secrets["DATABASE"]};
        Trusted_Connection=yes;"""
    )

conn = init_connection()

df = pd.read_sql(f'SELECT * FROM {st.secrets["TABLE"]}', con=conn)

edited_df = st.data_editor(df)

if st.button('Save'):
    message = st.empty() #creates a placeholder for message
    message.text('Saving. Please Wait.') #replaces message with new message
    update(edited_df, conn)
    message.text('SAVED!')
    time.sleep(3) #wait 3 seconds before clear message
    message.empty() #clears message object