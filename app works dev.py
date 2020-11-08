### ToDo: 
# Column with baseline leves for all the above (1990 or 2005 levels)
# column with annual perc growth form sliders
# column with annual perc rgowth from slider to the power of years since 2008 or 2009
# Trends: per capita residential emissions 2008_2017
# Trends: per capita total emissions 2008_2017

#### Added value only has data from 2008 onwards? Can we fix this, or do we censor?


########################
# Reload environemtn with dbc componenets
###################





# source the data preparation yes or no
#exec(open('./dataprep.py').read())
#exec(open('./calcprep.py').read())

# Packages 
import pandas as pd
import numpy as np
import re # for some string manipulation with regex
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
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
### Work with defined set of colors to keep sector the same color across figures
# Emissions
fig_emissions_total = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector", color_discrete_sequence=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF']).update_layout(legend_traceorder="reversed")
# Added value
df_nat_val_add = df_nat[df_nat.sector != 'LULUCF']
df_nat_val_add = df_nat_val_add [df_nat_val_add .sector != 'Residential']
fig_added_value_total = px.area(df_nat_val_add, x="year", y="ind_val_add_output", color="sector", color_discrete_sequence=['#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#17BECF']).update_layout(legend_traceorder="reversed")

### Define the app layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div(html.H1('  ANU CCEP Australian emissions trend tool thingy'))),
            ]),
        dbc.Row([
            dbc.Col(html.Div(html.H6('  Introduction: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))),
            ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='emissions_total', figure = fig_emissions_total))),
            dbc.Col(html.Div(dcc.Graph(id='value_added_total', figure = fig_added_value_total))),
            ]),
        dbc.Row([
            dbc.Col(html.Div([
                html.H6('Agriculture & Forestry emissions trend:'),
                dcc.Slider(id='agrifor_emis_slider', min=-20, max=20, value=0.34, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}),
                html.H6('Commercial transport emissions trend:'),
                dcc.Slider(id='com_transp_emis_slider', min=-20, max=20, value=-0.71, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Construction emissions trend:'),
                dcc.Slider(id='construction_emis_slider', min=-20, max=20, value=--0.14, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Electricity generation emissions trend:'),
                dcc.Slider(id='electricity_emis_slider', min=-20, max=20, value=1.80, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Gas, water & waste services emissions trend:'),
                dcc.Slider(id='gas_water_waste_emis_slider', min=-20, max=20, value=0.31, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Manufacturing emissions trend:'),
                dcc.Slider(id='manufacturing_emis_slider', min=-20, max=20, value=1.83, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Mining emissions trend:'),
                dcc.Slider(id='mining_emis_slider', min=-20, max=20, value=-2.90, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Residential emissions trend:'),
                dcc.Slider(id='residential_emis_slider', min=-20, max=20, value=-0.70, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('Services emissions trend:'),
                dcc.Slider(id='services_emis_slider', min=-20, max=20, value=-0.32, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)}),
                html.H6('LULUCF emissions trend:'),
                dcc.Slider(id='lulucf_emis_slider', min=-20, max=20, value=-10.3, step=0.01, marks={i: '{}'.format(i) for i in range(-20, 20)})
                ])),
            ]),
        ], fluid=True, style={"padding": "20px 60px 20px 60px"}) ### This is for padding aroudn the entire app: fill the entire screen, but keep padding top right bottom left at x pixels
    ])

#### Dynamic output based on user input
@app.callback(
    Output('emissions_total', 'figure'),
    [Input('agrifor_emis_slider', 'value'),
     Input('com_transp_emis_slider', 'value'),
     Input('construction_emis_slider', 'value'),
     Input('electricity_emis_slider', 'value'),
     Input('gas_water_waste_emis_slider', 'value'),
     Input('manufacturing_emis_slider', 'value'),
     Input('mining_emis_slider', 'value'),
     Input('residential_emis_slider', 'value'),
     Input('services_emis_slider', 'value'),
     Input('lulucf_emis_slider', 'value')]
    )
def update_figure(agrifor_emis_trend, com_transp_emis_trend, construction_emis_trend, electricty_emis_trend, 
                  gas_water_waste_emis_trend, manufacturing_emis_trend, mining_emis_trend, residential_trend, services_trend, lulucf_emis_trend):
    ### Emissions output per sector: emissions levels at last observation, minus number of years since final observation *annual emission reductions. 
    ### Second line with each sector is so they cannot go negative. Exception is LULUCF, this can go negative
    ### Agriculture & forestry emmissions:
    df_nat.loc[(df_nat['sector']=='Agriculture & Forestry') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+agrifor_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Agriculture & Forestry') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Commercial Transport emmissions:
    df_nat.loc[(df_nat['sector']=='Commercial Transport') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+com_transp_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Commercial Transport') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Construction emmissions:
    df_nat.loc[(df_nat['sector']=='Construction') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+construction_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Construction') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Electricity emmissions:
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+electricty_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Electricity generation') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Gas, Water & Waste Services emissions:
    df_nat.loc[(df_nat['sector']=='Gas, Water & Waste Services') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+gas_water_waste_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Gas, Water & Waste Services') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Manufacturing emmissions:
    df_nat.loc[(df_nat['sector']=='Manufacturing') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+manufacturing_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Manufacturing') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Mining emmissions:
    df_nat.loc[(df_nat['sector']=='Mining') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+mining_emis_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Mining') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Residential emmissions:
    df_nat.loc[(df_nat['sector']=='Residential') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+residential_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Residential') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Services emmissions:
    df_nat.loc[(df_nat['sector']=='Services') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+services_trend*df_nat['yrs_since_final_obs']
    df_nat.loc[(df_nat['sector']=='Services') & (df_nat['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### LULUCF emissions: 
    ### Note again thes emay go negative
    df_nat.loc[(df_nat['sector']=='LULUCF') & (df_nat['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_nat['emissions_MtCo2_finaly']+lulucf_emis_trend*df_nat['yrs_since_final_obs']
    
    
    ### Redefine emissions total figure again, with dynamic input
    fig_emissions_total = px.area(df_nat, x="year", y="emissions_MtCo2_output", color="sector", color_discrete_sequence=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF'])
    fig_emissions_total.update_layout(transition_duration=500, legend_traceorder="reversed")
    return fig_emissions_total
    ### Redefine value added figure again, but with dynamic input
    df_nat_val_add = df_nat[df_nat.sector != 'LULUCF']
    df_nat_val_add = df_nat_val_add [df_nat_val_add .sector != 'Residential']
    fig_added_value_total = px.area(df_nat_val_add, x="year", y="ind_val_add_output", color="sector", color_discrete_sequence=['#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#17BECF'])
    fig_added_value_total.update_layout(transition_duration=500, legend_traceorder="reversed")
    return fig_added_value_total



if __name__ == '__main__':
    app.run_server()
    
    