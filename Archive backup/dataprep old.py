### To prep environment
# import environment.yml with navigator, or with conda:
# conda env create -f environment.yml
# activate ausenergydash

# Packages 
# import os
import pandas as pd
import xlrd # Required dependency for pd.read_excel
import re # for some string manipulation with regex
#from pyprojroot import here
# For the dash bits
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#For setting w, use here()


######### Import data mess from excel for individual states

base1990 = ['ACT', 'SA', 'TAS']
base2005 = ['NSW', 'NT', 'QLD', 'VIC', 'WA']
allstates = ['ACT', 'SA', 'TAS', 'NSW', 'NT', 'QLD', 'VIC', 'WA']
df_ = {}
for state in base1990:
    # create set of dataframes
    df_[state] = pd.read_excel('./db/State with edits.xlsx', sheet_name=state)
    ### Create column names: sector + years 2009 through 2018
    years = list(range(2009, 2051))
    years = [str(year) for year in years]
    colnamelist = []
    for year in years:    
        colnamelist.append('y'+ year)
    colnamelist = ['y1990'] + colnamelist
    colnamelist = ['varname'] + colnamelist
    colnamelist = ['sector'] + colnamelist
    del years, year 
    df_[state].columns = colnamelist
    df_[state].insert(0, 'geo', state)
    df_[state] = df_[state].drop([0,1,9,10,13,14,15,16,17,25,26,28,29,30,38,39,40,48,49,50,])
for state in base2005:
    # create set of dataframes
    df_[state] = pd.read_excel('./db/State with edits.xlsx', sheet_name=state)
    ### Create column names: sector + years 2009 through 2018
    years = list(range(2009, 2051))
    years = [str(year) for year in years]
    colnamelist = []
    for year in years:    
        colnamelist.append('y'+ year)
    colnamelist = ['y2005'] + colnamelist
    colnamelist = ['varname'] + colnamelist
    colnamelist = ['sector'] + colnamelist
    del years, year 
    df_[state].columns = colnamelist
    df_[state].insert(0, 'geo', state)
    df_[state] = df_[state].drop([0,1,9,10,13,14,15,16,17,25,26,28,29,30,38,39,40,48,49,50,])
# Create dataframa out of df in dictonary
df_states = pd.DataFrame()
for i in allstates:
    dict_new = df_[i]
    df_states = df_states.append(dict_new, ignore_index=True)


######### Import data mess from excel for national level
df_nat = pd.read_excel('./db/Nat with edits.xlsx', sheet_name='Final')
### Create column names: sector + years2005 through 2050
years = list(range(2005, 2051))
years = [str(year) for year in years]
colnamelist = []
for year in years:    
    colnamelist.append('y'+ year)
colnamelist = ['varname'] + colnamelist
colnamelist = ['sector'] + colnamelist
del years, year 
df_nat.columns = colnamelist
df_nat.insert(0, 'geo', 'National')
### Housekeeping
# get rid of non-data columns
df_nat = df_nat.drop([0,9,10,13,14,16,17,18,27,28,29,39,40,41,45,46,47])
### Create one big dataframe for national and all states
df_nat =df_nat.append(df_states)

#
########## make it tidy
# make sensible variable names
# Note National and state-level setors not exactly the same (Gas, Water & Waste Services + Electricity generation) is one thing at state level
# print (df_nat['varname'].unique())
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Emissions (Mt CO2-eq)'),'emissions_MtCo2_inp')
df_nat['varname'] = df_nat['varname'].str.replace('RBA Inflator','rba_inflator_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Industry value added ($ billions, 2019)'),'ind_val_add_2019_bln_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Industry gross value added (2019 $ billions)'),'ind_val_add_2019_bln_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Industry gross value added ($ millions nominal)'),'ind_val_add_nom_bln_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Emissions intensity (kg CO2-eq/$)'),'emis_int_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Electricity generation (GWh)'),'elec_gen_GWh_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Carbon intensity of electricity generation (kg Co2-eq/kWh)'),'elec_carb_int_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Value of electricity ($/MWh)'),'elec_value_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Population (millions)'),'pop_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Residential emissions intensity (Mt CO2-eq/millions people)'),'resi_emis_int_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Emissions Intensity (kg CO2-eq/$)'),'emis_int_inp')
df_nat['varname'] = df_nat['varname'].str.replace(re.escape('Per capita total emissions (Mt CO2-eq/millions people)'),'pcap_emis_int_inp')
# make electricity a sector
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Electricity generation (GWh)'),'Electricity generation')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Carbon intensity of electricity generation (kg Co2-eq/kWh)'),'Electricity generation')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Value of electricity ($/MWh)'),'Electricity generation')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Electricity'),'Electricity generation')
# @@ fix this. Figure out way to replace when matches whole string only
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Electricity generation generation'),'Electricity generation')
# Fix variants of agriculture and forestry as a sector
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Agriculture & Forestry'),'Agriculture')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Agriculture (note that includes Forestry)'),'Agriculture')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Agriculture (note that econ. output component includes Forestry)'),'Agriculture')
# turn non-sectoral data into overall vars
df_nat['sector'] = df_nat['sector'].str.replace('RBA Inflator','Overall')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Population (millions)'),'Overall')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape( 'Residential emissions intensity (Mt CO2-eq/millions people)'),'Overall')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Per capita total emissions (Mt CO2-eq/millions people)'),'Overall')
df_nat['sector'] = df_nat['sector'].str.replace(re.escape('Residential emissions per capita (Mt CO2-eq/millions people)'),'Overall')
### Reshaping
## reshape to doubly long
df_nat = df_nat.melt(id_vars=['geo', 'sector', 'varname'], var_name='year', value_name='y')
### reshape to tidy long
df_nat=df_nat.pivot(index=['geo', 'sector', 'year'], columns='varname', values='y')
df_nat = df_nat.reset_index()
df_nat['year'] = df_nat['year'].str.replace('y','')
#### Housekeeping
del df_states, i, state, allstates, base1990, base2005, colnamelist, dict_new, df_
#
#### Export to csv to use to mkae some calculations
df_nat.to_csv('./db/preppedraw.csv', index=False)  


