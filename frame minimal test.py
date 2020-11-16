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

#######################  HTML divs styles  ######################

# the style arguments for the header. 
my_header_style = {
    "background-color": "#f8f9fa",
    'width': "100%"
}

# the style arguments for the header. 
my_tablist_style = {
    "position": "sticky",
    "top": 0,
    "background-color": "#f8f9fa",
    'width': "100%"
}


# the style arguments for the sidebar. Sticky on top: scrolls untill 50px from top
my_sidebar_style = {
    "position": "sticky",
    "top": 50,
    "background-color": "#f8f9fa",
}

#style={"padding": "0px 10px 0px 10px", "position": "sticky", "top": 0, 'zIndex': 9999

# the styles for the main content position it to the right of the sidebar and
# add some padding.
my_content_style = {
    "background-color": "#f8f9fa",
}





### Define the app
# Note an additional stylesheet is loaded locally, see assets/bootstrap_modified.css
app = dash.Dash(__name__)


header  = html.Div(style=my_header_style, children=[ ### backgroundColor here is for the whole webpage
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div(html.H1('  ANU CCEP Australian emissions trend tool thingy'))),
            ],style={"color": "#1F77B4"}),
        dbc.Row([
            html.Div(html.H4('How to use this tool. NB This text needs updating:')),
            ]),
        dbc.Row([
            html.Div(html.H4('1. Use the "Scenario Input" pickers to adjust: (i) 2018-2050 average growth in economic output for each industry (+ growth in electricity generation), & (ii) 2018-2050 average annual industry emissions reductions. The default inputs are historical 2008-2017 data. Hence, the default outputs represent a continuation of 2008-2017 trends across the 2018-2050 period.')),
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
            dcc.Tab(label='Documentation', value='docs'),
            dcc.Tab(label='Reports', value='other')
            ]),
        ], fluid=True), 
    ])

sidebar  = html.Div(style=my_sidebar_style, children=[
    dbc.Container([
        html.Div(id='tabslist-sidebar')
        ]),
    ])


content  = html.Div(style=my_sidebar_style, children=[
    dbc.Container([
        html.Div(id='tabslist-content')
        ]),
    ])


app.layout = html.Div([header, tabheader, sidebar, content])
    
        

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
    

