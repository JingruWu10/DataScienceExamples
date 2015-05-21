# Why = Analyzing Temperature data
# Where = https://courses.thinkful.com/data-001v2/project/3.2.4

"""
#SF#
We preprocess everything we need to populate the database
"""
from matplotlib import pyplot as plt
import numpy as np
import datetime
import requests
from pandas.io.json import json_normalize
import sqlite3
import pandas as pd
import collections

#################################################################
# What's the range of temperatures for each city? What is the mean temperature for each city? 
# What's the variance? Are there any patterns in the data? Which cities had the largest temperature 
# changes over the time period?
#################################################################

# create and connect to a database
conn = sqlite3.connect('weather.db')
# All interactions with the database are called querys
# And they require to be used through a cursor
c = conn.cursor()
# Retrieve data from sql database for SPRING and FALL
df_spring = pd.read_sql_query('SELECT * FROM daily_avg_spring',conn)
df_fall = pd.read_sql_query('SELECT * FROM daily_avg_fall',conn)

# Drop column date as I'm not interested in its stats
df_spring.drop('date', axis=1, inplace=True)
df_fall.drop('date', axis=1, inplace=True)


##################  Compute basics stats for both dataframes ################# 

# Spring

rge_s = {}
mean_s = {}
var_s = {}

for key in df_spring.keys():
    # compute the stats
    rge_s[key] = df_spring[key].max()-df_spring[key].min()
    mean_s[key] = df_spring[key].mean()
    var_s[key] = df_spring[key].var()

# print the results   
for key,val in rge_s.items():
    print 'The range temperature in Spring for' ,key,  'is'  ,val
for key,val in mean_s.items():
    print 'The mean temperature in Spring for' ,key,  'is'  ,round(val,1)
for key,val in mean_s.items():
    print 'The temperature  variance in Spring for' ,key,  'is'  ,round(val,1)
    
# Fall

rge_f = {}
mean_f = {}
var_f = {}

for key in df_fall.keys():
    # compute the stats
    rge_f[key] = df_fall[key].max()-df_fall[key].min()
    mean_f[key] = df_fall[key].mean()
    var_f[key] = df_fall[key].std()

# print the results      
for key,val in rge_f.items():
    print 'The range temperature in Fall for' ,key,  'is'  ,val
for key,val in mean_f.items():
    print 'The mean temperature in Fall for' ,key,  'is'  ,round(val,1)
for key,val in mean_f.items():
    print 'The temperature  variance in Fall for' ,key,  'is'  ,round(val,1)

#################################################################
# Find the greatest range in avg temperatures in the months you measured for Spring and Fall time. 
# Which city had the greatest variation? 
#################################################################

# intiate dict of monthly temperature change for spring and fall
monthly_change_spring = collections.defaultdict(int)
monthly_change_fall = collections.defaultdict(int)

# Spring

# iterate over df_spring.columns
for col in df_spring.columns:
    # put the dataframe of [col] in a list
    temp_val = df_spring[col].tolist()
    # initial values for temperature change
    temp_change = 0
    # iterate over col list using enumerate. Using enumerate we obtain a 
    # a key index (k) for each value of the list
    for k,v in enumerate(temp_val):
        if k < len(temp_val) -1:
            # update temp_change adding the difference between k+1 and k
            temp_change += abs(temp_val[k] - temp_val[k+1])
            # assign the value to the monthly_change dictionary
            monthly_change_spring[col] = temp_change    

# Fall

# iterate over df_fall.columns
for col in df_fall.columns:
    # put the dataframe of [col] in a list
    temp_val = df_fall[col].tolist()
    # initial values for temperature change
    temp_change = 0
    # iterate over col list using enumerate. Using enumerate we obtain a 
    # a key index (k) for each value of the list
    for k,v in enumerate(temp_val):
        if k < len(temp_val) -1:
            # update temp_change adding the difference between k+1 and k
            temp_change += abs(temp_val[k] - temp_val[k+1])
            # assign the value to the monthly_change dictionary
            monthly_change_fall[col] = temp_change  
    

#################################################################
# And the winner is? 
#################################################################

max_variation_spring = max(monthly_change_spring, key=monthly_change_spring.get)
max_variation_fall = max(monthly_change_fall, key=monthly_change_fall.get)

print 'The city with the greater temeprature variation in Spring is ' + max_variation_spring
print 'The city with the greater temeprature variation in Fall is ' + max_variation_fall

#################################################################
# What is the distribution of the difference? Does the result surprise you?
#################################################################

# Create an empty dataframe called monthly_temp_change to store the daily difference for 
# Spring and Fall
columns = df_spring.columns.tolist()
daily_temp_diff_spring=pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
daily_temp_diff_fall=pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)

# Spring
# iterate over df.columns
for col in df_spring.columns:
    # put the dataframe of [col] in a list
    temp_val = df_spring[col].tolist()
    temp_diff = [abs(temp_val[n]-temp_val[n-1]) for n in range(1,len(temp_val))]
    # Populate the dataframe with temp_diff relatives to col
    daily_temp_diff_spring[col] = temp_diff 
    
# Fall
# iterate over df.columns
for col in df_fall.columns:
    # put the dataframe of [col] in a list
    temp_val = df_fall[col].tolist()
    temp_diff = [abs(temp_val[n]-temp_val[n-1]) for n in range(1,len(temp_val))]
    # Populate the dataframe with temp_diff relatives to col
    daily_temp_diff_fall[col] = temp_diff


# Boxplots for each cities for spring and fall
fig, (ax1,ax2) = plt.subplots(1, 2,figsize=(10,6))
daily_temp_diff_spring.plot(kind='box',title='Spring',ax=ax1,)
daily_temp_diff_fall.plot(kind='box',title='Fall',ax=ax2)
plt.show()

#################################################################
#################################################################
# ### Spring data analysis
# 
# The distributions is similar for Lugano, Lausanne Roma and Vancouver, with the mean value
# around two. However, for Quebec and Ottawa, the mean daily difference is slightly high,
# meaning there is a greater gap between daily temp. This two cities shows also a greater variability
# in daily temperature
# 
# ### Fall data analysis
# 
# In Fall, the daily mean difference value for Quebec and Ottawa is in the same range than 
# the other cities. However they still show graeter variability compared to the other cities.
# 
# ### Final conclusion
# 
# We have more chance to have a 'hot' day followed by a 'chill' day in Ottawa, than in Lausanne even though they are at the same latitutde.
#################################################################
#################################################################
