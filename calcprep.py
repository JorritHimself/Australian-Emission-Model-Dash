### ToDo: 
# Column with baseline leves for all the above (1990 or 2005 levels)
# column with annual perc growth form sliders
# column with annual perc rgowth from slider to the power of years since 2008 or 2009
# Trends: per capita residential emissions 2008-2017
# Trends: per capita total emissions 2008-2017


# source the data preparation yes or no
exec(open('./dataprep.py').read())

# Packages 
# import os
import pandas as pd
import numpy as np
import re # for some string manipulation with regex

# @@ Set first and last years of data here
firstyearnat = 2008
lastyearnat = 2018
firstyearstate = 2009
lastyearstate = 2018

### Import the prepped df_nat 
df_nat = pd.read_csv('./db/preppedraw.csv') 

### Create column with emissions, value added, and GWh electricity in the last year of data: used to multiply with trend
df_lasty = df_nat
df_lasty['tokeep'] = 0
df_lasty.loc[(df_lasty['year']==lastyearstate) & (df_lasty['geo']!= 'National'), 'tokeep'] = 1
df_lasty.loc[(df_lasty['year']==lastyearnat) & (df_lasty['geo']== 'National'), 'tokeep'] = 1
df_lasty = df_lasty[df_lasty['tokeep']==1]
df_lasty =  df_lasty[['geo', 'sector','emis_int_inp', 'emissions_MtCo2_inp', 'ind_val_add_2019_bln_inp', 'elec_gen_GWh_inp']]
df_lasty.columns = ['geo', 'sector', 'emis_int_finaly',  'emissions_MtCo2_finaly', 'ind_val_add_2019_bln_finaly', 'elec_gen_GWh_finaly']

### Create column with emissions, value added, and GWh electricity in the FIRST YEAR of data: used to calculate avg trend
df_firsty = df_nat
df_firsty['tokeep'] = 0
df_firsty.loc[(df_firsty['year']==firstyearstate) & (df_firsty['geo']!= 'National'), 'tokeep'] = 1
df_firsty.loc[(df_firsty['year']==firstyearnat) & (df_firsty['geo']== 'National'), 'tokeep'] = 1
df_firsty = df_firsty[df_firsty['tokeep']==1]
df_firsty =  df_firsty[['geo', 'sector','emis_int_inp', 'emissions_MtCo2_inp', 'ind_val_add_2019_bln_inp', 'elec_gen_GWh_inp']]
df_firsty.columns = ['geo', 'sector', 'emis_int_firsty', 'emissions_MtCo2_firsty', 'ind_val_add_2019_bln_firsty', 'elec_gen_GWh_firsty']

### Calculate long-term trends
df_trend = pd.merge(df_lasty, df_firsty, how='left', on=['geo', 'sector'])
# Emission reduction trend: change in MtCo2/y
df_trend.loc[(df_trend['geo']!='National'), 'emissions_MtCo2_trend']= (df_trend['emissions_MtCo2_finaly']-df_trend['emissions_MtCo2_firsty'])/(lastyearstate-firstyearstate)
df_trend.loc[(df_trend['geo']=='National'), 'emissions_MtCo2_trend']= (df_trend['emissions_MtCo2_finaly']-df_trend['emissions_MtCo2_firsty'])/(lastyearnat-firstyearnat)
# Emission intenisty trend: annual change in MtCo2/$ 
# 10 year trend
df_trend['emis_int_trend'] = df_trend['emis_int_finaly']/df_trend['emis_int_firsty']
# Annual trend: 10 year factor to the power of 1/10
df_trend.loc[(df_trend['geo']!='National'), 'emis_int_trend']= np.power((df_trend['emis_int_trend']),1/(lastyearstate-firstyearstate))
df_trend.loc[(df_trend['geo']=='National'), 'emis_int_trend']= np.power((df_trend['emis_int_trend']),1/(lastyearnat-firstyearnat))
# Industry value added trend: %/year
# 10 year trend
df_trend['ind_val_add_2019_bln_trend'] = df_trend['ind_val_add_2019_bln_finaly']/df_trend['ind_val_add_2019_bln_firsty']
# Annual trend: 10 year factor to the power of 1/10
df_trend.loc[(df_trend['geo']!='National'), 'ind_val_add_2019_bln_trend']= np.power((df_trend['ind_val_add_2019_bln_trend']),1/(lastyearstate-firstyearstate))
df_trend.loc[(df_trend['geo']=='National'), 'ind_val_add_2019_bln_trend']= np.power((df_trend['ind_val_add_2019_bln_trend']),1/(lastyearnat-firstyearnat))
# Electricity generation growth trend: %/year
# 10 year trend
df_trend['elec_gen_GWh_trend'] = df_trend['elec_gen_GWh_finaly']/df_trend['elec_gen_GWh_firsty']
# Annual trend: 10 year factor to the power of 1/10
df_trend.loc[(df_trend['geo']!='National'), 'elec_gen_GWh_trend']= np.power((df_trend['elec_gen_GWh_trend']),1/(lastyearstate-firstyearstate))
df_trend.loc[(df_trend['geo']=='National'), 'elec_gen_GWh_trend']= np.power((df_trend['elec_gen_GWh_trend']),1/(lastyearnat-firstyearnat))

### Retain the last year of all emission, value added, and electricty gen: these are used to multiply with growth factor from user input
df_trend = df_trend[['geo', 'sector', 'emissions_MtCo2_finaly', 'ind_val_add_2019_bln_finaly', 'elec_gen_GWh_finaly', 
                     'emissions_MtCo2_trend', 'emis_int_trend', 'ind_val_add_2019_bln_trend','elec_gen_GWh_trend']]

### Base year and base-year emissions
df_baseyear = df_nat
df_baseyear['tokeep'] = 0
### base1990 = ['ACT', 'SA', 'TAS']
base2005 = ['National', 'ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
# Keep base year only
# Flag the base year rows
###for state in base1990:
###    df_baseyear.loc[(df_baseyear['geo']==state) & (df_baseyear['year']== 1990), 'tokeep'] = 1
for state in base2005:
    df_baseyear.loc[(df_baseyear['geo']==state) & (df_baseyear['year']== 2005), 'tokeep'] = 1
# Keep only the dtaa for the baseyears
df_baseyear = df_baseyear[df_baseyear['tokeep']==1]
df_baseyear = df_baseyear[['geo', 'sector', 'year', 'emissions_MtCo2_inp']]
df_baseyear.columns = ['geo','sector', 'baseyear', 'emissions_MtCo2_baseyear']

### Add trends and base years to main df
full_df= pd.merge(df_nat, df_trend, how='left', on=['geo', 'sector'])
full_df= pd.merge(full_df, df_baseyear, how='left', on=['geo', 'sector'])
full_df.drop(columns=['tokeep'])

### Create column with multiplication factor: this number will be adjusted by sliders
# Years since last year of observed data
full_df.loc[full_df['geo']== 'National', 'yrs_since_final_obs'] = full_df['year']-lastyearnat
full_df.loc[full_df['geo']!= 'National', 'yrs_since_final_obs'] = full_df['year']-lastyearstate
### Housekeeping
del base2005, df_baseyear, df_firsty, df_lasty, df_trend, state, firstyearnat, firstyearstate, lastyearnat, lastyearstate, df_nat

### Calculate output numbers
#!!! Note this is just for baseline graphs. User input from sliders should do all these calculations again 
# Take the trend to the power of the number of years passed since the last year of input data
full_df['ind_val_add_multiplier']= np.power((full_df['ind_val_add_2019_bln_trend']),full_df['yrs_since_final_obs'])
full_df['elec_gen_GWh_multiplier']= np.power((full_df['elec_gen_GWh_trend']),full_df['yrs_since_final_obs'])

### Value added output: trend multiplied with last observation
full_df['ind_val_add_output']=full_df['ind_val_add_multiplier']*full_df['ind_val_add_2019_bln_finaly']
# But keep original input for years where we have data
full_df.loc[(full_df['yrs_since_final_obs']<=0), 'ind_val_add_output'] = full_df['ind_val_add_2019_bln_inp']

### Electircity generation output: trend multiplied with last observation
full_df['elec_gen_GWh_output']=full_df['elec_gen_GWh_multiplier']*full_df['elec_gen_GWh_finaly']
# But keep original input for years where we have data
full_df.loc[(full_df['yrs_since_final_obs']<=0), 'elec_gen_GWh_output'] = full_df['elec_gen_GWh_inp']

### Emissions output: emissions levels at last observation, minus number of years since final observation *annual emission reductions
full_df['emissions_MtCo2_output']=full_df['emissions_MtCo2_finaly']+full_df['emissions_MtCo2_trend']*full_df['yrs_since_final_obs']
# But keep original input for years where we have data
full_df.loc[(full_df['yrs_since_final_obs']<=0), 'emissions_MtCo2_output'] = full_df['emissions_MtCo2_inp']

### Emissions intensity output: forget input just calculate
full_df['emis_int_outp']=full_df['emissions_MtCo2_output']/full_df['ind_val_add_output']

### Carbon intensity of electricity generation output: forget input just calculate
full_df['elec_carb_int_outp']=1000*full_df['emissions_MtCo2_output']/full_df['elec_gen_GWh_output']

# But keep original input for years where we have data
full_df.loc[(full_df['yrs_since_final_obs']<=0), 'emissions_MtCo2_output'] = full_df['emissions_MtCo2_inp']













#### Export to csv to use to use in dash app
full_df.to_csv('./db/preppeddata.csv', index=False) 