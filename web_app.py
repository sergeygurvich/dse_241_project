# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__)


# MAP

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_map = pd.read_csv('wildfires_grouped_task1.csv')
# df_ = px.data.gapminder().query("year==2007")
fig_map = px.scatter_geo(df_map, lat='lat',lon='lon',
                     hover_name="unit", size="count",
                     scope='usa',
                     center={'lat':37.16611, 'lon':-119.44944},
                     # fitbounds='locations',
                     # animation_group="year",
                     animation_frame="year",
                     color_continuous_scale=px.colors.cyclical.IceFire,
                     color='count'
                     )
fig_map.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Green",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Orange"
)
fig_map.update_geos(fitbounds="locations")
fig_map.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig_map.update_layout(
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon': -73, 'lat': 46 },
        'zoom': 5},
    showlegend = False)

fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})




# TRENDS

df_grouped = pd.read_csv('wildfires_grouped_task2_2.csv')


# Create figure with secondary y-axis
fig_trends = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig_trends.add_trace(
    go.Scatter(x=df_grouped['year'].astype(str), y=df_grouped['count'], name="wildfires count"),
    secondary_y=False,
)

fig_trends.add_trace(
    go.Scatter(x=df_grouped['year'].astype(str), y=df_grouped['area_burned'], name="wildfires area burned"),
    secondary_y=True,
)

# Add figure title
fig_trends.update_layout(
    title_text="Wildfires Trends"
)

# Set x-axis title
fig_trends.update_xaxes(title_text="year")

# Set y-axes titles
fig_trends.update_yaxes(title_text="<b>wildfires</b> count", secondary_y=False)
fig_trends.update_yaxes(title_text="<b>wildfires</b> area burned", secondary_y=True)








app.layout = html.Div(children=[
    html.H1(children='California Wildfires Analysis'),

    html.Div(children='Wildfires Geography Visualization'),

    dcc.Graph(
        id='map_graph',
        figure=fig_map
    ),
    html.Div(children='Wildfires Geography Visualization'),

    dcc.Graph(
        id='trend_graph',
        figure=fig_trends
    )
]
                     
                     
)

if __name__ == '__main__':
    app.run_server(debug=True)
