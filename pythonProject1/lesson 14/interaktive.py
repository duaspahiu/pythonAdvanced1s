import plotly.express as px
import  pandas as pd
import matplotlib.pyplot as pit

df = pd.read_csv("data1.csv")

df['Population - 2023'] = df['Population - 2023'].str.replace(",",'').astype(float)


fig = px.scatter_geo(df,locations='Country',
                     locationmode='country names',
                     hover_name='Country',
                     size="Average IQ",
                     color="Continent",
                     projection="natural earth",
                     title="Average IQ",
                     size_max=20,
                     template='plotly_dark')

fig.show()