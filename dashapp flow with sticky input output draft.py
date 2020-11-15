### ToDo: 
# Column with baseline leves for all the above
# column with annual perc growth form sliders
# column with annual perc rgowth from slider to the power of years since 2008 or 2009
# Trends: per capita residential emissions 2008_2017
# Trends: per capita total emissions 2008_2017
# Reload environemtn with dbc componenets
# tabbed in a loop
# extra tabs woth method etc
# white backgroudn theme
# beter colours wihtout the line
## Add title and change labels: https://plotly.com/python/figure-labels/
# Add scenarios
# Create a file with baseline slidervalues
# Better slider
# Smaller everything
# Create separate emis and va df
# Add calculations as in excel scenario sheet
###################





# source the data preparation yes or no
#exec(open('./dataprep.py').read())
#exec(open('./calcprep.py').read())

# Packages 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc


### Import the prepped data
df_full = pd.read_csv('./db/preppeddata.csv') 

# get good sort, with LULUCF as first one, then others on top
df_full['sectorsorted']=df_full['sector']
df_full.loc[(df_full['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_full.loc[(df_full['sector']=='Residential'), 'sectorsorted'] = '1 Residential'
df_full.loc[(df_full['sector']=='Electricity generation'), 'sectorsorted'] = '2 Electricity generation'
df_full = df_full.sort_values(['sectorsorted', 'year'], ascending=[True, True])

# Define list of states
statelist = ['National' , 'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

### Get national values: these are use to create the figures for when the user lands on the page and hasnt selected a tab yet
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
### List of starting figures and other output
### Work with defined set of colors to keep sector the same color across figures
## Emissions figure
fig_emissions_total = px.area(df_select, x="year", y="emissions_MtCo2_output", color="sector", 
                              color_discrete_sequence=['#1F77B4', '#FF7F0E', '#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                              labels={"year": "", "emissions_MtCo2_output": "CO2 Emissions (Mt CO<sub>2</sub>-eq/y)"},
                              title="Annual CO<sub>2</sub>-emissions by industry")
fig_emissions_total.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=60, pad=0))
fig_emissions_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_emissions_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)

## Added value figure
df_select_val_add = df_select[df_select.sector != 'LULUCF']
df_select_val_add = df_select_val_add [df_select_val_add.sector != 'Residential']
fig_added_value_total = px.area(df_select_val_add, x="year", y="ind_val_add_output", color="sector",
                                color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                labels={"year": "", "ind_val_add_output": "Value added (billion 2019 AUD)"},
                                title="Value added by industry")
fig_added_value_total.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=60, pad=0))
fig_added_value_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_added_value_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)


### Define the app
# Note an additional stylesheet is loaded locally, see assets/bootstrap_modified.css
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


### Define the app layout with tabs: content 'tabslist-content' is generated based on the tab selection
app.layout = html.Div(style={'backgroundColor': 'rgba(192, 192, 192, 0.2)'}, children=[ ### backgroundColor here is for the whole webpage
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div(html.H1('  ANU CCEP Australian emissions trend tool thingy'))),
            ],style={"color": "#1F77B4"}),
        dbc.Row([
            dbc.Col(html.Div(html.H5('  Introduction: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))),
            ]),
        ], fluid=True, style={"padding": "20px 200px 20px 200px"}), ### padding around the title and intro
    dbc.Container([
        dcc.Tabs(id='tabslist', value='National', children=[
            dcc.Tab(label='Australia', value='National'),
            dcc.Tab(label='ACT', value='ACT'),
            dcc.Tab(label='NSW', value='NSW'),
            dcc.Tab(label='NT', value='NT'),
            dcc.Tab(label='QLD', value='QLD'),
            dcc.Tab(label='SA', value='SA'),
            dcc.Tab(label='TAS', value='TAS'),
            dcc.Tab(label='VIC', value='VIC'),
            dcc.Tab(label='WA', value='WA'),
            dcc.Tab(label='Documentation', value='docs'),
            dcc.Tab(label='Reports', value='other')
            ])
        ], fluid=True, style={"padding": "0px 130px 20px 130px", "position": "sticky", "top": 0, 'zIndex': 9999}), ### padding around the tabs box. Sticky and zIndex make it float on top of the other stuff. Keep padding top at 0 because otherwise the other stuff will be visible again 
    dbc.Container([
        html.Div(id='tabslist-content')
        ], fluid=True, style={"padding": "20px 60px 20px 60px"}) ### padding around the entire app
    ])


### Define app content based on tab choice. 
### The slider value selection is a separate callback, below this block
@app.callback(Output('tabslist-content', 'children'),
              [Input('tabslist', 'value')])
def render_content(tab):
    if tab in statelist:
        return html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col((html.Div(html.H3('Sector'))), width=2),
            dbc.Col((html.Div(html.H3('Annaul industry emission reduction'))), width=2),
            dbc.Col((html.Div(html.H3('Industry gross added value growth'))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6(''))), width=2),
            dbc.Col((html.Div(html.H6('(Mt CO2-eq per year)'))), width=2),
            dbc.Col((html.Div(html.H6('(% annual change in 2019 AUD)'))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Services'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='services_emis_slider', min=-20, max=20, value=-0.32, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(23,190,207,0.8)"}),     
        dbc.Row([
            dbc.Col((html.Div(html.H6('Mining'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='mining_emis_slider', min=-20, max=20, value=2.90, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(127,127,127,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Manufacturing'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='manufacturing_emis_slider', min=-20, max=20, value=1.83, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(188,189,34,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Gas, water & waste services'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='gas_water_waste_emis_slider', min=-20, max=20, value=0.31, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(227,119,194,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Construction'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='construction_emis_slider', min=-20, max=20, value=-0.14, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(140,86,75,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Commercial transport'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='com_transp_emis_slider', min=-20, max=20, value=-0.71, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(148,103,189,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Agriculture & Forestry'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='agrifor_emis_slider', min=-20, max=20, value=0.34, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2)
            ],style={"background-color": "rgba(44,160,44,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H6('LULUCF'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='lulucf_emis_slider', min=-20, max=20, value=-10.3, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(31,119,180,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H3('Sector'))), width=2),
            dbc.Col((html.Div(html.H3('Annaul industry emission reduction'))), width=2),
            dbc.Col((html.Div(html.H3('Electricity generation growth'))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6(''))), width=2),
            dbc.Col((html.Div(html.H6('(Mt CO2-eq per year)'))), width=2),
            dbc.Col((html.Div(html.H6('(% per year)'))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Electricity generation'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='electricity_emis_slider', min=-20, max=20, value=1.80, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(214,39,40,0.8)"}),
        dbc.Row([
            dbc.Col((html.Div(html.H3('Sector'))), width=2),
            dbc.Col((html.Div(html.H3('Annaul emission reduction'))), width=2),
            dbc.Col((html.Div(html.H3(''))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6(''))), width=2),
            dbc.Col((html.Div(html.H6('(Mt CO2-eq per year)'))), width=2),
            dbc.Col((html.Div(html.H6(''))), width=2),
            ]),
        dbc.Row([
            dbc.Col((html.Div(html.H6('Residential'))), width=2),
            dbc.Col((html.Div(dcc.Slider(id='residential_emis_slider', min=-20, max=20, value=0.70, step=0.01, marks={-20: '-20',-10: '-10',0: '0',10: '10',20: '20'}))), width=2),
            dbc.Col((html.Div(html.H6('Placeholder for slider'))), width=2),
            ],style={"background-color": "rgba(255,127,14,0.8)"}),
        ], fluid=True, style={"padding": "20px 60px 20px 60px", "position": "sticky", "top": 50, 'zIndex': 9999, 'backgroundColor': 'rgba(192, 192, 192, 1)'}), ### This is for padding aroudn the entire app: fill the entire screen, but keep padding top right bottom left at x pixels
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='emissions_total', figure = fig_emissions_total))),
            dbc.Col(html.Div(dcc.Graph(id='value_added_total', figure = fig_added_value_total))),
            ]),
        ], fluid=True, style={"padding": "20px 60px 20px 60px"}),
    ])
    elif tab == 'docs':
        return html.Div([
            html.H3('Here will be some documentation')
            ])
    elif tab == 'other':
        return html.Div([
            html.H3('Here will be some other reports and links to the CCEP website etc')
            ])

### Update the figures dynamically based on slider input
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
     Input('lulucf_emis_slider', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_emisisons_total(agrifor_emis_trend, com_transp_emis_trend, construction_emis_trend, electricty_emis_trend, 
                  gas_water_waste_emis_trend, manufacturing_emis_trend, mining_emis_trend, residential_trend, services_trend, lulucf_emis_trend,
                  tab):
    df_select = df_full[(df_full['geo']==tab) & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
    ### Emissions output per sector: emissions levels at last observation, minus number of years since final observation *annual emission reductions. 
    ### Second line with each sector is so they cannot go negative. Exception is LULUCF, this can go negative
    ### Agriculture & forestry emmissions:
    df_select.loc[(df_select['sector']=='Agriculture & Forestry') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+agrifor_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Agriculture & Forestry') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Commercial Transport emmissions:
    df_select.loc[(df_select['sector']=='Commercial Transport') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+com_transp_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Commercial Transport') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Construction emmissions:
    df_select.loc[(df_select['sector']=='Construction') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+construction_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Construction') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Electricity emmissions:
    df_select.loc[(df_select['sector']=='Electricity generation') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+electricty_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Electricity generation') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Gas, Water & Waste Services emissions:
    df_select.loc[(df_select['sector']=='Gas, Water & Waste Services') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+gas_water_waste_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Gas, Water & Waste Services') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Manufacturing emmissions:
    df_select.loc[(df_select['sector']=='Manufacturing') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+manufacturing_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Manufacturing') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Mining emmissions:
    df_select.loc[(df_select['sector']=='Mining') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+mining_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Mining') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Residential emmissions:
    df_select.loc[(df_select['sector']=='Residential') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+residential_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Residential') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Services emmissions:
    df_select.loc[(df_select['sector']=='Services') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+services_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Services') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### LULUCF emissions: 
    ### Note again thes emay go negative
    df_select.loc[(df_select['sector']=='LULUCF') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+lulucf_emis_trend*df_select['yrs_since_final_obs']
    ### Redefine emissions total figure again, with dynamic input
    fig_emissions_total = px.area(df_select, x="year", y="emissions_MtCo2_output", color="sector", 
                                  color_discrete_sequence=['#1F77B4', '#FF7F0E', '#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                    labels={"year": "", "emissions_MtCo2_output": "CO2 Emissions (Mt CO<sub>2</sub>-eq/y)"},
                                    title="Annual CO<sub>2</sub>-emissions by industry")
    fig_emissions_total.update_layout(transition_duration=500,
                                      template="plotly_white",
                                      legend_traceorder="reversed",
                                      title_font_color="#1F77B4",
                                      title_font_size=18,
                                      title_font_family="Rockwell",
                                      title_x = 0.02,
                                      margin=dict(t=40, r=0, b=0, l=60, pad=0))
    fig_emissions_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_emissions_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_emissions_total


    ### Redefine value added figure again, but with dynamic input
    df_select_val_add = df_select[df_select.sector != 'LULUCF']
    df_select_val_add = df_select_val_add [df_select_val_add .sector != 'Residential']
    fig_added_value_total = px.area(df_select_val_add, x="year", y="ind_val_add_output", color="sector", color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'])
    fig_added_value_total.update_layout(transition_duration=500, legend_traceorder="reversed")
    return fig_added_value_total


if __name__ == '__main__':
    app.run_server(debug=True)
    

