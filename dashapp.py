### ToDo: 
# Column with baseline leves for all the above (1990 or 2005 levels)
# column with annual perc growth form sliders
# column with annual perc rgowth from slider to the power of years since 2008 or 2009
# Trends: per capita residential emissions 2008-2017
# Trends: per capita total emissions 2008-2017


# source the data preparation yes or no
#exec(open('./dataprep.py').read())
#exec(open('./calcprep.py').read())

# Packages 
import os
import pandas as pd
import numpy as np
import re # for some string manipulation with regex
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


### Import the prepped data
df_final = pd.read_csv('./db/preppeddata.csv') 
df_nat = df_final[(df_final['geo']=='National') & (df_final['year']>=2005)]
# get good sort, with LULUCF as first one, then others on top
df_nat['sectorsorted'] =df_nat['sector']
df_nat.loc[(df_nat['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_nat = df_nat.sort_values(['sectorsorted', 'year'], ascending=[True, True])


#plotly figure
fig = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector",)
fig.show()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-sliders'),
    dcc.Slider(
        id='year-slider',
        min=1,
        max=5,
        value=1,
        step=1
    )
])


@app.callback(
    Output('graph-with-sliders', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    fig = px.area(df_nat, x="year", y="emissions_MtCo2_output", line_group="sector", color="sector")
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    