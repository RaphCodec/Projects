import streamlit as st
import pandas as pd
import numpy as np
import time
import pyodbc
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode

def update(df, conn):
    #correcting datatypes returned from AgGrid
    df[['OnMarketDate','SoldDate']] = pd.to_datetime(df[['OnMarketDate','SoldDate']].stack(), errors='coerce').unstack()
    df[['InitialPrice','SoldPrice']] = df[['InitialPrice','SoldPrice']].apply(pd.to_numeric, errors ='coerce')

    #Changing Nulls to None so that They update properly on the SQL SERVER end
    df = df.astype(object).where(pd.notnull(df), None)
    
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

gb = GridOptionsBuilder() #used to define gridOptions dictionary

# makes columns resizable, sortable and filterable by default
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=True,
    theme='streamlit',
    groupable=True,
    value=True,
    enableRowGroup=True,
    aggFunc='sum',
    rowDrag = True,
    enablePivot = True,
)

gb.configure_column(
    field="HouseName",
    header_name="Name",
    flex=1,
    tooltipField="Name",
)

gb.configure_column(
    field="Description",
    header_name="Description",
    flex=1,
    tooltipField="Description",
    aggFunc = 'count',
)

gb.configure_column(
    field="OnMarketDate",
    header_name="On Market Date",
    flex=1,
    type=["customDateTimeFormat"],
    custom_format_string='yyyy-MM-dd')

gb.configure_column(
    field="InitialPrice",
    header_name="Initial Price",
    flex=1,
    type=["numericColumn"],
    aggFunc = 'sum'
)

gb.configure_column(
    field="SoldDate",
    header_name="Sold Date",
    flex=1,
    type=["customDateTimeFormat"],
    custom_format_string='yyyy-MM-dd'
)

gb.configure_column(
    field="SoldPrice",
    header_name="Sold Price",
    flex=1,
    type=["numericColumn"],
)

gb.configure_side_bar()
gb.configure_selection(selection_mode = 'multiple')

#makes tooltip appear instantly
gb.configure_grid_options(tooltipShowDelay=0)
go = gb.build()

grid_return = AgGrid(df, gridOptions=go, height = 800)

if st.button('Save'):
    message = st.empty() #creates a placeholder for message
    message.text('Saving. Please Wait.') #replaces message with new message
    edited_df = grid_return['data']
    update(edited_df, conn)
    message.text('SAVED!')
    time.sleep(3) #wait 3 seconds before clear message
    message.empty() #clears message object