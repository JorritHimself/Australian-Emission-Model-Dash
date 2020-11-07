### ToDo: 
# Column with baseline leves for all the above (1990 or 2005 levels)
# column with annual perc growth form sliders
# column with annual perc rgowth from slider to the power of years since 2008 or 2009
# Trends: per capita residential emissions 2008-2017
# Trends: per capita total emissions 2008-2017

#### Added value only has data from 2008 onwards? Can we fix this, or do we censor?


########################
# Save the environemtn with dbc componenets
###################





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
import dash_bootstrap_components as dbc


### Import the prepped data
df_final = pd.read_csv('./db/preppeddata.csv') 
df_nat = df_final[(df_final['geo']=='National') & (df_final['year']>=2005) & (df_final['sector']!="Overall")]
# get good sort, with LULUCF as first one, then others on top
df_nat['sectorsorted'] =df_nat['sector']
df_nat.loc[(df_nat['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_nat = df_nat.sort_values(['sectorsorted', 'year'], ascending=[True, True])


### Define the app
# Note the stylesheet is loaded locally, see assets/ausenergydash_stylehseet.css
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

### List of starting figures and other output
fig_emissions_total = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector")
fig_added_value_total = px.area(df_nat, x="year", y="ind_val_add_output", color="sector")

### Define the app layout
app.layout = html.Div([
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='emissions-total', figure = fig_emissions_total))),
            dbc.Col(html.Div(dcc.Graph(id='value-added-total', figure = fig_added_value_total))),
            ]),
        dbc.Row([
            dbc.Col(html.Div([
                html.H6('Agriculture & Forestry emissions trend:'),
                dcc.Slider(id='agrifor-emis-slider', min=-20, max=20, value=0.54, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Electricity generation emissions trend:'),
                dcc.Slider(id='elec-emis-slider', min=-20, max=20, value=-1.96, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('LULUCF emissions trend:'),
                dcc.Slider(id='lulucf-emis-slider', min=-20, max=20, value=-12.2, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)})
                ])),
            ]),
        ])



#### Dynamic output based on user input
@app.callback(
    Output('emissions-total', 'figure'),
    [Input('agrifor-emis-slider', 'value'),
     Input('elec-emis-slider', 'value'),
     Input('lulucf-emis-slider', 'value')]
    )
def update_figure(agrifor_emis_trend, elec_emis_trend, lulucf_emis_trend):
    ### Emissions output agriculutre: emissions levels at last observation, minus number of years since final observation *annual emission reductions. Second line si so they cannot go negative
    df_nat.loc[(df_nat['sector']=='Agriculture & Forestry') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+agrifor_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Agriculture & Forestry') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Emissions output electricity: emissions levels at last observation, minus number of years since final observation *annual emission reductions. Second line si so they cannot go negative
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+elec_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Emissions output LULUCF: emissions levels at last observation, minus number of years since final observation *annual emission reductions
    df_nat.loc[(df_nat['sector']=='LULUCF') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+lulucf_emis_trend*df_nat['yrs_since_final_obs']
    
    
    
    
    ### Redefine figure again, but with dynamic input
    fig_emissions_total = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector")
    fig_emissions_total.update_layout(transition_duration=500)

    return fig_emissions_total



if __name__ == '__main__':
    app.run_server(debug=True)
    
    