# Run this app with `python web_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression
import os
from pathlib import Path

app = Dash(__name__)

# Load Data
notebook_path = __file__
data_path = Path(notebook_path).parent.joinpath('data')

df_1 = pd.read_csv(data_path / 'wildfires_grouped_task1.csv')
df_2 = pd.read_csv(data_path / 'wildfires_grouped_task2_2.csv')
df_3 = pd.read_csv(data_path / 'wildfires_grouped_task3.csv')
df_4_1 = pd.read_csv(data_path / 'wildfires_grouped_task4_1.csv')
df_4_2 = pd.read_csv(data_path / 'wildfires_grouped_task4_2.csv')
df_4_3 = pd.read_csv(data_path / 'wildfires_grouped_task4_3.csv')
df_5 = pd.read_csv(data_path / 'wildfires_grouped_task5.csv')


order = df_4_2.groupby('cause').sum().sort_values('count', ascending=False)
order_list = order.index.to_list()


def make_fig1():
    """
    Function to make Task 1 - Bubble map
    """
    fig_1 = px.scatter_geo(df_1, lat='lat',lon='lon',
                         size="area_burned",
                         scope='usa',
                         center={'lat':37.16611, 'lon':-119.44944},
                         animation_frame="year",
                         color_continuous_scale='bluered',
                         color='area_burned',
                         hover_data=['year', 'count'],
                         hover_name="unit",
                         )
    fig_1.update_geos(
        resolution=50,
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="#FFF3CD",
        showocean=True, oceancolor="lightblue",
        showlakes=True, lakecolor="lightblue",
        showrivers=True, rivercolor="lightblue",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Orange",
        projection_scale=2.7,
    )
    fig_1.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    fig_1.update_layout(
        mapbox = {
            'style': "stamen-terrain",
            'center': {'lon': -73, 'lat': 46 },
            'zoom': 5},
        showlegend = False)
    fig_1.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    fig_1.update_layout(coloraxis_colorbar_x=0.8)
    fig_1.update_layout(
    coloraxis_colorbar=dict(
        title="Area Burned, acres",
    ),
)
    
    return fig_1

def make_fig2():
    """
    Function to make Task 2 - Trends
    """

    # Create figure with secondary y-axis
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig_2.add_trace(go.Scatter(x=df_2['year'].astype(str), y=df_2['count'], name="wildfires count"), secondary_y=False)
    
    # trend line 1
    X = df_2[['year']]
    y=df_2['count']
    model = LinearRegression().fit(X,y)
    y_hat = model.predict(X)
    
    fig_2.add_trace(go.Scatter(x=df_2['year'].astype(str), y=y_hat, line = dict(color='royalblue', width=1, dash='dash'),
                               name="wildfires count trend"), 
                               secondary_y=False)

    fig_2.add_trace(
        go.Scatter(x=df_2['year'].astype(str), y=df_2['area_burned'], name="wildfires area burned", line = dict(color='red')), 
        secondary_y=True)
    
    # trend line 2
    y=df_2['area_burned']
    model = LinearRegression().fit(X,y)
    y_hat2 = model.predict(X)
    
    fig_2.add_trace(go.Scatter(x=df_2['year'].astype(str), y=y_hat2, name="wildfires area burned trend",
                              line = dict(color='firebrick', width=1, dash='dot')), secondary_y=True)
    


    # Set x-axis title
    fig_2.update_xaxes(title_text="year")

    # Set y-axes titles
    fig_2.update_yaxes(title_text="wildfires count", secondary_y=False)
    fig_2.update_yaxes(title_text="wildfires area burned, acres", secondary_y=True)

    return fig_2

def make_fig3():
    """
    Function to make Task 3 - Onset Stacked Bar Chart
    """

    fig_3 = px.bar(df_3, x="year", y="count", color="cause", category_orders={'cause': order_list},
                    height=500,
                    width=1200,
                    # color_discrete_sequence=px.colors.qualitative.G10
                  )
    fig_3.update_yaxes(title_text="wildfires count")
    
    return fig_3


def make_fig4_1():
    """
    Function to make Task 4.1 - Seasonality Bar Charts
    """
    fig_4_1 = px.bar(df_4_1, x="month", y="count",
                height=500,
                width=1000,
                text_auto=True,
                category_orders={'cause': order_list},
                )
    fig_4_1.update_xaxes(tickvals=np.arange(1,13), ticktext=['Jan', 'Feb', 'Mar',
                                                       'Apr', 'May', 'Jun',
                                                       'Jul', 'Aug', 'Sep',
                                                       'Oct', 'Nov', 'Dec'])

    return fig_4_1


def make_fig4_2():
    """
    Function to make Task 4.2 - Seasonality Bar Charts
    """
    fig_4_2 = px.bar(df_4_2, x="month", y="count", 
                # color="cause",
                facet_row='cause', 
                facet_col_wrap=1,
                facet_row_spacing=0.007,
                height=2700,
                width=1000,
                text_auto=True,
                category_orders={'cause': order_list},
                )
    fig_4_2.update_xaxes(tickvals=np.arange(1,13), ticktext=['Jan', 'Feb', 'Mar',
                                                       'Apr', 'May', 'Jun',
                                                       'Jul', 'Aug', 'Sep',
                                                       'Oct', 'Nov', 'Dec'])
    fig_4_2.update_yaxes(title_font={'size':1})
    xaxis = go.layout.YAxis(
            tickangle = 45)
    fig_4_2.for_each_annotation(lambda a: a.update(text=a.text.split("- ")[1].split("/")[0]))
    fig_4_2.update_yaxes(matches=None)


    return fig_4_2


def make_fig4_3():
    """
    Function to make Task 4.3 - Seasonality Bar Charts Animation
    """
    fig_4_3 = px.bar(df_4_3, x="month", y="count",
                height=500,
                width=1000,
                # text_auto=True,
                animation_frame='year',
                range_y=[0,135]
                )
    fig_4_3.update_xaxes(tickvals=np.arange(1,13), ticktext=['Jan', 'Feb', 'Mar',
                                                       'Apr', 'May', 'Jun',
                                                       'Jul', 'Aug', 'Sep',
                                                       'Oct', 'Nov', 'Dec'])
    fig_4_3.update_yaxes(title_font={'size':1})
    xaxis = go.layout.YAxis(
            tickangle = 45)
    # fig_4_3.update_yaxes(matches=None)


    return fig_4_3

def make_fig5():
    """
    Function to make Task 5 - Avg Fire Duration, Area Chart
    """
    fig_5 = px.area(df_5, x="year", y="duration",
                height=500,
                width=1200)
    fig_5.update_yaxes(title_text="average fire duration, days")
    return fig_5





app.layout = html.Div(

    children=[
            html.H1(children='California Wildfires Analysis'),
            dcc.Dropdown(   options=[
               {'label': '1. Wildfires Geography', 'value': 'task1'},
               {'label': '2. Wildfires Trends', 'value': 'task2'},
               {'label': '3. Causes Of Wildfires Onset', 'value': 'task3'},
               {'label': '4.1. Seasonality Of Wildfires Overall', 'value': 'task4_1'},
               {'label': '4.2. Seasonality Of Wildfires by Their Cause', 'value': 'task4_2'},
               {'label': '4.3. Seasonality Of Wildfires by Years', 'value': 'task4_3'},
               {'label': '5. Average Wildfire Duration', 'value': 'task5'},
               ],
               value='task1',id='demo-dropdown', searchable=False, clearable=False),
            html.Div(id='dd-output-container'),
            dcc.Graph(id='fig_1', figure=make_fig1()),
    ]
)

    
@app.callback(
    Output('fig_1', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value == 'task1':
        fig = make_fig1()
        return fig
    if value == 'task2':
        fig = make_fig2()
        return fig
    if value == 'task3':
        fig = make_fig3()
        return fig
    if value == 'task4_1':
        fig = make_fig4_1()
        return fig
    if value == 'task4_2':
        fig = make_fig4_2()
        return fig
    if value == 'task4_3':
        fig = make_fig4_3()
        return fig
    if value == 'task5':
        fig = make_fig5()
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
