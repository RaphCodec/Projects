import pandas as pd



#this page config section must always be the first sction of streamlit code
PAGE_TITLE = 'Housing Project | Raphael Clifton'
PAGE_ICON = '🧙‍♂️'


st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout = 'wide')

dc = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/dc-wikia-data.csv')
marvel = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/marvel-wikia-data.csv')
marvel