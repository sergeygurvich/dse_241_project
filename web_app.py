# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('grouped.csv')
# df_ = px.data.gapminder().query("year==2007")
fig = px.scatter_geo(df, lat='lat',lon='lon',
                     hover_name="unit", size="count",
                     scope='usa',
                     center={'lat':37.16611, 'lon':-119.44944},
                     # fitbounds='locations',
                     # animation_group="year",
                     animation_frame="year",
                     color_continuous_scale=px.colors.cyclical.IceFire,
                     color='count'
                     )
fig.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Green",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Orange"
)
fig.update_geos(fitbounds="locations")
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon': -73, 'lat': 46 },
        'zoom': 5},
    showlegend = False)

fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children=[
    html.H1(children='California Wildfires Analysis'),

    html.Div(children='Wildfires Geography Visualization'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)