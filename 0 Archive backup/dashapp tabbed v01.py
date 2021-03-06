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
# Better slider
# Smaller everything
# Create separate emis and va df
# Add calculations as in excel scenario sheet
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



### Import the prepped input data
df_full = pd.read_csv('./db/preppeddata.csv')
### Import the slider settings 
df_slider_in = pd.read_excel('./db/sliderslist.xlsx', sheet_name="slidersettings") 

# get good sort, with LULUCF as first one, then others on top
df_full['sectorsorted']=df_full['sector']
df_full.loc[(df_full['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_full.loc[(df_full['sector']=='Residential'), 'sectorsorted'] = '1 Residential'
df_full.loc[(df_full['sector']=='Electricity generation'), 'sectorsorted'] = '2 Electricity generation'
df_full = df_full.sort_values(['sectorsorted', 'year'], ascending=[True, True])

# Define list of states
statelist = ['National' , 'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
# Define list of slider names: this will be used in a loop to create a dictionary of vlues to set slidersettinsg for each state
sliderlist = ['services_emis_slider','mining_emis_slider','manufacturing_emis_slider','gas_water_waste_emis_slider','construction_emis_slider',
'com_transp_emis_slider','agrifor_emis_slider','lulucf_emis_slider','electricity_emis_slider','residential_emis_slider',
'services_valadd_slider','mining_valadd_slider','manufacturing_valadd_slider','gas_water_waste_valadd_slider',
'construction_valadd_slider','com_transp_valadd_slider','agrifor_valadd_slider','electricity_growth_slider']
# Define list of slider settings: this will be used in a loop to create a dictionary of vlues to set slidersettinsg for each state
slidersettinglist = ['min', 'max','value', 'steps', 'marks']

### Get national values: these are use to create the figures for when the user lands on the page and hasnt selected a tab yet
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2005) & (df_full['sector']!="Overall")]
### List of starting figures and other output
### Work with defined set of colors to keep sector the same color across figures
## Emissions figure
fig_emissions_total = px.area(df_select, x="year", y="emissions_MtCo2_output", color="sector", 
                              color_discrete_sequence=['#1F77B4', '#FF7F0E', '#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                              labels={"year": "", "emissions_MtCo2_output": "CO<sub>2</sub> Emissions (Mt CO<sub>2</sub>-eq/y)"},
                              title="CO<sub>2</sub>-emissions by industry")
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
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
df_select_val_add = df_select[df_select.sector != 'LULUCF']
df_select_val_add = df_select_val_add [df_select_val_add.sector != 'Residential']
fig_added_value_total = px.area(df_select_val_add, x="year", y="ind_val_add_output", color="sector",
                                color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                labels={"year": "", "ind_val_add_output": "Value added (billion 2019 AUD)<sub> </sub>"},
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

## Emission intensity figure
df_select = df_full[(df_full['geo']=='National') & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
df_select_emis_int = df_select[df_select.sector != 'LULUCF']
df_select_emis_int = df_select_emis_int[df_select_emis_int.sector != 'Residential']
fig_emis_int = px.line(df_select_emis_int, x="year", y="emis_int_outp", color="sector",
                                color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                labels={"year": "", "emis_int_outp": "Emission intensity (kg CO<sub>2</sub>-eq/2019 AUD)"},
                                title="Emission intensity by industry")
fig_emis_int.update_layout(template="plotly_white",
                                    legend_traceorder="reversed",
                                    title_font_color="#1F77B4",
                                    title_font_size=18,
                                    title_font_family="Rockwell",
                                    title_x = 0.02,
                                    margin=dict(t=40, r=0, b=0, l=60, pad=0))
fig_emis_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
fig_emis_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)




### Define the app
# Note an additional stylesheet is loaded locally, see assets/bootstrap_modified.css
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

### Define the app layout with tabs: content 'tabslist-content' is generated based on the tab selection
app.layout = html.Div(style={'backgroundColor': 'rgba(242, 241, 239, 1)'}, children=[ ### backgroundColor here is for the whole webpage
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div(html.H1('  ANU CCEP Australian emissions trend tool thingy'))),
            ],style={"color": "#1F77B4"}),
        dbc.Row([
            html.Div(html.H4('How to use this tool. NB This text needs updating:')),
            ]),
        dbc.Row([
            html.Div(html.H4('1. Use the "Scenario Input" sliders to adjust: (i) 2018-2050 average growth in economic output for each industry (+ growth in electricity generation), & (ii) 2018-2050 average annual industry emissions reductions. The default inputs are historical 2008-2017 data. Hence, the default outputs represent a continuation of 2008-2017 trends across the 2018-2050 period.')),
            ]),
        dbc.Row([
            html.Div(html.H4('2. Review your Scenario in the Output cells and the 7 graphs. Historical data is provided in Column M to compare the 2020-2030 "decarbonisation effort" that your scenario involves. If the values for 2020-2030 are more negative than 2008-2017, then the decarbonisation effort in your scenario is greater than historical data. Note that higher industry output growth for a given annual emissions reduction will increase decarbonisation effort & vice versa. See the Glossary for variable definitions. ')),
            ]),
        dbc.Row([
            html.Div(html.H4('3. Select a Reference Scenario and compare your 2050 Emissions Reductions and Negative Emissions to reference values in Column K. Compare your Scenario to other Reference Scenarios & consider adjusting your Scenario Inputs accordingly. You may want to consider different ways to meet a Net-Zero 2050 Emissions Target.')),
            ]),
        dbc.Row([
            html.Div(html.H4('"4. Finalise your Scenario. You can name your Scenario and include your name in the cells provided. If you would like to make another Scenario, you can ""Save As"" the excel workbook with your scenario name and start again with the original file. Happy 2050 emissions pathway scenario building!!"')),
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
        ], fluid=True, style={"padding": "0px 130px 0px 130px", "position": "sticky", "top": 0, 'zIndex': 9999}), ### padding around the tabs box. Sticky and zIndex make it float on top of the other stuff. Keep padding top at 0 because otherwise the other stuff will be visible again 
    dbc.Container([
        html.Div(id='tabslist-content')
        ], fluid=True, style={"padding": "0px 60px 10px 60px"}) ### padding around the entire app
    ])


dict_of_fig = dict({
    "data": [{"type": "bar",
              "x": [1, 2, 3],
              "y": [1, 3, 2]}],
    "layout": {"title": {"text": "A Figure Specified By A Graph Object With A Dictionary"}}
})


### Define app content based on tab choice. 
### The slider value selection is a separate callback, below this block
@app.callback(Output('tabslist-content', 'children'),
              [Input('tabslist', 'value')])
def render_content(tab):
    if tab in statelist:
        ## Loop to get the right slider settings for each state and type of slider
        df_sliderselect = df_slider_in[(df_slider_in['geo']==tab)]
        df_sliderselect = df_sliderselect.set_index('slider')
        slidersetting_dict = {}
        for slidername in sliderlist:
            for slidersetting in slidersettinglist:
                slidersetting_dict[slidername + '_' + slidersetting] = df_sliderselect._get_value(slidername, slidersetting)
        return html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=2),
                    dbc.Col((html.Div(html.H4('Annaul industry emission reduction'))), width=2),
                    dbc.Col((html.Div(html.H4('Industry gross added value growth'))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=2),
                    dbc.Col((html.Div(html.H5('(% annual change in 2019 AUD)'))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Services'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='services_emis_slider', min=slidersetting_dict['services_emis_slider_min'], max=slidersetting_dict['services_emis_slider_max'], value=slidersetting_dict['services_emis_slider_value'], step=slidersetting_dict['services_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['services_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='services_valadd_slider', min=slidersetting_dict['services_valadd_slider_min'], max=slidersetting_dict['services_valadd_slider_max'], value=slidersetting_dict['services_valadd_slider_value'], step=slidersetting_dict['services_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['services_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(23,190,207,0.8)"}),     
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Mining'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='mining_emis_slider', min=slidersetting_dict['mining_emis_slider_min'], max=slidersetting_dict['mining_emis_slider_max'], value=slidersetting_dict['mining_emis_slider_value'], step=slidersetting_dict['mining_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['mining_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='mining_valadd_slider', min=slidersetting_dict['mining_valadd_slider_min'], max=slidersetting_dict['mining_valadd_slider_max'], value=slidersetting_dict['mining_valadd_slider_value'], step=slidersetting_dict['mining_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['mining_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(127,127,127,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Manufacturing'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='manufacturing_emis_slider', min=slidersetting_dict['manufacturing_emis_slider_min'], max=slidersetting_dict['manufacturing_emis_slider_max'], value=slidersetting_dict['manufacturing_emis_slider_value'], step=slidersetting_dict['manufacturing_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['manufacturing_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='manufacturing_valadd_slider', min=slidersetting_dict['manufacturing_valadd_slider_min'], max=slidersetting_dict['manufacturing_valadd_slider_max'], value=slidersetting_dict['manufacturing_valadd_slider_value'], step=slidersetting_dict['manufacturing_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['manufacturing_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(188,189,34,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Gas, water & waste services'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='gas_water_waste_emis_slider', min=slidersetting_dict['gas_water_waste_emis_slider_min'], max=slidersetting_dict['gas_water_waste_emis_slider_max'], value=slidersetting_dict['gas_water_waste_emis_slider_value'], step=slidersetting_dict['gas_water_waste_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['gas_water_waste_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='gas_water_waste_valadd_slider', min=slidersetting_dict['gas_water_waste_valadd_slider_min'], max=slidersetting_dict['gas_water_waste_valadd_slider_max'], value=slidersetting_dict['gas_water_waste_valadd_slider_value'], step=slidersetting_dict['gas_water_waste_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['gas_water_waste_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(227,119,194,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Construction'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='construction_emis_slider', min=slidersetting_dict['construction_emis_slider_min'], max=slidersetting_dict['construction_emis_slider_max'], value=slidersetting_dict['construction_emis_slider_value'], step=slidersetting_dict['construction_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['construction_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='construction_valadd_slider', min=slidersetting_dict['construction_valadd_slider_min'], max=slidersetting_dict['construction_valadd_slider_max'], value=slidersetting_dict['construction_valadd_slider_value'], step=slidersetting_dict['construction_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['construction_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(140,86,75,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Commercial transport'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='com_transp_emis_slider', min=slidersetting_dict['com_transp_emis_slider_min'], max=slidersetting_dict['com_transp_emis_slider_max'], value=slidersetting_dict['com_transp_emis_slider_value'], step=slidersetting_dict['com_transp_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['com_transp_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='com_transp_valadd_slider', min=slidersetting_dict['com_transp_valadd_slider_min'], max=slidersetting_dict['com_transp_valadd_slider_max'], value=slidersetting_dict['com_transp_valadd_slider_value'], step=slidersetting_dict['com_transp_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['com_transp_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(148,103,189,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Agriculture & Forestry'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='agrifor_emis_slider', min=slidersetting_dict['agrifor_emis_slider_min'], max=slidersetting_dict['agrifor_emis_slider_max'], value=slidersetting_dict['agrifor_emis_slider_value'], step=slidersetting_dict['agrifor_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['agrifor_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='agrifor_valadd_slider', min=slidersetting_dict['agrifor_valadd_slider_min'], max=slidersetting_dict['agrifor_valadd_slider_max'], value=slidersetting_dict['agrifor_valadd_slider_value'], step=slidersetting_dict['agrifor_valadd_slider_steps'], marks=ast.literal_eval(slidersetting_dict['agrifor_valadd_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(44,160,44,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('LULUCF'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='lulucf_emis_slider', min=slidersetting_dict['lulucf_emis_slider_min'], max=slidersetting_dict['lulucf_emis_slider_max'], value=slidersetting_dict['lulucf_emis_slider_value'], step=slidersetting_dict['lulucf_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['lulucf_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=2),
					],style={"background-color": "rgba(31,119,180,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=2),
                    dbc.Col((html.Div(html.H4('Annaul industry emission reduction'))), width=2),
                    dbc.Col((html.Div(html.H4('Electricity generation growth'))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H5(''))), width=2),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=2),
                    dbc.Col((html.Div(html.H5('(% per year)'))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Electricity generation'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='electricity_emis_slider', min=slidersetting_dict['electricity_emis_slider_min'], max=slidersetting_dict['electricity_emis_slider_max'], value=slidersetting_dict['electricity_emis_slider_value'], step=slidersetting_dict['electricity_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['electricity_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='electricity_growth_slider', min=slidersetting_dict['electricity_growth_slider_min'], max=slidersetting_dict['electricity_growth_slider_max'], value=slidersetting_dict['electricity_growth_slider_value'], step=slidersetting_dict['electricity_growth_slider_steps'], marks=ast.literal_eval(slidersetting_dict['electricity_growth_slider_marks'])))), width=2),
                    ],style={"background-color": "rgba(214,39,40,0.8)"}),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Sector'))), width=2),
                    dbc.Col((html.Div(html.H4('Annaul emission reduction'))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4(''))), width=2),
                    dbc.Col((html.Div(html.H5('(Mt CO2-eq per year)'))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=2),
                    ]),
                dbc.Row([
                    dbc.Col((html.Div(html.H4('Residential'))), width=2),
                    dbc.Col((html.Div(dcc.Slider(id='residential_emis_slider', min=slidersetting_dict['residential_emis_slider_min'], max=slidersetting_dict['residential_emis_slider_max'], value=slidersetting_dict['residential_emis_slider_value'], step=slidersetting_dict['residential_emis_slider_steps'], marks=ast.literal_eval(slidersetting_dict['residential_emis_slider_marks'])))), width=2),
                    dbc.Col((html.Div(html.H4(''))), width=2),
                    ],style={"background-color": "rgba(255,127,14,0.8)"}),
                ], fluid=True, style={"padding": "20px 80px 20px 80px", 'backgroundColor': 'rgba(242, 241, 239, 1)', "position": "sticky", "top": 60, 'zIndex': 9999}), ### This is for padding aroudn the entire app: fill the entire screen, but keep padding top right bottom left at x pixels
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div(dcc.Graph(id='emissions_total', figure = fig_emissions_total))),
                    dbc.Col(html.Div(dcc.Graph(id='value_added_total', figure = fig_added_value_total))),
                    ]),
                ], fluid=True, style={"padding": "20px 60px 20px 60px"}),
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div(dcc.Graph(id='emis_int', figure = fig_emis_int))),
                    dbc.Col(html.Div(html.H4('Some other figure'))),
                    ]),
                ], fluid=True, style={"padding": "20px 60px 20px 60px"}),
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div(html.H4('Some other figure'))),
                    dbc.Col(html.Div(html.H4('Some other figure'))),
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

### Update the emissions figure dynamically based on slider input
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
                                  color_discrete_sequence=['#1F77B4', '#FF7F0E', '#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                    labels={"year": "", "emissions_MtCo2_output": "CO<sub>2</sub> Emissions (Mt CO<sub>2</sub>-eq/y)"},
                                    title="CO<sub>2</sub>-emissions by industry")
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

### Update the valadd figure dynamically based on slider input
@app.callback(
    Output('value_added_total', 'figure'),
    [Input('services_valadd_slider', 'value'),
     Input('mining_valadd_slider', 'value'),
     Input('manufacturing_valadd_slider', 'value'),
     Input('gas_water_waste_valadd_slider', 'value'),
     Input('construction_valadd_slider', 'value'),
     Input('com_transp_valadd_slider', 'value'),
     Input('agrifor_valadd_slider', 'value'),
     Input('electricity_growth_slider', 'value'),
     Input('tabslist', 'value')]
    )
def update_figure_valadds_total(services_valadd_trend, mining_valadd_trend, manufacturing_valadd_trend, gas_water_waste_valadd_trend, 
                                construction_valadd_trend, com_transp_valadd_trend, agrifor_valadd_trend, 
                                electricity_growth_trend, tab):
    df_select = df_full[(df_full['geo']==tab) & (df_full['year']>=2009) & (df_full['sector']!="Overall")]
    ### Value added calculation:
    ### For value added trends, we need slider 1 plus slider value 
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
                                    color_discrete_sequence=['#D62728', '#2CA02C', '#9467BD', '#8C564B', '#E377C2', '#BCBD22', '#7F7F7F', '#17BECF'],
                                    labels={"year": "", "ind_val_add_output": "Value added (billion 2019 AUD)<sub> </sub>"},
                                    title="Value added by industry")
    fig_added_value_total.update_layout(transition_duration=500,
                                        template="plotly_white",
                                        legend_traceorder="reversed",
                                        title_font_color="#1F77B4",
                                        title_font_size=18,
                                        title_font_family="Rockwell",
                                        title_x = 0.02,
                                        margin=dict(t=40, r=0, b=0, l=60, pad=0))
    fig_added_value_total.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_added_value_total.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_added_value_total

### Update the emission intensity figure dynamically based on inputs already calculated above


@app.callback(
    Output('emis_int', 'figure'),
    [Input('agrifor_emis_slider', 'value'),
     Input('com_transp_emis_slider', 'value'),
     Input('construction_emis_slider', 'value'),
     Input('electricity_emis_slider', 'value'),
     Input('gas_water_waste_emis_slider', 'value'),
     Input('manufacturing_emis_slider', 'value'),
     Input('mining_emis_slider', 'value'),
     Input('services_emis_slider', 'value'),
     Input('services_valadd_slider', 'value'),
     Input('mining_valadd_slider', 'value'),
     Input('manufacturing_valadd_slider', 'value'),
     Input('gas_water_waste_valadd_slider', 'value'),
     Input('construction_valadd_slider', 'value'),
     Input('com_transp_valadd_slider', 'value'),
     Input('agrifor_valadd_slider', 'value'),
     Input('electricity_growth_slider', 'value'),
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
    ### For value added trends, we need slider 1 plus slider value 
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
                                    title="Emission intensity by industry")
    fig_emis_int.update_layout(template="plotly_white",
                                        legend_traceorder="reversed",
                                        title_font_color="#1F77B4",
                                        title_font_size=18,
                                        title_font_family="Rockwell",
                                        title_x = 0.02,
                                        margin=dict(t=40, r=0, b=0, l=60, pad=0))
    fig_emis_int.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    fig_emis_int.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='rgba(149, 165, 166, 0.6)', mirror=True)
    return fig_emis_int




if __name__ == '__main__':
    app.run_server(debug=True)
    

