import streamlit as st
import pandas as pd
import pyodbc
import shortuuid

def init_connection():
    return pyodbc.connect(
        f"""DRIVER={st.secrets["DRIVER"]};
        SERVER= {st.secrets["SERVER"]};
        DATABASE={st.secrets["DATABASE"]};
        Trusted_Connection=yes;"""
    )


def insert(df):
    #Changing Nulls to None so that They insert properly on the SQL SERVER end
    df = df.astype(object).where(pd.notnull(df), None)
    insert_stmt = f'''
    INSERT INTO {st.secrets["TABLE"]}(
       [ID]
       ,[HouseName]
       ,[Description]
       ,[OnMarketDate]
       ,[InitialPrice]
       ,[SoldDate]
       ,[SoldPrice] 
    )
    Values(
            {('?,' * len(df.columns))[:-1]}
        )
    '''
    conn = init_connection()
    cur = conn.cursor()
    cur.executemany(insert_stmt, df.values.tolist())
    conn.commit()


PAGE_TITLE = 'Insert New Data'
PAGE_ICON = ':smile:'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON)




with st.form("my_form"):
   st.write("Insert Housing Data")
   Name = st.text_input('Enter House Name', max_chars = 100)
   description = st.text_area('Enter a description', max_chars = 2000)
   OnMarketDate = st.date_input('Enter the Date the house was put on the market')
   InitialPrice = st.number_input('Asking Price', min_value = 0.00)
   SoldDate = st.date_input('When was the house sold?')
   SoldPrice = st.number_input('Sold Price', min_value = 0.00)

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write('Inserting the follwoing data:')
       data = {
           'ID':shortuuid.ShortUUID().random(length=4),
           'HouseName':Name,
           'Description':description,
           'MarketDate':OnMarketDate,
           'InitPrice':[InitialPrice],
           'SoldDate':SoldDate,
           'SoldPrice':[SoldPrice]
       }
       df = pd.DataFrame(data = data)
       st.write(df)
       insert(df)
       st.write('Data Inserted')