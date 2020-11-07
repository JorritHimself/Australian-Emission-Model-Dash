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
#import os
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


### Get stylesheet for pretty layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### Define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Define the app layout
app.layout = html.Div([
    dcc.Graph(id='graph-with-sliders'),
    html.H2('Agriculture emissions trend:'),
    dcc.Slider(id='agri-emis-slider', min=-20, max=20, value=0.54, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
    html.H2('Electricity generation emissions trend:'),
    dcc.Slider(id='elec-emis-slider', min=-20, max=20, value=-1.96, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
    html.H2('LULUCF emissions trend:'),
    dcc.Slider(id='lulucf-emis-slider', min=-20, max=20, value=-12.2, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)})
])


@app.callback(
    Output('graph-with-sliders', 'figure'),
    [Input('agri-emis-slider', 'value'),
     Input('elec-emis-slider', 'value'),
     Input('lulucf-emis-slider', 'value')])
def update_figure(agri_emis_trend, elec_emis_trend, lulucf_emis_trend):
    ### Emissions output agriculutre: emissions levels at last observation, minus number of years since final observation *annual emission reductions. Second line si so they cannot go negative
    df_nat.loc[(df_nat['sector']=='Agriculture') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+agri_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Agriculture') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Emissions output electricity: emissions levels at last observation, minus number of years since final observation *annual emission reductions. Second line si so they cannot go negative
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+elec_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
        ### Emissions output LULUCF: emissions levels at last observation, minus number of years since final observation *annual emission reductions
    df_nat.loc[(df_nat['sector']=='LULUCF') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+lulucf_emis_trend*df_nat['yrs_since_final_obs']
    
    fig = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector")
    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    
    