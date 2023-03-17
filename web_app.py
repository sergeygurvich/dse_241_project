# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

app = Dash(__name__)


# Task 1
# plot bubble map
df_1 = pd.read_csv('wildfires_grouped_task1.csv')
# df_ = px.data.gapminder().query("year==2007")
fig_1 = px.scatter_geo(df_1, lat='lat',lon='lon',
                     size="count",
                     scope='usa',
                     center={'lat':37.16611, 'lon':-119.44944},
                     # fitbounds='locations',
                     # animation_group="year",
                     animation_frame="year",
                     color_continuous_scale=px.colors.cyclical.IceFire,
                     color='count',
                     hover_data=['year', 'count'],
                     hover_name="unit",
                     # title=' Wildfires Geography over Time'
                     )
fig_1.update_geos(
    resolution=50,
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Green",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Orange"
)
# fig.update_geos(fitbounds="locations")
fig_1.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig_1.update_layout(
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon': -73, 'lat': 46 },
        'zoom': 5},
    showlegend = False)

fig_1.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})


# TASK 2
# Read
df_2 = pd.read_csv('wildfires_grouped_task2_2.csv')

# Create figure with secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig_2.add_trace(
    go.Scatter(x=df_2['year'].astype(str), y=df_2['count'], name="wildfires count"),
    secondary_y=False,
)

fig_2.add_trace(
    go.Scatter(x=df_2['year'].astype(str), y=df_2['area_burned'], name="wildfires area burned"),
    secondary_y=True,
)

# # Add figure title
# fig_2.update_layout(
#     title_text="Wildfires Trends"
# )

# Set x-axis title
fig_2.update_xaxes(title_text="year")

# Set y-axes titles
fig_2.update_yaxes(title_text="<b>wildfires</b> count", secondary_y=False)
fig_2.update_yaxes(title_text="<b>wildfires</b> area burned", secondary_y=True)


# TASK 3
df_3 = pd.read_csv('wildfires_grouped_task3.csv')
fig_3 = px.bar(df_3, x="year", y="count", color="cause")


# TASK 4
df_4 = pd.read_csv('wildfires_grouped_task4.csv')
df_4_1 = df_4.groupby('month').sum()
df_4_1.reset_index(inplace=True)

order = df_4.groupby('cause').sum().sort_values('count', ascending=False)
order_list = order.index.to_list()
fig_4 = px.bar(df_4_1, x="month", y="count",
            height=500,
            width=1000,
            text_auto=True,
            category_orders={'cause': order_list},
            )
fig_4.update_xaxes(tickvals=np.arange(1,13), ticktext=['Jan', 'Feb', 'Mar',
                                                   'Apr', 'May', 'Jun',
                                                   'Jul', 'Aug', 'Sep',
                                                   'Oct', 'Nov', 'Dec'])


fig_5 = px.bar(df_4, x="month", y="count", 
            # color="cause",
            facet_row='cause', 
            facet_col_wrap=1,
            facet_row_spacing=0.007,
            height=2700,
            width=1000,
            text_auto=True,
            category_orders={'cause': order_list},
            )
fig_5.update_xaxes(tickvals=np.arange(1,13), ticktext=['Jan', 'Feb', 'Mar',
                                                   'Apr', 'May', 'Jun',
                                                   'Jul', 'Aug', 'Sep',
                                                   'Oct', 'Nov', 'Dec'])
fig_5.update_yaxes(title_font={'size':1})
xaxis = go.layout.YAxis(
        tickangle = 45)
fig_5.for_each_annotation(lambda a: a.update(text=a.text.split("- ")[1].split("/")[0]))
fig_5.update_yaxes(matches=None)

# TASK 5
df_5 = pd.read_csv('wildfires_grouped_task5.csv')

fig_6 = px.area(df_5, x="year", y="duration")





app.layout = html.Div(
    style={
"background-image": "url('/assets/fire.jpeg')",
"background-repeat": "repeat",
"background-position": "right top",
"background-size": "150px 100px"
},
    children=[
    html.H1(children='California Wildfires Analysis'),

    html.H2(children='Task 1: Wildfires Geography'),
    dcc.Graph(
        id='fig_1',
        figure=fig_1
    ),
    
    
    html.H2(children='Task 2: Wildfires Trends'),
    dcc.Graph(
        id='fig_2',
        figure=fig_2
    ),
    
    html.H2(children='Task 3: Causes Of Wildfires Onset'),
    dcc.Graph(
        id='fig_3',
        figure=fig_3
    ),
    
    html.H2(children='Task 4.1: Seasonality Of Wildfires'),
    dcc.Graph(
        id='fig_4',
        figure=fig_4
    ),


    html.H2(children="Task 4.2: Seasonality Of Wildfires by Their Cause"),
    dcc.Graph(
        id='fig_5',
        figure=fig_5
    ),
    
    html.H2(children="Task 5: Fire Average Duration"),
    dcc.Graph(
        id='fig_6',
        figure=fig_6
    ),
    
]
                     
                     
)

if __name__ == '__main__':
    app.run_server(debug=True)
