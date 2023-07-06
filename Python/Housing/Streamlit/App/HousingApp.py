import streamlit as st
import pandas as pd
import platform
import pyodbc
import plotly.express as px

def update(edited_df,df):
    df_merge    = pd.merge(df, edited_df, how='left', left_on='ID', right_on='ID')
    
    df_merge.to_csv('test.csv', index = False)


    #insert new data into the table
    # df_insert   = df_merge[ pd.isna(df_merge['existing_id']) ]

#this pae config section must always be the first sction of code
PAGE_TITLE = 'Housing Project | Raphael Clifton'
PAGE_ICON = ':house:'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout = 'wide')

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        f"""DRIVER={st.secrets["DRIVER"]};
        SERVER= {st.secrets["SERVER"]};
        DATABASE={st.secrets["DATABASE"]};
        Trusted_Connection=yes;"""
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# rows = run_query("SELECT * from HousingData;")

df = pd.read_sql(f'SELECT * FROM {st.secrets["TABLE"]}', con=conn)

st.title('Housing Data')
st.subheader('By Raphael Clifton')
st.write('This is a project that analyzes dummy housing data, using streamlit.  The purpose is to examine the functionality of strealit')

col1, col2, col3 = st.columns(3)
col1.metric(label = 'Averge Initial Price', value = f'${round(df.InitialPrice.mean(),2)}')
col2.metric(label = 'Number Of Hosues Sold', value = f'{df["SoldDate"].isnull().sum()}/{len(df)}')

init_df = df[['OnMarketDate','InitialPrice']].groupby('OnMarketDate')['InitialPrice'].mean().reset_index()

fig = px.line(init_df,
              x = 'OnMarketDate',
              y = 'InitialPrice',
              title='Average Asking Price Over Time').update_layout(
              xaxis_title="Date",
              yaxis_title="Price"
              )

st.write(fig)
