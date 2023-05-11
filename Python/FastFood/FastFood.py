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

df_cats = df.groupby('Category')
gor = df_cats.get_group('GOURMET MENU')
mccafe = df_cats.get_group('McCAFE MENU')
cbb = df_cats.get_group('Cookies, Brownies & Bars')

print(mccafe)
print(df_cats.groups.keys())

df = df.replace({'Hot Breakfast':'Breakfast','BREAKFAST MENU':'Breakfast','GOURMET MENU':'Drinks'})
#print(df['Category'].value_counts())

sys.exit()

#unpivotting some columns
df1 = pd.melt(df, id_vars=['Company','Product'], value_vars=['Protein (g)', 'Fiber (g)','Sugar (g)',
                                            'Total Fat (g)', 'Saturated Fat (g)', 'Trans Fat (g)',
                                            'Cholesterol (mg)', 'Sodium (mg)'])
print(df1)

df1 = df1.groupby(['Company','variable']).mean().reset_index()





sys.exit()
fig = px.bar(
    df1,
    x='Company',
    y='value',
    color = 'variable',
    barmode = 'stack',
    title = 'Avg Nutrition'
)
fig.show()


# fig = px.bar(df1.pivot(columns='Company',
#     values='value').sum(),
#     title='Protein Per Company',
#     color= 'variable'
#     ).update_layout()
# fig.show()



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

