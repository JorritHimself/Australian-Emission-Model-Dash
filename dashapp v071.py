### ToDo: 
# Column with baseline leves for all the above
# column with annual perc growth form pickers
# column with annual perc rgowth from picker to the power of years since 2008 or 2009
# Smaller everything
# Create separate emis and va df
# Add calculations as in excel scenario sheet
# LULUCF to brown
# 2030 rates
###################

# Packages 
import pandas as pd
import numpy as np
import xlrd # Required dependency for pd.read_excel
import ast
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

### Import the prepped input data
df_full = pd.read_csv('./db/preppeddata.csv')
### Import the picker settings 
df_picker_in = pd.read_excel('./db/inputpickerlist.xlsx', sheet_name="pickersettings") 

# get good sort, with LULUCF as first one, then others on top
df_full['sectorsorted']=df_full['sector']
df_full.loc[(df_full['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_full.loc[(df_full['sector']=='Residential'), 'sectorsorted'] = '1 Residential'
df_full.loc[(df_full['sector']=='Electricity generation'), 'sectorsorted'] = '2 Electricity generation'
df_full = df_full.sort_values(['sectorsorted', 'year'], ascending=[True, True])

# Define list of states
statelist = ['National' , 'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
# Define list of picker names: this will be used in a loop to create a dictionary of vlues to set pickersettinsg for each state
pickerlist = ['services_emis_picker','mining_emis_picker','manufacturing_emis_picker','gas_water_waste_emis_picker','construction_emis_picker',
'com_transp_emis_picker','agrifor_emis_picker','lulucf_emis_picker','electricity_emis_picker','residential_emis_picker',
'services_valadd_picker','mining_valadd_picker','manufacturing_valadd_picker','gas_water_waste_valadd_picker',
'construction_valadd_picker','com_transp_valadd_picker','agrifor_valadd_picker','electricity_growth_picker']
# Define list of picker settings: this will be used in a loop to create a dictionary of vlues to set pickersettinsg for each state
pickersettinglist = ['min', 'max','value', 'steps', 'marks']

# Define list of colors for the sectors
my_discrete_color_map={"LULUCF": '#8C564B',
                    "Residential": '#FF7F0E',
                    "Electricity generation":'#D62728',
                    "Agriculture & Forestry":'#2CA02C',
                    "Commercial Transport": '#9467BD',
                    "Construction": '#1F77B4',
                    "Gas, Water & Waste Services":'#E377C2',
                    "Manufacturing":'#BCBD22', 
                    "Mining":'#7F7F7F', 
                    "Services": '#17BECF'}

### Get national values: these are use to create the figures for when the user lands on the page and hasnt selected a tab yet
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2005) & (df_full['sector']!="Overall")]
### List of starting figures and other output
### Work with defined set of colors to keep sector the same color across figures
## Emissions figure
fig_emissions_total = px.area(df_select, x="year", y="emissions_MtCo2_output", color="sector", 
                              color_discrete_map=my_discrete_color_map,
                              labels={"year": "", "emissions_MtCo2_output": "CO<sub>2</sub> Emissions (Mt CO<sub>2</sub>-eq/y)"},
                              title="CO<sub>2</sub>-emissions by industry",
                              width=800, height=375)
fig_emissions_total.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=65, pad=0))
fig_emissions_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_emissions_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)

## Added value figure
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
df_select_val_add = df_select[df_select.sector != 'LULUCF']
df_select_val_add = df_select_val_add [df_select_val_add.sector != 'Residential']
fig_added_value_total = px.area(df_select_val_add, x="year", y="ind_val_add_output", color="sector",
                                color_discrete_map=my_discrete_color_map,
                                labels={"year": "", "ind_val_add_output": "Value added (billion 2019 AUD)<sub> </sub>"},
                                title="Value added by industry",
                                width=800, height=375)
fig_added_value_total.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=65, pad=0))
fig_added_value_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_added_value_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)

## Emission intensity figure
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
df_select_emis_int = df_select[df_select.sector != 'LULUCF']
df_select_emis_int = df_select_emis_int[df_select_emis_int.sector != 'Residential']
fig_emis_int = px.line(df_select_emis_int, x="year", y="emis_int_outp", color="sector",
                       color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                       labels={"year": "", "emis_int_outp": "Emission intensity (kg CO<sub>2</sub>-eq/2019 AUD)"},
                       title="Emission intensity by industry",
                       width=800, height=375)
fig_emis_int.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=65, pad=0))
fig_emis_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_emis_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)

## Electricity generation and carbon intensity
df_select_elec = df_full[(df_full['geo']=='National') & (df_full['year']>=2005) & (df_full['sector']=="Electricity generation")]
# Make lists of you data because of course this type of figure has a completley different syntax again
year_dict = df_select_elec['year'].tolist()
gwh_dict = df_select_elec['elec_gen_GWh_output'].tolist()
elec_carb_int_dict = df_select_elec['elec_carb_int_outp'].tolist()
# create df_select_elec
fig_elec_gen_int = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig_elec_gen_int.add_scatter(x=year_dict, y=gwh_dict, name="Electricity generation", mode="lines", line=dict(width=2, color="rgba(214,39,40,1)"), secondary_y=False,)
fig_elec_gen_int.add_scatter(x=year_dict, y=elec_carb_int_dict, name="Carbon intensity", mode="lines", line=dict(width=2, color="black"), secondary_y=True,)
fig_elec_gen_int.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_text="Electricity generation and carbon intensity",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=65, pad=0),
                                    width=800, height=375)
fig_elec_gen_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_elec_gen_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
# Set y-axes titles
fig_elec_gen_int.update_yaxes(title_text="Electricity generation (GWh)<sub> </sub>", secondary_y=False)
fig_elec_gen_int.update_yaxes(title_text="Carbon intensity (kg CO<sub>2</sub>-eq/kWh)", secondary_y=True)






#######################  HTML divs styles for the overall layout  ######################

# the style arguments for the header. 
my_header_style = {
    "padding": "0 10% 0 10%",
    "width": "100%",
    "background-color": "#f8f9fa",
}
# the style arguments for the header. 
my_tablist_style = {
    "position": "sticky",
    "top": 0,
    "padding": "0 10% 0 10%",
    "width": "100%",
    "background-color": "#f8f9fa",
    'zIndex': 9999
    }
# the style arguments for the sidebar. Sticky on top: scrolls untill 50px from top
my_sidebar_style = {
    "position": "sticky",
    "top": 65,
    "left": "10%",
    "width": "45%",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
my_content_style = {
    "position": "relative",
    "top": -550,
    "margin-left": "53%",
}








### Define the app
# Note an additional stylesheet is loaded locally, see assets/bootstrap_modified.css
app = dash.Dash(__name__)


header  = html.Div(style=my_header_style, children=[ ### backgroundColor here is for the whole webpage
    dbc.Container([
        dbc.Row([
            html.Div(html.H1('2050 emissions pathway tool for')),
            ],style={"color": "#1F77B4"}),
        dbc.Row([
            html.Div(html.H1('Australia and Australian States and Territories')),
            ],style={"color": "#1F77B4"}),
        dbc.Row([
            html.Div(html.H3('V0.71: this tool is still under development')),
            ],style={"color": "#D62701", }),
        dbc.Row([
            html.Div(html.H4('This tool compiles data from Australia’s emissions inventories, economics statistics and some other sources, and allows the creation of pathways to low-emissions and net zero outcomes.')),
            ]),
        dbc.Row([
            html.Div(html.H4('It allows users to input their own assumptions about future rates of change of economic activity and emissions intensity by sector, for Australia as a whole and for each State and Territory.')),
            ]),
        dbc.Row([
            html.Div(html.H4('Brief instructions: (Instructions to users to come)')),
            ]),
        ], fluid=True), ### padding around the title and intro
    ])

tabheader = html.Div(style=my_tablist_style, children=[ ### backgroundColor here is for the whole webpage
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
            dcc.Tab(label='About', value='about'),
            dcc.Tab(label='Reports', value='other')
            ]),
        ], fluid=True), 
    ])

sidebar  = html.Div(style=my_sidebar_style, children=[
    dbc.Container([
        html.Div(id='tabslist-sidebar')
        ], fluid=True),
    ])


content  = html.Div(style=my_content_style, children=[
    dbc.Container([
        html.Div(id='tabslist-content')
        ], fluid=True),
    ])



# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/


### Define the app layout with tabs: content 'tabslist-content' is generated based on the tab selection
#app.layout = html.Div([dcc.Location(id="url"), header, sidebar, content])

app.layout = html.Div([header, tabheader, sidebar, content], style ={"background-color": "#f8f9fa"})
    
        
### Define app content based on tab choice. 
### The picker value selection is a separate callback, below this block
@app.callback(Output('tabslist-sidebar', 'children'),
              [Input('tabslist', 'value')])
def render_sidebar(tab):
    if tab in statelist:
        ## Loop to get the right picker settings for each state and type of picker
        df_pickerselect = df_picker_in[(df_picker_in['geo']==tab)]
        df_pickerselect = df_pickerselect.set_index('picker')
        pickersetting_dict = {}
        for pickername in pickerlist:
            for pickersetting in pickersettinglist:
                pickersetting_dict[pickername + '_' + pickersetting] = df_pickerselect._get_value(pickername, pickersetting)
        return html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=2),
                    dbc.Col((html.Div(html.H4('Annaul change in emissions by sector'))), width=5),
                    dbc.Col((html.Div(html.H4('Industry gross added value growth'))), width=5),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H5(''))), width=3),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=5),
                    dbc.Col((html.Div(html.H5('(% annual change in 2019 AUD)'))), width=4),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H5(''))), width=3),
                    dbc.Col((html.Div(html.H5('10yr trend'))), width=1),
                    dbc.Col((html.Div(html.H5('2020 to 2030'))), width=2),
                    dbc.Col((html.Div(html.H5('2030 to 2050'))), width=2),
                    dbc.Col((html.Div(html.H5('10yr trend'))), width=2),
                    dbc.Col((html.Div(html.H5('2020 to 2050'))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Services'))), width=3),
                    dbc.Col((html.Div(html.H4(pickersetting_dict['services_emis_picker_value']))), width=1),
                    dbc.Col((html.Div(dbc.Input(id='services_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['services_emis_picker_value'], step=pickersetting_dict['services_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='services_emis_picker3050', type="number", bs_size="sm", value=pickersetting_dict['services_emis_picker_value'], step=pickersetting_dict['services_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H4(pickersetting_dict['services_valadd_picker_value']))), width=1, style={'text-align': 'center'}),
                    dbc.Col((html.Div(dbc.Input(id='services_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['services_valadd_picker_value'], step=pickersetting_dict['services_valadd_picker_steps']))), width=2),
                    ],style={"background-color": "rgba(23,190,207,0.6)"}),     
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Mining'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='mining_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['mining_emis_picker_value'], step=pickersetting_dict['mining_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='mining_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['mining_valadd_picker_value'], step=pickersetting_dict['mining_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(127,127,127,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Manufacturing'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='manufacturing_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['manufacturing_emis_picker_value'], step=pickersetting_dict['manufacturing_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='manufacturing_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['manufacturing_valadd_picker_value'], step=pickersetting_dict['manufacturing_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(188,189,34,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Gas, water & waste services'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='gas_water_waste_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['gas_water_waste_emis_picker_value'], step=pickersetting_dict['gas_water_waste_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='gas_water_waste_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['gas_water_waste_valadd_picker_value'], step=pickersetting_dict['gas_water_waste_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(227,119,194,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Construction'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='construction_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['construction_emis_picker_value'], step=pickersetting_dict['construction_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='construction_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['construction_valadd_picker_value'], step=pickersetting_dict['construction_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(31,119,180,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Commercial transport'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='com_transp_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['com_transp_emis_picker_value'], step=pickersetting_dict['com_transp_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='com_transp_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['com_transp_valadd_picker_value'], step=pickersetting_dict['com_transp_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(148,103,189,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Agriculture & Forestry'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='agrifor_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['agrifor_emis_picker_value'], step=pickersetting_dict['agrifor_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='agrifor_valadd_picker', type="number", bs_size="sm", value=pickersetting_dict['agrifor_valadd_picker_value'], step=pickersetting_dict['agrifor_valadd_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(44,160,44,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('LULUCF'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='lulucf_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['lulucf_emis_picker_value'], step=pickersetting_dict['lulucf_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=2),
					],style={"background-color": "rgba(140,86,75,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=3),
                    dbc.Col((html.Div(html.H4('Annaul change in emissions by sector'))), width=4),
                    dbc.Col((html.Div(html.H4('Electricity generation growth'))), width=4),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H5(''))), width=3),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=4),
                    dbc.Col((html.Div(html.H5('(% per year)'))), width=4),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Electricity generation'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='electricity_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['electricity_emis_picker_value'], step=pickersetting_dict['electricity_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(dbc.Input(id='electricity_growth_picker', type="number", bs_size="sm", value=pickersetting_dict['electricity_growth_picker_value'], step=pickersetting_dict['electricity_growth_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    ],style={"background-color": "rgba(214,39,40,0.6)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=3),
                    dbc.Col((html.Div(html.H4('Annaul emission change'))), width=4),
                    dbc.Col((html.Div(html.H4(''))), width=4),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4(''))), width=3),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=4),
                    dbc.Col((html.Div(html.H4(''))), width=4),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Residential'))), width=3),
                    dbc.Col((html.Div(dbc.Input(id='residential_emis_picker', type="number", bs_size="sm", value=pickersetting_dict['residential_emis_picker_value'], step=pickersetting_dict['residential_emis_picker_steps']))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=4),
                    ],style={"background-color": "rgba(255,127,14,0.6)"}),
                dbc.Row([
                    html.Div(html.H4('Provided by the Centre for Climate and Energy Policy, Crawford School of Public Policy, The Australian National University, with funding support by the 2050 Pathways Platform.')),
                    ]),
                dbc.Row([
                    html.Div(html.H4('Contact for queries and comments: ccep@anu.edu.au')),
                    ]),
                dbc.Row([
                    html.Div(html.H4('Emission pathway tool concept and data compilation by Paul Wyrwoll, Jorrit Gosens, Zeba Anjum, Frank Jotzo.')),
                    ]),
                dbc.Row([
                    html.Div(html.H4('Website & web application in Dash built by Jorrit Gosens.')),
                    ]),
                ], fluid=True, style={"padding": "20px 20px 20px 20px", 'backgroundColor': 'rgba(242, 241, 239, 1)', "position": "sticky", "top": 60, 'zIndex': 9999}), ### This is for padding aroudn the entire app: fill the entire screen, but keep padding top right bottom left at x pixels
            ])
    elif tab == 'docs':
        return html.Div([
            html.H3('Here will be some documentation')
            ])
    elif tab == 'other':
        return html.Div([
            html.H3('Here will be some other reports and links to the CCEP website etc')
            ])
    
    
    
    
### Define app content based on tab choice. 
### The picker value selection is a separate callback, below this block
@app.callback(Output('tabslist-content', 'children'),
              [Input('tabslist', 'value')])
def render_content(tab):
    if tab in statelist:
        return html.Div([
            dbc.Container([
                dbc.Row([html.Div(dcc.Graph(id='emissions_total', figure = fig_emissions_total))]),
                dbc.Row([html.Div(dcc.Graph(id='value_added_total', figure = fig_added_value_total))]),
                dbc.Row([html.Div(dcc.Graph(id='emis_int', figure = fig_emis_int))]),
                dbc.Row([html.Div(dcc.Graph(id='elec_gen_int', figure = fig_elec_gen_int))]),
                dbc.Row([html.Div(html.H2('To Do: Residential per capita emissions'))]),
                ]),
            ])
    elif tab == 'docs':
        return html.Div([
            html.H3('Here will be some documentation')
            ])
    elif tab == 'other':
        return html.Div([
            html.H3('Here will be some other reports and links to the CCEP website etc')
            ])    

### Update the emissions figure dynamically based on picker input
@app.callback(
    Output('emissions_total', 'figure'),
    [Input('agrifor_emis_picker', 'value'),
     Input('com_transp_emis_picker', 'value'),
     Input('construction_emis_picker', 'value'),
     Input('electricity_emis_picker', 'value'),
     Input('gas_water_waste_emis_picker', 'value'),
     Input('manufacturing_emis_picker', 'value'),
     Input('mining_emis_picker', 'value'),
     Input('residential_emis_picker', 'value'),
     Input('services_emis_picker', 'value'),
     Input('lulucf_emis_picker', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_emisisons_total(agrifor_emis_trend, com_transp_emis_trend, construction_emis_trend, electricty_emis_trend, 
                  gas_water_waste_emis_trend, manufacturing_emis_trend, mining_emis_trend, residential_emis_trend, services_emis_trend, lulucf_emis_trend,
                  tab):
    df_select = df_full[(df_full['geo']==tab) & (df_full['year']>=2005) & (df_full['sector']!="Overall")]
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
    df_select.loc[(df_select['sector']=='Residential') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+residential_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Residential') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Services emmissions:
    df_select.loc[(df_select['sector']=='Services') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+services_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Services') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### LULUCF emissions: 
    ### Note again thes emay go negative
    df_select.loc[(df_select['sector']=='LULUCF') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+lulucf_emis_trend*df_select['yrs_since_final_obs']
    ### Redefine emissions total figure again, with dynamic input
    fig_emissions_total = px.area(df_select, x="year", y="emissions_MtCo2_output", color="sector", 
                                  color_discrete_map=my_discrete_color_map,
                                  labels={"year": "", "emissions_MtCo2_output": "CO<sub>2</sub> Emissions (Mt CO<sub>2</sub>-eq/y)"},
                                  title="CO<sub>2</sub>-emissions by industry",
                                  width=800, height=375)
    fig_emissions_total.update_layout(transition_duration=350,
                                      template="plotly_white",
                                      legend_traceorder="reversed",
                                      title_font_color="#1F77B4",
                                      title_font_size=18,
                                      title_font_family="Rockwell",
                                      title_x = 0.02,
                                      margin=dict(t=40, r=0, b=0, l=65, pad=0))
    fig_emissions_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_emissions_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_emissions_total

### Update the valadd figure dynamically based on picker input
@app.callback(
    Output('value_added_total', 'figure'),
    [Input('services_valadd_picker', 'value'),
     Input('mining_valadd_picker', 'value'),
     Input('manufacturing_valadd_picker', 'value'),
     Input('gas_water_waste_valadd_picker', 'value'),
     Input('construction_valadd_picker', 'value'),
     Input('com_transp_valadd_picker', 'value'),
     Input('agrifor_valadd_picker', 'value'),
     Input('electricity_growth_picker', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_valadds_total(services_valadd_trend, mining_valadd_trend, manufacturing_valadd_trend, gas_water_waste_valadd_trend, 
                                construction_valadd_trend, com_transp_valadd_trend, agrifor_valadd_trend, 
                                electricity_growth_trend, tab):
    df_select = df_full[(df_full['geo']==tab) & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
    ### Value added calculation:
    ### For value added trends, we need picker 1 plus picker value 
    df_select.loc[(df_select['sector']=='Services') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(services_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Mining') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(mining_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Manufacturing') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(manufacturing_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Gas, Water & Waste Services') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(gas_water_waste_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Construction') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(construction_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Commercial Transport') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(com_transp_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Agriculture & Forestry') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(agrifor_valadd_trend/100)),df_select['yrs_since_final_obs'])
    ### Note electricity generation here has added value grow together with value added
    df_select.loc[(df_select['sector']=='Electricity generation') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(electricity_growth_trend/100)),df_select['yrs_since_final_obs'])
    
    ### Redefine value added figure again, but with dynamic input
    df_select_val_add = df_select[df_select.sector != 'LULUCF']
    df_select_val_add = df_select_val_add[df_select_val_add .sector != 'Residential']
    fig_added_value_total = px.area(df_select_val_add, x="year", y="ind_val_add_output", color="sector",
                                    color_discrete_map=my_discrete_color_map,
                                    labels={"year": "", "ind_val_add_output": "Value added (billion 2019 AUD)<sub> </sub>"},
                                    title="Value added by industry",
                                    width=800, height=375)
    fig_added_value_total.update_layout(transition_duration=350,
                                        template="plotly_white",
                                        legend_traceorder="reversed",
                                        title_font_color="#1F77B4",
                                        title_font_size=18,
                                        title_font_family="Rockwell",
                                        title_x = 0.02,
                                        margin=dict(t=40, r=0, b=0, l=65, pad=0))
    fig_added_value_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_added_value_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_added_value_total

### Update the emission intensity figure dynamically based on inputs already calculated above
@app.callback(
    Output('emis_int', 'figure'),
    [Input('agrifor_emis_picker', 'value'),
     Input('com_transp_emis_picker', 'value'),
     Input('construction_emis_picker', 'value'),
     Input('electricity_emis_picker', 'value'),
     Input('gas_water_waste_emis_picker', 'value'),
     Input('manufacturing_emis_picker', 'value'),
     Input('mining_emis_picker', 'value'),
     Input('services_emis_picker', 'value'),
     Input('services_valadd_picker', 'value'),
     Input('mining_valadd_picker', 'value'),
     Input('manufacturing_valadd_picker', 'value'),
     Input('gas_water_waste_valadd_picker', 'value'),
     Input('construction_valadd_picker', 'value'),
     Input('com_transp_valadd_picker', 'value'),
     Input('agrifor_valadd_picker', 'value'),
     Input('electricity_growth_picker', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_emis_int(agrifor_emis_trend, com_transp_emis_trend, construction_emis_trend, electricty_emis_trend, 
                  gas_water_waste_emis_trend, manufacturing_emis_trend, mining_emis_trend, services_emis_trend,
                  services_valadd_trend, mining_valadd_trend, manufacturing_valadd_trend, gas_water_waste_valadd_trend,
                  construction_valadd_trend, com_transp_valadd_trend, agrifor_valadd_trend, 
                  electricity_growth_trend, tab):
    df_select = df_full[(df_full['geo']==tab) & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
    ### Recalculate all the emissions yet again
    ### Second line with each sector is so they cannot go negative. 
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
    ### Services emmissions:
    df_select.loc[(df_select['sector']=='Services') & (df_select['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select['emissions_MtCo2_finaly']+services_emis_trend*df_select['yrs_since_final_obs']
    df_select.loc[(df_select['sector']=='Services') & (df_select['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    
    ### Value added calculation:
    ### For value added trends, we need picker 1 plus picker value 
    df_select.loc[(df_select['sector']=='Services') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(services_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Mining') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(mining_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Manufacturing') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(manufacturing_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Gas, Water & Waste Services') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(gas_water_waste_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Construction') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(construction_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Commercial Transport') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(com_transp_valadd_trend/100)),df_select['yrs_since_final_obs'])
    df_select.loc[(df_select['sector']=='Agriculture & Forestry') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(agrifor_valadd_trend/100)),df_select['yrs_since_final_obs'])
    ### Note electricity generation here has added value grow together with value added
    df_select.loc[(df_select['sector']=='Electricity generation') & (df_select['yrs_since_final_obs']>0),'ind_val_add_output'] = df_select['ind_val_add_2019_bln_finaly']*np.power((1+(electricity_growth_trend/100)),df_select['yrs_since_final_obs'])
    
    ### Emission intensity calculation:
    df_select['emis_int_outp']=df_select['emissions_MtCo2_output']/df_select['ind_val_add_output']
    ### Redefine value added figure again, but with dynamic input
    df_select_emis_int = df_select[df_select.sector != 'LULUCF']
    df_select_emis_int = df_select_emis_int[df_select_emis_int.sector != 'Residential']
    fig_emis_int = px.line(df_select_emis_int, x="year", y="emis_int_outp", color="sector",
                                    color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                    labels={"year": "", "emis_int_outp": "Emission intensity (kg CO<sub>2</sub>-eq/2019 AUD)"},
                                    title="Emission intensity by industry",
                                    width=800, height=375)
    fig_emis_int.update_layout(template="plotly_white",
                                        legend_traceorder="reversed",
                                        title_font_color="#1F77B4",
                                        title_font_size=18,
                                        title_font_family="Rockwell",
                                        title_x = 0.02,
                                        margin=dict(t=40, r=0, b=0, l=65, pad=0))
    fig_emis_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_emis_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_emis_int


### Update the elec generation and emission intensity dynamically based on picker input
@app.callback(
    Output('elec_gen_int', 'figure'),
    [Input('electricity_emis_picker', 'value'),
     Input('electricity_growth_picker', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_elec_gen_emis(electricty_emis_trend, electricity_growth_trend, tab):
    df_select_elec = df_full[(df_full['geo']==tab) & (df_full['year']>=2005) & (df_full['sector']!="Overall")]
    ### Calculate growth of electricity output in GWh:
    df_select_elec.loc[(df_select_elec['sector']=='Electricity generation') & (df_select_elec['yrs_since_final_obs']>0),'elec_gen_GWh_output'] = df_select_elec['elec_gen_GWh_finaly']*np.power((1+(electricity_growth_trend/100)),df_select_elec['yrs_since_final_obs'])
    ### Electricity emmissions:
    df_select_elec.loc[(df_select_elec['sector']=='Electricity generation') & (df_select_elec['yrs_since_final_obs']>0),'emissions_MtCo2_output'] = df_select_elec['emissions_MtCo2_finaly']+electricty_emis_trend*df_select_elec['yrs_since_final_obs']
    df_select_elec.loc[(df_select_elec['sector']=='Electricity generation') & (df_select_elec['emissions_MtCo2_output']<0), 'emissions_MtCo2_output'] = 0
    ### Calculate emission intensity:
    df_select_elec['elec_carb_int_outp']=1000*df_select_elec['emissions_MtCo2_output']/df_select_elec['elec_gen_GWh_output']
    ### Redefine Electricity generation and carbon intensity figure again, but with dynamic input
    # Make lists of data again because of course this type of figure has a completley different syntax again
    year_dict = df_select_elec['year'].tolist()
    gwh_dict = df_select_elec['elec_gen_GWh_output'].tolist()
    elec_carb_int_dict = df_select_elec['elec_carb_int_outp'].tolist()
    # create df_select_elec
    fig_elec_gen_int = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig_elec_gen_int.add_scatter(x=year_dict, y=gwh_dict, name="Electricity generation", mode="lines", line=dict(width=2, color="rgba(214,39,40,1)"), secondary_y=False,)
    fig_elec_gen_int.add_scatter(x=year_dict, y=elec_carb_int_dict, name="Carbon intensity", mode="lines", line=dict(width=2, color="black"), secondary_y=True,)
    fig_elec_gen_int.update_layout(template="plotly_white",
                                        legend_traceorder="reversed",
                                        title_text="Electricity generation and carbon intensity",
                                        title_font_color="#1F77B4",
                                        title_font_size=18,
                                        title_font_family="Rockwell",
                                        title_x = 0.02,
                                        margin=dict(t=40, r=0, b=0, l=65, pad=0),
                                        width=800, height=375)
    fig_elec_gen_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_elec_gen_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    # Set y-axes titles
    fig_elec_gen_int.update_yaxes(title_text="Electricity generation (GWh)<sub> </sub>", secondary_y=False)
    fig_elec_gen_int.update_yaxes(title_text="Carbon intensity (kg CO<sub>2</sub>-eq/kWh)", secondary_y=True)
    return fig_elec_gen_int


if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
    