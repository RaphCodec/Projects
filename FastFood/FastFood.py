import pandas as pd
import tomli
import plotly_express as px
import sys

pd.set_option('display.max_rows', None)

with open('FastFood.config.toml', mode='rb') as fp:
    config = tomli.load(fp)

SRC_FILE = config['SRC_FILE']

df = pd.read_csv(SRC_FILE)
print(len(df))

'''['Company', 'Category', 'Product', 'Per Serve Size', 'Energy (kCal)',
       'Carbohydrates (g)', 'Protein (g)', 'Fiber (g)', 'Sugar (g)',
       'Total Fat (g)', 'Saturated Fat (g)', 'Trans Fat (g)',
       'Cholesterol (mg)', 'Sodium (mg)']'''

# frames = [df['Product'],df[['Protein (g)', 'Fiber (g)', 'Sugar (g)']]]
# res = pd.concat(frames, keys=['Protein', 'Fiber', 'Sugar']).reset_index()
# print(df['Fiber (g)'].head(25))
# print(res.head(25))

#unpivotting some columns
df1 = pd.melt(df, id_vars=['Company','Product'], value_vars=['Protein (g)', 'Fiber (g)'])
print(df1)

fig = px.bar(
    df1,
    x='Company',
    y='value',
    color = 'variable',
    barmode = 'stack'
)
fig.show()



sys.exit()
fig = px.bar(df1.pivot(columns='Company',
    values='value').sum(),
    title='Protein Per Company',).update_layout(
    xaxis_title="Company",
    yaxis_title="Amount Protein (g)",
    barmode = 'overlay',
    color='variable', 
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)').update_xaxes(showgrid=False).update_yaxes(showgrid=False)
fig.show()

