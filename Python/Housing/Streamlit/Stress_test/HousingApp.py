import streamlit as st
import pandas as pd
import platform
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

start = time.time()


#this page config section must always be the first sction of streamlit code
PAGE_TITLE = 'Housing Project | Raphael Clifton'
PAGE_ICON = '🏡'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout = 'wide')

# Initialize connection.
# Uses st.cache_resource to only run once.

def generate_dummy_data(num_rows):
    # Generate the main DataFrame
    descriptions = [
        '2 Story home with 2 full baths and one half bath. 2 bedrooms and 1 guest room. Open concept kitchen, with gas stove and smart refrigerator. Spacious backyard',
        '3 bedroom home. Fully furnished and carpeted. Outdoor Backyard Pool, with a depth of up to 6 feet. Large windows for ample sunlight. Property is fenced.',
        '2 family duplex. Shared backyard. Both units are furnished. Washer and dryer included in both. Easy access to transportation. 20 minutes from downtown.'
    ]

    data = {
    'HouseName': ['House ' + str(i) for i in range(1, num_rows + 1)],
    'Description': [random.choice(descriptions) for _ in range(num_rows)],
    'OnMarketDate': [(datetime(2022, 1, 1) + timedelta(days=random.randint(1, 365))).date() for _ in range(num_rows)],
    'SoldDate': [(datetime(2022, 1, 1) + timedelta(days=random.randint(1, 365))).date() if random.random() < 0.5 else None for _ in range(num_rows)],
    'InitialPrice': [round(random.uniform(100000, 500000), 2) for _ in range(num_rows)],
    'SoldPrice': [round(random.uniform(80000, 600000), 2) for _ in range(num_rows)]
    }

    df = pd.DataFrame(data)
    
    #needed to detect None/null values in the soldDate column
    df = df.astype(object).where(pd.notnull(df), None)
    #changing SoldPrice to none where SoldDate is None
    for idx,date in enumerate(df['SoldDate']):
        if date == None:
            df.at[idx, 'SoldPrice'] = None
    
    return df

df = generate_dummy_data(1_000_000)

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

st.write(f'Time to load {time.time() - start} seconds')
