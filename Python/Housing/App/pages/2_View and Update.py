import streamlit as st
import pandas as pd
import pyodbc

def update(edited_df,df):
    df_merge    = pd.merge(df, edited_df, how='left', left_on='ID', right_on='ID')
    
    df_merge.to_csv('test.csv', index = False)


    #insert new data into the table
    # df_insert   = df_merge[ pd.isna(df_merge['existing_id']) ]

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
    'ID': None
}

edited_df = st.data_editor(df, column_config = column_config, num_rows = 'dynamic')


st.markdown(f'You are viewing {len(edited_df)} rows')

if st.button('save'):
    update(df,edited_df)
    st.write('SAVED!')