import streamlit as st
import pandas as pd
import pyodbc

def update(df, conn):
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
    cur.executemany(update_stmt, df.values.tolist())
    conn.commit()

#this pae config section must always be the first sction of code
PAGE_TITLE = 'View and Update Data'
PAGE_ICON = ':smile:'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON)

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

column_config = {
    'ID': None,
    'OnMarketDate':st.column_config.DateColumn(
            "On Market Date",
            format="DD.MM.YYYY",
            step=1),
    'SoldDate':st.column_config.DateColumn(
            "Sold Date",
            format="DD.MM.YYYY",
            step=1)
}

edited_df = st.data_editor(df, column_config = column_config)


st.markdown(f'You are viewing {len(edited_df)} rows')

if st.button('Save'):
    st.write('Saving. Please Wait.')
    update(edited_df, conn)
    st.write('SAVED!')