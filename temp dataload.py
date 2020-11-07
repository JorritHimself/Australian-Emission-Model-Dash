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


### Import the prepped data
df_final = pd.read_csv('./db/preppeddata.csv') 
df_nat = df_final[(df_final['geo']=='National') & (df_final['year']>=2005)]
# get good sort, with LULUCF as first one, then others on top
df_nat['sectorsorted'] =df_nat['sector']
df_nat.loc[(df_nat['sector']=='LULUCF'), 'sectorsorted'] = '0 LULUCF'
df_nat = df_nat.sort_values(['sectorsorted', 'year'], ascending=[True, True])